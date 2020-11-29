# -*- coding: UTF-8 -*-

VERSION = "0.3.6.099"

import sys

try:
    import os, json, socket, sqlite3, rsa, gettext, time, random, threading
except ModuleNotFoundError:
    print(
        'FATAL: Modules not found. Please run "pip install -r requirements.txt" to install these required modules.'
    )
    sys.exit(1)

sys.path.append("./cfs-include/")

import common.colset as colset
import letscrypt
from connsupport import *

import common.logkit as logkit

log = logkit.log(logname="Core.Shell", filepath="./cfs-content/log/shell.log")

server = socket.socket()

time1 = time.time()

log.logger.debug("Setting up the server...")


def title():
    print(
        multicol.Yellow(
            "______________                    _________________     _________"
        )
    )
    print(
        multicol.Yellow(
            "__  ____/__  /_____ _________________(_)__  __/__(_)__________  /"
        )
    )
    print(
        multicol.Yellow(
            "_  /    __  /_  __ `/_  ___/_  ___/_  /__  /_ __  /_  _ \  __  / "
        )
    )
    print(
        multicol.Yellow(
            "/ /___  _  / / /_/ /_(__  )_(__  )_  / _  __/ _  / /  __/ /_/ /  "
        )
    )
    print(
        multicol.Yellow(
            "\____/  /_/  \__,_/ /____/ /____/ /_/  /_/    /_/  \___/\__,_/   "
        )
    )
    print(
        multicol.Yellow("Classified Server")
        + multicol.Green(" RELOADED ")
        + "[%s]" % VERSION
    )
    print()


multicol = colset.Colset()

title()
print("Running On: Python %s" % sys.version)

if os.path.exists("_classified_initialized") == False:
    log.logger.info("The system is initializing...")
    os.chdir("./cfs-content/cert/")
    letscrypt.RSA.CreateNewKey(2048)
    os.chdir("../../")
    langlist = {
        "0": "en_US",
        "1": "zh_CN",
    }
    print("Please choose a language:")
    print(langlist)
    try:
        lang = langlist[input("# ")]
    except KeyError:
        log.logger.error("The value of the language is invaild.")
        sys.exit()

    log.logger.debug("Connecting to the database...")
    dbconn = sqlite3.connect("./cfs-content/database/sqlite3.db")
    dbcursor = dbconn.cursor()
    """with open('./cfs-content/database/setup', 'r', encoding='utf-8') as scriptfile:
        for line in scriptfile:
            dbcursor.execute(line)
        print(dbconn.total_changes)
        dbconn.commit()
        dbconn.close()"""  # CFS-2020081501: Can't run scripts from files.
    log.logger.debug("Writing options to the database...")
    try:
        dbcursor.executescript(
            """
            create table auth(username, password, authlevel, isadmin);
            insert into auth values('master', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 5, 1);
            create table server(key, value);
            insert into server values('host', '0.0.0.0');
            insert into server values('port', '5104');
            insert into server values('language', '%s');
            insert into server values('name', 'Classified_Server')
            """
            % lang
        )
    except:
        pass
    dbcursor.execute("""insert into server values('version', '%s')""" % VERSION)
    log.logger.debug("Total Changes: %s." % dbconn.total_changes)
    dbconn.commit()
    dbconn.close()
    with open("_classified_initialized", "w") as x:
        x.write("\n")

### INIT SQLITE3 ###
dbconn = sqlite3.connect("./cfs-content/database/sqlite3.db")
dbcursor = dbconn.cursor()
settings = dict(dbcursor.execute("select key, value from server"))
dbconn.close()
log.logger.debug("General options loaded: %s" % settings)
### END SQLITE3 ###

log.logger.debug("Setting up general settings...")
lang = settings["language"]
server_name = settings["name"]

es = gettext.translation(
    "cfs_shell", localedir="cfs-content/locale", languages=[lang], fallback=True
)
es.install()

svcinfo = (settings["host"], int(settings["port"]))

sqlite3.connect("./cfs-content/database/sqlite3.db")

try:
    server.bind(svcinfo)
    server.listen(15)
except:
    log.logger.fatal("There was a problem listening on the port.", exc_info=True)
    sys.exit()

log.logger.info(_("Server Name: %s") % server_name)
log.logger.info(_("IPv4 Address: %s:%s") % (svcinfo[0], svcinfo[1]))
log.logger.info(_("IPv6 is not supported."))

log.logger.debug(_("Loading RSA resources..."))
with open("./cfs-content/cert/e.pem", "rb") as x:
    ekey = x.read()
with open("./cfs-content/cert/f.pem", "rb") as x:
    fkey = x.read()

time2 = time.time() - time1
log.logger.info(_("Done(%ss)!") % time2)

while True:
    conn, addr = server.accept()  # 等待链接,多个链接的时候就会出现问题,其实返回了两个值
    log.logger.info(_("New connection: %s") % str(addr))
    ThreadName = "Thread-%s" % random.randint(1, 10000)
    Thread = threading.Thread(
        target=ConnThreads, args=(ThreadName, conn, addr, (fkey, ekey)), name=ThreadName
    )
    Thread.start()
    log.logger.debug(_("A new thread %s has started.") % ThreadName)
