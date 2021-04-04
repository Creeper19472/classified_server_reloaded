# -*- coding: UTF-8 -*-

VERSION = "0.4.4.100"

import sys, os, json, socket, sqlite3, rsa, gettext, time, random, threading

current_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.append(''.join((current_dir, '/cfs-include')))

# BEGIN cfs_config.py
with open('cfs_config.py') as script:
    exec(script.read())
# END cfs_config.py

import tool.colset as colset
from tool.ipv46 import *
import slib.docrypt as letscrypt
from libconn import *

import tool.logkit as logkit

log = logkit.log(logname="Loader", filepath=''.join((current_dir, '/cfs-content/log/loader.log')))

server = socket.socket()

begin_time = time.time()

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
            create table {0}auth(username, password, authlevel, role);
            insert into {0}auth values('master', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 5, ('admin'));
            create table {0}file(id, title, content, protectionlevel, author);
            insert into {0}file values(0, 'Example', 'Hello world!', 0, 'master');
            create table {0}options(key, value);
            insert into {0}options values('protection_text', '[DATA REDACTED]')
            """.format(database_prefix)
        )
    except:
        pass
    log.logger.debug("Total Changes: %s." % dbconn.total_changes)
    dbconn.commit()
    dbconn.close()
    with open("_classified_initialized", "w") as x:
        x.write("\n")

es = gettext.translation("cfs_loader", localedir="./cfs-content/locale", languages=[language], fallback=True)
es.install()

if enable_ipv4 is False and enable_ipv6 is False:
    log.logger.fatal(_("ipv4 and ipv6 are not enabled, what the hell do you want to do?!"))
    sys.exit()

try:
    if enable_ipv4 is True:
        ipvstatus = IPvStatus(bind4_address[0])
        if ipvstatus.ipv4():
            server.bind(bind4_address)
            server.listen(0)
        else:
            enable_ipv4 = False
    if enable_ipv6 is True:
        ipvstatus = IPvStatus(bind6_address[0])
        if ipvstatus.ipv6():
            server.bind(bind6_address)
            server.listen(0)
        else:
            enable_ipv6 = False
except socket.error:
    enable_ipv6 = False
except:
    log.logger.fatal("There was a problem listening on the port.", exc_info=True)
    sys.exit()

if enable_ipv4 is False and enable_ipv6 is False:
    raise socket.error('Unable to monitor the specified protocol.')

log.logger.info(_("Server Name: %s") % display_name)
if enable_ipv4:
    log.logger.info(_("IPv4 Address: {0}").format(bind4_address))
else:
    log.logger.info(_("IPv4 is not supported."))
if enable_ipv6:
    log.logger.info(_("IPv6 Address: {0}").format(bind6_address))
else:
    log.logger.info(_("IPv6 is not supported."))

log.logger.debug(_("Loading RSA resources..."))
with open("./cfs-content/cert/e.pem", "rb") as x:
    ekey = x.read()
with open("./cfs-content/cert/f.pem", "rb") as x:
    fkey = x.read()

end_time = time.time()
total_time = end_time - begin_time
log.logger.info(_("Done(%ss)!") % total_time)

while True:
    conn, addr = server.accept()  # 等待链接,多个链接的时候就会出现问题,其实返回了两个值
    log.logger.info(_("New connection: %s") % str(addr))
    ThreadName = "Thread-%s" % random.randint(1, 10000)
    Thread = threading.Thread(
        target=ConnThreads, args=(ThreadName, conn, addr, (fkey, ekey)),kwargs={'root_dir':current_dir, 'lang': language, 'db_prefix': database_prefix, 'display_name': display_name}, name=ThreadName
    )
    Thread.start()
    log.logger.debug(_("A new thread %s has started.") % ThreadName)
