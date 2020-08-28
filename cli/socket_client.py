import socket, sys, random, string, rsa, json, hashlib

sys.path.append('./functions/')

from letscrypt import *
import pkgGenerator as gpkg

class IO():
    def __init__(self, fkey, bf_key):
        self.rsa_fkey = fkey
        self.blowfish_key = bf_key

    def send(self, msg):
        bytes_msg = BLOWFISH.Encrypt(msg, self.blowfish_key)
        client.send(bytes_msg)

    def recv(self, limit=8192):
        bytes_recv = client.recv(limit)
        recv = BLOWFISH.Decrypt(bytes_recv, self.blowfish_key)
        return recv

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliinfo = ("127.0.0.1", 5104)
client.connect(cliinfo)

with open('./$.tmp', 'w') as file:
    file.write(client.recv(8192).decode())
with open('./$.tmp') as file:
    fkey = rsa.PublicKey.load_pkcs1(file.read())

salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))

obj = bytes(json.dumps(salt), encoding='UTF-8')
cipher_text = rsa.encrypt(obj, fkey)
client.send(cipher_text)

MsgIO = IO(fkey, salt)

recv = MsgIO.recv()
SHA256 = hashlib.sha256('123456'.encode()).hexdigest()
MsgIO.send(gpkg.gpkg.Message('CMD', 'Login master %s' % SHA256))
recv = MsgIO.recv()
print(recv)
MsgIO.send(gpkg.gpkg.Message('CMD', 'disconnect'))
client.close()
