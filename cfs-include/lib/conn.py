# -*- coding: utf-8 -*-

import socket, sys, sqlite3, gettext, json, re
import generator.socketpkg as gpkg
import threading

from docrypt import RSA, BLOWFISH
import tool.logkit as logkit
import interface.usertools as usertools
import lib.parser.replace as replace

class ConnThreads(threading.Thread):
    def __init__(self, tname, conn, addr, rsa_keys, **kwargs):
        self.root_dir = kwargs['root_dir']
        self.db_prefix = kwargs['db_prefix']
        self.thread_name = tname
        self.conn = conn
        self.addr = str(addr)
        self.rsa_fkey, self.rsa_ekey = rsa_keys
        self.log = logkit.log(
            logname="Core.Threads.%s" % self.thread_name,
            filepath="".join((self.root_dir, "/cfs-content/log/threads.log")),
        )
        self.lang = kwargs['lang'] # self.lang = language
        dbconn = sqlite3.connect("".join((self.root_dir, "/cfs-content/database/sqlite3.db")))
        dbcursor = dbconn.cursor()
        options = dict(dbcursor.execute('select key, value from {0}options'.format(self.db_prefix)))
        dbconn.close()
        self.ptext = options['protection_text']
        self.system_info = (kwargs['display_name'], '0.3.x', 'cfs_master')
        self.run()

    def run(self):
        es = gettext.translation("cfs_connsupport", localedir="cfs-content/locale", languages=[self.lang], fallback=True)
        es.install()
        self.required_client_version = 5
        self.gpkg = gpkg.GeneratePackage(self.required_client_version, self.system_info)
        self.conn.send(self.rsa_fkey)  # Send RSA Public Key
        self.bf_key = RSA.Decrypt(self.conn.recv(8192), self.rsa_ekey)
        self.log.logger.debug(
            _("Encryption enabled successfully. Blowfish key: %s.") % self.bf_key
        )
        try:
            self.IOThread()
        except (ConnectionResetError, json.decoder.JSONDecodeError):
            self.log.logger.info(
                _("Connection Reset %s. Closing %s.") % (self.addr, self.thread_name)
            )
            sys.exit()
        except SystemExit:
            self.log.logger.info(
                _("Disconnected from %s. Closing %s.") % (self.addr, self.thread_name)
            )
            sys.exit()
        except:
            self.log.logger.fatal(
                _("In %s, one (or more) exceptions were caught:") % self.thread_name,
                exc_info=True,
            )
            self.log.logger.fatal(
                _("Due to the above exception, this thread cannot continue to run.")
            )
            sys.exit()

    def send(self, msg):
        self.log.logger.debug(_("Sending message %s.") % msg)
        bytes_msg = BLOWFISH.Encrypt(msg, self.bf_key)
        self.conn.send(bytes_msg)

    def recv(self, limit=8192):
        cipher_bytes_text = self.conn.recv(limit)
        text = BLOWFISH.Decrypt(cipher_bytes_text, self.bf_key)
        self.log.logger.debug(_("Received message %s.") % text)
        return text

    def IOThread(self):
        self.send(self.gpkg.Message("Success", "OK"))
        username = None  # Flake8 fix
        do_login = False
        while True:
            recv = self.recv()
            args = recv['Message'].split()
            args[0] = args[0].lower()
            if args[0] == "login":
                if not len(args) == 3:
                    self.send(self.gpkg.BadRequest())
                    continue
                if do_login == True:
                    self.log.logger.info(
                        _("%s: User %s is already logged in.") % (self.addr, username)
                    )
                    self.send(
                        self.gpkg.Message("Already logged in", "Please logout first.")
                    )
                    continue
                username = args[1]
                db_username = None
                password = args[2]
                dbconn = sqlite3.connect("./cfs-content/database/sqlite3.db")
                dbcursor = dbconn.cursor()
                users = dbcursor.execute(
                    "select username, password, authlevel from %s" % "".join((self.db_prefix, 'auth'))
                )
                for row in users:
                    if row[0] == username:
                        db_username = row[0]
                        db_password = row[1]
                        self.log.logger.debug(
                            _("Found user %s, password is %s.") % (username, db_password)
                        )
                        authlevel = int(row[2])
                        break
                dbconn.close()
                if db_username == None:
                    self.log.logger.warn(
                        _("%s: Username is incorrect. Login failed.") % self.addr
                    )
                    self.send(
                        self.gpkg.Message(
                            "Login FAILED", "Incorrect username or password.", 400
                        )
                    )
                    continue
                if password == db_password:
                    self.log.logger.info(
                        _("%s: User %s's password is match. Can login.")
                        % (self.addr, username)
                    )
                    self.send(self.gpkg.Message("SUCCESS", "Login Success!"))
                    do_login = True
                else:
                    self.log.logger.warn(
                        _("%s: User %s's password is incorrect. Login failed.")
                        % (self.addr, username)
                    )
                    self.send(
                        self.gpkg.Message(
                            "Login FAILED", "Incorrect username or password.", 400
                        )
                    )
            elif args[0] == "getfile":
                if not len(args) == 2:
                    self.send(self.gpkg.BadRequest())
                    continue
                try:
                    if not do_login == True:
                        raise PermissionError
                except PermissionError:
                    self.send(self.gpkg.Forbidden("You must to login first."))
                    continue
                filename = args[1]
                dbconn = sqlite3.connect("./cfs-content/database/sqlite3.db")
                dbcursor = dbconn.cursor()
                files = dbcursor.execute(
                    "select title, content, protectionlevel from %s" % "".join((self.db_prefix, 'file'))
                )
                targetname = None
                for row in files:
                    if row[0] == filename:
                        targetname = row[0] # set name instead None
                        content = row[1]
                        protectionlevel = int(row[2])
                dbconn.close()
                if targetname == None:
                    self.send(self.gpkg.FileNotFound('23333'))
                    continue
                if protectionlevel > authlevel:
                    self.send(self.gpkg.Forbidden(_("The security level required to request the document is higher than the current user level")))
                    continue
                result = replace.replacer.replaceTag("blocked", content, authlevel, self.ptext)
                self.send(self.gpkg.Message("Result", result))
            elif args[0] == "user":
                if not len(args) >= 2:
                    self.send(self.gpkg.BadRequest())
                    continue
                ut = usertools.usertools(self.db_prefix)
                if args[1] == "add":
                    if not len(args) == 4:
                        self.send(self.gpkg.BadRequest())
                        continue
                    if do_login is False:
                        self.send(self.gpkg.Message("What?!", "You must to login first."))
                        continue
                    if ut.isAdmin(username) is False:
                        self.log.logger.warn(_("%s: User %s tried to add a new user %s, but did not have the right to do so.") % (self.addr, username, args[2]))
                        self.send(
                            self.gpkg.Forbidden(
                                "You are not an administrator, this command is not for you!"
                            )
                        )
                        continue
                    if ut.isUserExists(args[2]) is True:
                        self.send(self.gpkg.BadRequest("Are you serious??"))
                        continue
                    if ut.addUser(args[2], args[3]) is False:
                        self.send(self.gpkg.Message("Error", "...", Code=500))
                    else:
                        self.send(self.gpkg.Message("Success", "Successfully added a new user."))
                    continue
                elif args[1] == "remove":
                    if not len(args) == 3:
                        self.send(self.gpkg.BadRequest())
                        continue
                    if do_login is False:
                        self.send(self.gpkg.Message("What?!", "You must to login first."))
                        continue
                    if ut.isUserExists(args[2]) is False:
                        self.send(self.gpkg.BadRequest("The server couldn\'t find the user."))
                        continue
                    if ut.isAdmin(username) is False:
                        self.send(
                            self.gpkg.Forbidden(
                                "You are not an administrator, this command is not for you!"
                            )
                        )
                        continue
                    if ut.removeUser(args[2]) is False:
                        self.send(self.gpkg.Message("Error", "Can\'t remove the user.", Code=500))
                    else:
                        self.send(self.gpkg.Message("Success", "Successfully removed the user."))
                elif args[1] == "passwd":
                    if do_login is False:
                        self.send(self.gpkg.Message("What?!", "You must to login first."))
                        continue
                    if len(args) == 4:
                        if ut.isAdmin(username) is False:
                            self.send(
                                self.gpkg.Forbidden(
                                    "You are not an administrator, this command is not for you!"
                                )
                            )
                            continue
                        if ut.passwd(args[2], args[3]) is False:
                            self.send(self.gpkg.Message("Error", "...", Code=500))
                            continue
                        else:
                            self.send(self.gpkg.Message("Success", "Successfully changed the password."))
                            continue
                    elif len(args) < 3:
                        self.send(self.gpkg.BadRequest())
                        continue
                    if ut.passwd(username, args[2]) is False:
                        self.send(self.gpkg.Message("Error", "...", Code=500))
                        continue
                    else:
                        self.send(self.gpkg.Message("Success", "Successfully changed the password."))
                else:
                    self.send(self.gpkg.BadRequest())
    

            elif args[0] == "logout":
                if do_login is False:
                    self.send(self.gpkg.Message("What?!", "You must to login first."))
                    continue
                do_login = False
                self.log.logger.info(_('%s: User %s logged out.') % (self.addr, username))
                self.send(self.gpkg.Message("OK", "Successfully logged out."))
            elif args[0] == "stop":
                if do_login is False:
                    self.send(self.gpkg.Message("What?!", "You must to login first."))
                    continue
                if ut.isAdmin(username) is True:
                    self.log.logger.info("Server shutdown has been scheduled!")
                    self.send(
                        self.gpkg.Message(
                            "Scheduled", "Server shutdown has been scheduled!"
                        )
                    )
                else:
                    self.send(
                        self.gpkg.Forbidden(
                            "You are not an administrator, this command is not for you!"
                        )
                    )
            elif args[0] == "disconnect":
                self.conn.close()
                sys.exit()
            else:
                self.send(self.gpkg.BadRequest())
