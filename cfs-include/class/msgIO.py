import socket, sys, sqlite3
import pkgGenerator as gpkg
import threading

sys.path.append('..')
sys.path.append('.\\common')
sys.path.append('.\\interface')

from letscrypt import RSA, BLOWFISH
import logkit, logio

class ConnThreads(threading.Thread):
    def __init__(self, tname, conn, addr, rsa_keys):
        self.thread_name = tname
        self.conn = conn
        self.addr = str(addr)
        self.rsa_fkey, self.rsa_ekey = rsa_keys
        self.log = logkit.log(logname='Core.Threads.%s' % self.thread_name, filepath='./cfs-content/log/threads.log')
        self.run()

    def run(self):
        self.conn.send(self.rsa_fkey) # Send RSA Public Key
        self.bf_key = RSA.Decrypt(self.conn.recv(8192), self.rsa_ekey)
        self.log.logger.debug('Encryption enabled successfully. Blowfish key: %s.' % self.bf_key)
        try:
            self.IOThread()
        except ConnectionResetError:
            self.log.logger.info('Connection Reset %s. Closing %s.' % (self.addr, self.thread_name))
            sys.exit()
        except SystemExit:
            self.log.logger.info('Disconnected from %s. Closing %s.' % (self.addr, self.thread_name))
            sys.exit()
        except:
            self.log.logger.fatal('In %s, one (or more) exceptions were caught:', print_exc=True)
            self.log.logger.fatal('Due to the above exception, this thread cannot continue to run.')
            sys.exit()

    def send(self, msg):
        self.log.logger.debug('Sending message %s.' % msg)
        bytes_msg = BLOWFISH.Encrypt(msg, self.bf_key)
        self.conn.send(bytes_msg)

    def recv(self, limit=8192):
        cipher_bytes_text = self.conn.recv(limit)
        text = BLOWFISH.Decrypt(cipher_bytes_text, self.bf_key)
        self.log.logger.debug('Received message %s.' % text)
        return text

    def IOThread(self):
        self.send(gpkg.gpkg.Message('Success', 'OK'))
        while True:
            recv = self.recv()
            splitrecv = recv['Message'].split()
            if splitrecv[0].lower() == 'login':
                if not len(splitrecv) == 3:
                    self.send(gpkg.gpkg.BadRequest())
                    continue
                account = splitrecv[1]
                password = splitrecv[2]
                login_action = logio.logIO(self.thread_name, account)
                callback = login_action.log_in(password)
                print(callback)
                if callback == 0:
                    self.log.logger.info('%s: User %s\'s password is match. Can login.' % (self.addr, login_action.username))
                    self.send(gpkg.gpkg.Message('SUCCESS', 'Login Success!'))
                elif callback == 1:
                    self.log.logger.warn('%s: User %s\'s password is incorrect. Login failed.' % (self.addr, login_action.username))
                    self.send(gpkg.gpkg.Message('Login FAILED', 'Incorrect username or password.', 400))
                elif callback == -1:
                    self.send(gpkg.gpkg.Message('Already logged in', 'Already logged in.'))
                elif callback == 2:
                    self.log.logger.warn('Username is incorrect. Login failed.')
                    self.send(gpkg.gpkg.Message('Login FAILED', 'Incorrect username or password.', 400))
            elif splitrecv[0] == "disconnect":
                self.conn.close()
                sys.exit()
            else:
                self.send(gpkg.gpkg.BadRequest())
