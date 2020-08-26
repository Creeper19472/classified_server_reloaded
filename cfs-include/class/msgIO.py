import socket, sys, sqlite3
import pkgGenerator as gpkg

sys.path.append('../')
sys.path.append('./common/')

from letscrypt import RSA, BLOWFISH
import logkit

class ConnThreads():
    def __init__(self, tname, conn, addr, rsa_keys):
        self.thread_name = tname
        self.conn = conn
        self.addr = addr
        self.account = None
        self.password = None
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
                self.log.logger.debug('Loads options from the database.')
                dbconn = sqlite3.connect('./cfs-content/database/sqlite3.db')
                dbcursor = dbconn.cursor()
                users = dbcursor.execute('select username, password, authlevel from auth')
                for row in users:
                    if row[0] == account:
                        PASSWORD = row[1]
                        self.log.logger.debug('Found user %s, password is %s.' % (account, PASSWORD))
                        AUTHLEVEL = row[2]
                        break
                dbconn.close()
                if bool(self.password) is False:
                    self.log.logger.warn('Cannot found user. Login failed.')
                    self.send(gpkg.gpkg.Message('Login FAILED', 'Incorrect username or password.'))
                    continue
                if password == PASSWORD:
                    self.account = account
                    self.password = PASSWORD
                    self.authlevel = AUTHLEVEL
                else:
                    self.log.logger.warn('User %s\'s password is incorrect. Login failed.' % account)
                    self.send(gpkg.gpkg.Message('Login FAILED', 'Incorrect username or password.'))
            elif splitrecv[0] == "disconnect":
                self.conn.close()
                sys.exit()
