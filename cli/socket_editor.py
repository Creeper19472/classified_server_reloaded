# -*- coding: utf-8 -*-

import socket, sys, random, string, rsa, json, hashlib
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import tkinter.messagebox as messagebox

sys.path.append("./functions/")

from letscrypt import *
import pkgGenerator as gpkg
from userGenerator import Generator

CLIENT_VERSION = 6

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

def usr_log_in(event=None):
    statusbar.config(text='Getting Information')
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()
    SHA256 = hashlib.sha256(usr_pwd.encode()).hexdigest()
    MsgIO.send(gpkg.gpkg.Message("client/request", "CMD", cmd="login", username=usr_name, password=SHA256))
    statusbar.config(text='Waiting for response')
    if MsgIO.recv()['Code'] == 200:
        global logged_in
        logged_in = True
        window.destroy()
    else:
        statusbar.config(text='Failed!')
        Label(window, text='Login failed.').place(x=100, y=170)

def load(event=None):
    filenm = filename.get()
    MsgIO.send(gpkg.gpkg.Message("client/request", "CMD", cmd='file', action='get', gettype='source', fileid=int(filenm)))
    result = MsgIO.recv()
    contents.delete('1.0', END)
    contents.insert(INSERT, result['Message'])
    statusbar.config(text='done')
    
def save(event=None):
    filenm = filename.get()
    content = contents.get('1.0', 'end-1c')
    MsgIO.send(gpkg.gpkg.Message("client/request", "CMD", cmd='file', action='post', fileid=filenm, \
                                 filedata={'content': content}))
    result = MsgIO.recv()
    if result['Code'] != 200:
        statusbar.config(text='Save failed')
        messagebox.showerror('保存失败', '服务器返回以下错误：\n%s' % result['Message'])
    else:
        statusbar.config(text='Success')
        messagebox.showinfo('成功', '服务器无异常')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliinfo = ("127.0.0.1", 5104)
client.connect(cliinfo)

client.send(bytes("Non-HTTP/1.0 200", encoding="UTF-8"))

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


window = Tk()
window.title('Login Page')
window.geometry('400x300')
window.minsize(400, 300)   # 最小尺寸
window.maxsize(400, 300)   # 最大尺寸
# 登陆界面
Label(window, text='Account：').place(x=100,y=100)
Label(window, text='Password：').place(x=100, y=140)

var_usr_name = StringVar()
enter_usr_name = Entry(window, textvariable=var_usr_name)
enter_usr_name.place(x=160, y=100)

var_usr_pwd = StringVar()
enter_usr_pwd = Entry(window, textvariable=var_usr_pwd, show='*')
enter_usr_pwd.place(x=160, y=140)
enter_usr_pwd.bind("<Return>", usr_log_in)

logged_in = False

bt_login = Button(window,text='Login',command=usr_log_in)
bt_login.place(x=120,y=230)

statusbar = Label(window, text="Ready", bd=1, relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

window.mainloop()

if logged_in is False:
    sys.exit()

top = Tk()
top.title("CFMS Editor")
top.minsize(650, 500)   # 最小尺寸
top.maxsize(650, 500)   # 最大尺寸
 

contents = ScrolledText()
contents.grid(row=1, column=0, columnspan=3)

filename = Entry()
filename.bind("<Return>", load)
filename.grid(row=0, column=0, sticky=W+E)

btn1 = Button(text='Open', command=load)
btn2 = Button(text='Save', command=save, state=DISABLED)
btn1.grid(row=0, column=1, sticky=E)
btn2.grid(row=0, column=2, sticky=E)

statusbar = Label(top, text="Waiting for input", bd=1, relief=SUNKEN, anchor=W)
statusbar.grid(row=2, column=0, columnspan=3, sticky=W+E)

mainloop()

