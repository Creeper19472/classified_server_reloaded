import socket
import sys
import pkgGenerator as gpkg

sys.path.append('../')

from letscrypt import RSA, BLOWFISH

class ConnThreads():
    def __init__(self, tname, conn, addr, rsa_keys):
        self.thread_name = tname
        self.conn = conn
        self.addr = addr
        self.rsa_fkey, self.rsa_ekey = rsa_keys
        self.conn.send(self.rsa_fkey) # Send RSA Public Key
        self.bf_key = RSA.Decrypt(self.conn.recv(8192), self.rsa_ekey)
        self.IOThread()

    def send(self, msg):
        bytes_msg = BLOWFISH.Encrypt(msg, self.bf_key)
        self.conn.send(bytes_msg)

    def recv(self, limit=8192):
        cipher_bytes_text = self.conn.recv(limit)
        bytes_text = BLOWFISH.Decrypt(cipher_bytes_text, self.bf_key)
        text = bytes_text.decode()
        return text

    def IOThread(self):
        self.send(gpkg.gpkg.Message('Success', 'FuckU'))
        while True:
            pass
