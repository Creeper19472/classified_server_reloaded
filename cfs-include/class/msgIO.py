import socket, sys, sqlite3
import pkgGenerator as gpkg
import threading

sys.path.append('..')
sys.path.append('.\\common')
sys.path.append('.\\interface')

from letscrypt import RSA, BLOWFISH
import logkit, logio, fileDetect

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
            self.log.logger.fatal('In %s, one (or more) exceptions were caught:' % self.thread_name, exc_info=True)
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
            splitrecv[0] = splitrecv[0].lower()
            if splitrecv[0] == 'login':
                if not len(splitrecv) == 3:
                    self.send(gpkg.gpkg.BadRequest())
                    continue
                account = splitrecv[1]
                password = splitrecv[2]
                global login_action
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
            elif splitrecv[0] == 'getfile':
                if not len(splitrecv) == 2:
                    self.send(gpkg.gpkg.BadRequest())
                    continue
                try:
                    if not login_action.log_in == True:
                        raise PermissionError
                except PermissionError:
                    self.send(gpkg.gpkg.Forbidden('You must login first.'))
                    continue
                filename = splitrecv[1]
                try:
                    with open('./cfs-content/database/files/%s' % filename) as file:
                        if filename.find('../') != -1:
                            raise PermissionError('The client uses the \'../\' command')
                        result = fileDetect.Blocked.ReplaceBlock(file.read(), login_action.authlevel)
                        self.send(gpkg.gpkg.Message('Result', result))
                except (IsADirectoryError, FileNotFoundError):
                    self.send(gpkg.gpkg.FileNotFound())
                except (PermissionError, NameError):
                    self.send(gpkg.gpkg.BadRequest())

            elif splitrecv[0] == "disconnect":
                self.conn.close()
                sys.exit()
            else:
                self.send(gpkg.gpkg.BadRequest())
