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
            spiltrecv = recv['Message'].split()
            if splitrecv[0] == 'Login':
                account = spiltrecv[1]
                password = spiltrecv[2]
                log.logger.debug('Loads options from the database.')
                dbconn = sqlite3.connect('./cfs-content/database/sqlite3.db')
                dbcursor = dbconn.cursor()
                settings = dict(dbcursor.execute('select username, password, authlevel from auth'))
                print(settings)
                dbconn.close()
