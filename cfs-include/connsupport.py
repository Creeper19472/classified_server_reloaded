import socket, sys, sqlite3
import gpkg
import threading

from letscrypt import RSA, BLOWFISH
import common.logkit as logkit
import interface.usertools as usertools
import filedetect


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
        self.conn.send(self.rsa_fkey)  # Send RSA Public Key
        self.bf_key = RSA.Decrypt(self.conn.recv(8192), self.rsa_ekey)
        self.log.logger.debug(
            "Encryption enabled successfully. Blowfish key: %s." % self.bf_key
        )
        try:
            self.IOThread()
        except ConnectionResetError:
            self.log.logger.info(
                "Connection Reset %s. Closing %s." % (self.addr, self.thread_name)
            )
            sys.exit()
        except SystemExit:
            self.log.logger.info(
                "Disconnected from %s. Closing %s." % (self.addr, self.thread_name)
            )
            sys.exit()
        except:
            self.log.logger.fatal(
                "In %s, one (or more) exceptions were caught:" % self.thread_name,
                exc_info=True,
            )
            self.log.logger.fatal(
                "Due to the above exception, this thread cannot continue to run."
            )
            sys.exit()

    def send(self, msg):
        self.log.logger.debug("Sending message %s." % msg)
        bytes_msg = BLOWFISH.Encrypt(msg, self.bf_key)
        self.conn.send(bytes_msg)

    def recv(self, limit=8192):
        cipher_bytes_text = self.conn.recv(limit)
        text = BLOWFISH.Decrypt(cipher_bytes_text, self.bf_key)
        self.log.logger.debug("Received message %s." % text)
        return text

    def IOThread(self):
        self.send(gpkg.gpkg.Message("Success", "OK"))
        username = None  # Flake8 fix
        do_login = False
        while True:
            recv = self.recv()
            splitrecv = recv["Message"].split()
            splitrecv[0] = splitrecv[0].lower()
            if splitrecv[0] == "login":
                if not len(splitrecv) == 3:
                    self.send(gpkg.gpkg.BadRequest())
                    continue
                if do_login == True:
                    self.log.logger.info(
                        "%s: User %s is already logged in." % (self.addr, username)
                    )
                    self.send(
                        gpkg.gpkg.Message("Already logged in", "Please logout first.")
                    )
                    continue
                username = splitrecv[1]
                db_username = None
                password = splitrecv[2]
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
                            "Found user %s, password is %s." % (username, db_password)
                        )
                        authlevel = row[2]
                        break
                dbconn.close()
                if db_username == None:
                    self.log.logger.warn(
                        "%s; Username is incorrect. Login failed." % self.addr
                    )
                    self.send(
                        gpkg.gpkg.Message(
                            "Login FAILED", "Incorrect username or password.", 400
                        )
                    )
                    continue
                if password == db_password:
                    self.log.logger.info(
                        "%s: User %s's password is match. Can login."
                        % (self.addr, username)
                    )
                    self.send(gpkg.gpkg.Message("SUCCESS", "Login Success!"))
                    do_login = True
                else:
                    self.log.logger.warn(
                        "%s: User %s's password is incorrect. Login failed."
                        % (self.addr, username)
                    )
                    self.send(
                        gpkg.gpkg.Message(
                            "Login FAILED", "Incorrect username or password.", 400
                        )
                    )
            elif splitrecv[0] == "getfile":
                if not len(splitrecv) == 2:
                    self.send(gpkg.gpkg.BadRequest())
                    continue
                try:
                    if not do_login == True:
                        raise PermissionError
                except PermissionError:
                    self.send(gpkg.gpkg.Forbidden("You must to login first."))
                    continue
                filename = splitrecv[1]
                try:
                    with open("./cfs-content/database/files/%s" % filename) as file:
                        if filename.find("../") != -1:
                            raise PermissionError("The client uses the '../' command")
                        result = filedetect.Blocked.ReplaceBlock(file.read(), authlevel)
                        self.send(gpkg.gpkg.Message("Result", result))
                except (IsADirectoryError, FileNotFoundError):
                    self.send(gpkg.gpkg.FileNotFound())
                except (PermissionError, NameError):
                    self.send(gpkg.gpkg.BadRequest())
            elif splitrecv[0] == "logout":
                if do_login is False:
                    self.send(gpkg.gpkg.Message("What?!", "You must to login first."))
                    continue
                do_login = False
                self.send(gpkg.gpkg.Message("OK", "Successfully logged out."))
            elif splitrecv[0] == "stop":
                if do_login is False:
                    self.send(gpkg.gpkg.Message("What?!", "You must to login first."))
                    continue
                if usertools.isAdmin(username) is True:
                    self.log.logger.info("Server shutdown has been scheduled!")
                    self.send(
                        gpkg.gpkg.Message(
                            "Scheduled", "Server shutdown has been scheduled!"
                        )
                    )
                else:
                    self.send(
                        gpkg.gpkg.Forbidden(
                            "You are not an administrator, this command is not for you!"
                        )
                    )
            elif splitrecv[0] == "disconnect":
                self.conn.close()
                sys.exit()
            else:
                self.send(gpkg.gpkg.BadRequest())
