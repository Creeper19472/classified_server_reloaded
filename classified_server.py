# -*- coding: UTF-8 -*-

VERSION = "0.3.0a1"

import sys, os, json, socket, sqlite3, rsa, configparser, gettext, time, random, threading, string

sys.path.append('''./cfs-include/''')
sys.path.append('''./cfs-include/claas/''')
sys.path.append('''./cfs-include/class/common/''')

# Logger by 公众号python学习开发
from functools import wraps
from logger import get_logger
import traceback

def decorator(func):
    @wraps(func)
    def log(*args,**kwargs):
        try:
            print("当前运行方法",func.__name__)
            return func(*args,**kwargs)
        except Exception as e:
            get_logger().error(f"{func.__name__} is error,here are details:{traceback.format_exc()}")
    return log

import colset, letscrypt
from strFormat import *

server = socket.socket()

time1 = time.time()

@decorator
def title():
    print(multicol.Yellow("______________                    _________________     _________"))
    print(multicol.Yellow("__  ____/__  /_____ _________________(_)__  __/__(_)__________  /"))
    print(multicol.Yellow("_  /    __  /_  __ `/_  ___/_  ___/_  /__  /_ __  /_  _ \  __  / "))
    print(multicol.Yellow("/ /___  _  / / /_/ /_(__  )_(__  )_  / _  __/ _  / /  __/ /_/ /  "))
    print(multicol.Yellow("\____/  /_/  \__,_/ /____/ /____/ /_/  /_/    /_/  \___/\__,_/   "))
    print(multicol.Yellow('Classified Server') + multicol.Green(' RELOADED ') + '[%s]' % VERSION)
    print()

multicol = colset.Colset()

title()
print('Running On: Python %s' % sys.version)

if os.path.exists('_classified_initialized') == False:
    print(StrFormat.INFO() + 'The system is initializing, please wait ...')
    os.chdir('./cfs-content/cert/')
    letscrypt.RSA.CreateNewKey(2048)
    os.chdir('../../')
    import shutil
    shutil.copyfile('./cfs-include/class/template/config-sample.ini', './config/config.ini')
    langlist = {
        '0': 'en_US',
        '1': 'zh_CN',
        }
    print('Please choose a language:')
    print(langlist)
    try:
        lang = langlist[input('# ')]
    except KeyError:
        print('Value is invaild.')
        sys.exit()
    config = configparser.ConfigParser()
    config.read('./config/config.ini')
    config.set('SERVER', 'LANGUAGE', lang)
    config.write(open('./config/config.ini', 'w'))

    dbconn = sqlite3.connect('./cfs-content/database/sqlite3.db')
    dbcursor = dbconn.cursor()
    with open('./cfs-content/database/setup', 'r', encoding='utf-8') as scriptfile:
        script = scriptfile.read()
        dbcursor.executescript(script)
    with open("_classified_initialized", "w") as x:
        x.write('\n')

config = configparser.ConfigParser()
config.read('./config/config.ini')

lang = config.get("SERVER", "LANGUAGE")
es = gettext.translation(
        'cfs_server',
        localedir = 'locale',
        languages = [lang],
        fallback = True
        )
es.install()

svcinfo = ()

sqlite3.connect('./cfs-content/database/sqlite3.db')


server.bind(svcinfo)
server.listen(15)

print(StrFormat.INFO() + _("Verifying plugin information ..."))

time2 = time.time() - time1
print(StrFormat.INFO() + _("Done(%ss)!") % time2)

with open("./secure/e.pem", "rb") as x:
    ekey = x.read()
with open("./secure/f.pem", "rb") as x:
    fkey = x.read()

# salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
# print(letscrypt.BLOWFISH.Encrypt('aaaaaaa', salt))

while True:
    if EnablePlugins == True:
        for i in lists:
            exec(i + '.main()')
    conn, addr = server.accept() # 等待链接,多个链接的时候就会出现问题,其实返回了两个值
    ThreadNewName = "Thread-%s" % random.randint(1,10000)
    NewThread = MainThread(1, ThreadNewName, 1)
    NewThread.start()
