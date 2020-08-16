﻿# -*- coding: UTF-8 -*-

VERSION = "0.3.0a3"

import sys, os, json, socket, sqlite3, rsa, gettext, time, random, threading, string

# os.system('') CFS-2020081601: Can't display custom colors.

### LOGGER MOUDLE STARTS ###
import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
lfhandler = logging.FileHandler(filename='./cfs-content/log/main.log')
cshandler = logging.StreamHandler()
formatter1 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter2 = logging.Formatter('[%(asctime)s %(levelname)s] %(message)s')
lfhandler.setLevel(logging.DEBUG)
cshandler.setLevel(logging.DEBUG)
lfhandler.setFormatter(formatter1)
cshandler.setFormatter(formatter2)
logger.addHandler(lfhandler)
logger.addHandler(cshandler)
### LOGGER MOUDLE ENDS ###

sys.path.append('''./cfs-include/''')
sys.path.append('''./cfs-include/claas/''')
sys.path.append('''./cfs-include/class/common/''')

import colset, letscrypt
from strFormat import *

server = socket.socket()

time1 = time.time()

logger.debug('Defines method title().')
def title():
    print(multicol.Yellow("______________                    _________________     _________"))
    print(multicol.Yellow("__  ____/__  /_____ _________________(_)__  __/__(_)__________  /"))
    print(multicol.Yellow("_  /    __  /_  __ `/_  ___/_  ___/_  /__  /_ __  /_  _ \  __  / "))
    print(multicol.Yellow("/ /___  _  / / /_/ /_(__  )_(__  )_  / _  __/ _  / /  __/ /_/ /  "))
    print(multicol.Yellow("\____/  /_/  \__,_/ /____/ /____/ /_/  /_/    /_/  \___/\__,_/   "))
    print(multicol.Yellow('Classified Server') + multicol.Green(' RELOADED ') + '[%s]' % VERSION)
    print()

logger.debug('Inits multicol.')
multicol = colset.Colset()

title()
print('Running On: Python %s' % sys.version)

if os.path.exists('_classified_initialized') == False:
    logger.info('The system is initializing...')
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
        logger.error('The value of the language is invaild.')
        sys.exit()

    dbconn = sqlite3.connect('./cfs-content/database/sqlite3.db')
    dbcursor = dbconn.cursor()
    '''with open('./cfs-content/database/setup', 'r', encoding='utf-8') as scriptfile:
        for line in scriptfile:
            dbcursor.execute(line)
        print(dbconn.total_changes)
        dbconn.commit()
        dbconn.close()''' # CFS-2020081501: Can't run scripts from files.
    try:
        dbcursor.executescript('''
            create table auth(username, password, authlevel);
            insert into auth values('master', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 5);
            create table server(key, value);
            insert into server values('host', '0.0.0.0');
            insert into server values('port', '5104');
            insert into server values('language', '%s');
            insert into server values('name', 'Classified_Server')
            ''' % lang)
    except:
        pass
    dbcursor.execute('''insert into server values('version', '%s')''' % VERSION)
    logger.debug('Total Changes: %s.' % dbconn.total_changes)
    dbconn.commit()
    dbconn.close()
    with open("_classified_initialized", "w") as x:
        x.write('\n')

### INIT SQLITE3 ###
dbconn = sqlite3.connect('./cfs-content/database/sqlite3.db')
dbcursor = dbconn.cursor()
settings = dict(dbcursor.execute('select key, value from server'))
dbconn.close()
### END SQLITE3 ###

lang = settings['language']

es = gettext.translation(
        'cfs_server',
        localedir = 'cfs-content/locale',
        languages = [lang],
        fallback = True
        )
es.install()

svcinfo = (settings['host'], int(settings['port']))

sqlite3.connect('./cfs-content/database/sqlite3.db')

server.bind(svcinfo)
server.listen(15)

logger.info(_("Verifying plugin information ..."))

time2 = time.time() - time1
logger.info(_("Done(%ss)!") % time2)

with open("./cfs-content/cert/e.pem", "rb") as x:
    ekey = x.read()
with open("./cfs-content/cert/f.pem", "rb") as x:
    fkey = x.read()

# salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
# print(letscrypt.BLOWFISH.Encrypt('aaaaaaa', salt))

while True:
    conn, addr = server.accept() # 等待链接,多个链接的时候就会出现问题,其实返回了两个值
    ThreadNewName = "Thread-%s" % random.randint(1,10000)
    NewThread = MainThread(1, ThreadNewName, 1)
    NewThread.start()
