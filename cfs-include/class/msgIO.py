import socket, sys, sqlite3
import pkgGenerator as gpkg

sys.path.append('../')
sys.path.append('./common/')
sys.path.append('./api/')

from letscrypt import RSA, BLOWFISH
import logkit, logio

class ConnThreads():
    def __init__(self, tname, conn, addr, rsa_keys):
        self.thread_name = tname
        self.conn = conn
        self.addr = addr
        self.rsa_fkey, self.rsa_ekey = rsa_keys
        self.log = logkit.log(logname='Core.Threads.%s' % self.thread_name, filepath='./cfs-content/log/threads.log')
        self.conn.send(self.rsa_fkey) # Send RSA Public Key
        self.bf_key = RSA.Decrypt(self.conn.recv(8192), self.rsa_ekey)
        self.log.logger.debug('Encryption enabled successfully! Blowfish key: %s.' % self.bf_key)
        self.run()

    def run(self):
        self.IOThread()

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
                account = splitrecv[1]
                password = splitrecv[2]
                login_action = logio.logIO(self.thread_name, account)
                if login_action.log_in(password) is False:
                    self.log.logger.warn('Username or password is incorrect. Login failed.')
                    self.send(gpkg.gpkg.Message('Login FAILED', 'Incorrect username or password.', 400))
                    continue
                else:
                    self.log.logger.info('User %s\'s password is match. Can login.' % login_action.username)
                    self.send(gpkg.gpkg.Message('SUCCESS', 'Login Success!'))
            elif splitrecv[0] == "disconnect":
                self.conn.close()
                sys.exit()
