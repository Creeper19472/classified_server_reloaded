import socket, sys, random, string, rsa, json, hashlib

sys.path.append("./functions/")

from letscrypt import *
import pkgGenerator as gpkg
from userGenerator import Generator

CLIENT_VERSION = 4

class IO:
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

with open("./$.tmp", "w") as file:
    file.write(client.recv(8192).decode())
with open("./$.tmp") as file:
    fkey = rsa.PublicKey.load_pkcs1(file.read())

salt = Generator.GeneratePassword(1, 32)
print(salt)

obj = bytes(json.dumps(salt[0]), encoding="UTF-8")
cipher_text = rsa.encrypt(obj, fkey)
client.send(cipher_text)

MsgIO = IO(fkey, salt[0])

recv = MsgIO.recv()
if recv['required_client_version'] > CLIENT_VERSION:
    print('Warning: The server requires a higher version of the client. ')


while True:
    cmd = input("# ")
    if cmd == "":
        continue
    split = cmd.split()
    if split[0].lower() == "login":
        try:
            if not bool(split[2]) is True:
                print("Exception: Missing args.")
                continue
        except:
            print("Exception: Missing args.")
            continue
        SHA256 = hashlib.sha256(split[2].encode()).hexdigest()
        MsgIO.send(gpkg.gpkg.Message("CMD", "Login %s %s" % (split[1], SHA256)))
        print(MsgIO.recv()['Message'])
    elif split[0].lower() == "disconnect":
        MsgIO.send(gpkg.gpkg.Message("CMD", "disconnect"))
        client.close()
        sys.exit()
    else:
        MsgIO.send(gpkg.gpkg.Message("CMD", cmd))
        recv = MsgIO.recv()
        print(recv['Message'])
        continue
