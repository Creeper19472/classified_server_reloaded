import socket, sys, sqlite3, gettext, json, re
import gpkg
import threading

from letscrypt import RSA, BLOWFISH
import common.logkit as logkit
import interface.usertools as usertools
import replace

class ConnThreads(threading.Thread):
    def __init__(self, tname, conn, addr, rsa_keys):
        self.thread_name = tname
        self.conn = conn
        self.addr = str(addr)
        self.rsa_fkey, self.rsa_ekey = rsa_keys
        self.log = logkit.log(
            logname="Core.Threads.%s" % self.thread_name,
            filepath="./cfs-content/log/threads.log",
        )
        self.run()

    def run(self):
        dbconn = sqlite3.connect("cfs-content/database/sqlite3.db")  # init sqlite3
        dbcursor = dbconn.cursor()
        settings = dict(dbcursor.execute("select key, value from server"))
        dbconn.close()
        self.lang = settings["language"]
        es = gettext.translation("cfs_connsupport", localedir="cfs-content/locale", languages=[self.lang], fallback=True)
        es.install()
        self.system_info = (settings['name'], settings['version'], 'cfs_master')
        self.required_client_version = 3
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
            for i in range(0, len(args)):
                args[i] = re.escape(args[i])
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
                    "select username, password, authlevel from auth"
                )
                for row in users:
                    if row[0] == username:
                        db_username = row[0]
                        db_password = row[1]
                        self.log.logger.debug(
                            _("Found user %s, password is %s.") % (username, db_password)
                        )
                        authlevel = row[2]
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
                try:
                    with open("./cfs-content/database/files/%s" % filename) as file:
                        if filename.find("../") != -1:
                            raise PermissionError(_("The client uses the '../' command"))
                        result = replace.replacer.replaceTag("blocked", file.read(), authlevel, "[hidden]")
                        self.send(self.gpkg.Message("Result", result))
                except (IsADirectoryError, FileNotFoundError):
                    self.send(self.gpkg.FileNotFound())
                except (PermissionError, NameError):
                    self.send(self.gpkg.BadRequest())
            elif args[0] == "user":
                if not len(args) >= 2:
                    self.send(self.gpkg.BadRequest())
                    continue
                if args[1] == "add":
                    if not len(args) == 4:
                        self.send(self.gpkg.BadRequest())
                        continue
                    if do_login is False:
                        self.send(self.gpkg.Message("What?!", "You must to login first."))
                        continue
                    if usertools.isAdmin(username) is False:
                        self.send(
                            self.gpkg.Forbidden(
                                "You are not an administrator, this command is not for you!"
                            )
                        )
                        continue
                    if usertools.isUserExists(args[2]) is True:
                        self.send(self.gpkg.BadRequest("Are you serious??"))
                        continue
                    if usertools.addUser(args[2], args[3]) is False:
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
                    if usertools.isUserExists(args[2]) is False:
                        self.send(self.gpkg.BadRequest("The server couldn\'t find the user."))
                        continue
                    if usertools.isAdmin(username) is False:
                        self.send(
                            self.gpkg.Forbidden(
                                "You are not an administrator, this command is not for you!"
                            )
                        )
                        continue
                    if usertools.removeUser(args[2]) is False:
                        self.send(self.gpkg.Message("Error", "Can\'t remove the user.", Code=500))
                    else:
                        self.send(self.gpkg.Message("Success", "Successfully removed the user."))
                elif args[1] == "passwd":
                    if do_login is False:
                        self.send(self.gpkg.Message("What?!", "You must to login first."))
                        continue
                    if len(args) == 4:
                        if usertools.isAdmin(username) is False:
                            self.send(
                                self.gpkg.Forbidden(
                                    "You are not an administrator, this command is not for you!"
                                )
                            )
                            continue
                        if usertools.passwd(args[2], args[3]) is False:
                            self.send(self.gpkg.Message("Error", "...", Code=500))
                            continue
                        else:
                            self.send(self.gpkg.Message("Success", "Successfully changed the password."))
                            continue
                    elif len(args) < 3:
                        self.send(self.gpkg.BadRequest())
                        continue
                    if usertools.passwd(username, args[2]) is False:
                        self.send(self.gpkg.Message("Error", "...", Code=500))
                        continue
                    else:
                        self.send(self.gpkg.Message("Success", "Successfully changed the password."))                        
    

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
                if usertools.isAdmin(username) is True:
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
