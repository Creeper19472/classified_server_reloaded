# -*- coding: utf-8 -*-

import socket, sys, sqlite3, gettext, json, re, hashlib
import threading

sys.path.append('cfs-include/')

if __name__ == '__main__':
    sys.exit()

from slib.docrypt import RSA, BLOWFISH
import slib.generator.socketpkg as gpkg
import slib.parser.replace as replace
import tool.logkit as logkit
import interface.usertools as usertools

class Users(object):
    def __init__(self, username, **kwargs):
        self.username = str(username)
        print(kwargs)
        dbconn = sqlite3.connect("./cfs-content/database/sqlite3.db")
        dbcursor = dbconn.cursor()
        users = dbcursor.execute(
            "select username, password, userdata from {0}auth".format(kwargs['db_prefix'])
        )
        self.user_exists = False
        self.password = None
        self.userdata = None
        for row in users:
            if row[0] == self.username:
                self.password = row[1]
                self.userdata = row[2]
                self.log.logger.debug(
                    _("Found user {0}, password: {1}, userdata: {2}").format(row[0], row[1], row[2])
                )
                self.user_exists = True
                break
        dbconn.close()
        if self.user_exists == True:
            self.access_level = int(self.userdata['access_level'])
            self.role = self.userdata['role']

    def login(self, reqpass):
        if self.user_exists != True:
            self.online = False
        hs = hashlib.md5(self.password[1].encode())
        hs.update(reqpass.encode())
        req_return = hs.hexdigest()
        if req_return == self.password[0]:
            self.online = True
        else:
            self.online = False

    def logout(self):
        self.online = False

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
        self.system_info = (kwargs['display_name'], '0.4.x', 'cfs_master')
        self.run()

    def run(self):
        es = gettext.translation("cfs_connsupport", localedir="cfs-content/locale", languages=[self.lang], fallback=True)
        es.install()
        self.required_client_version = 8
        self.gpkg = gpkg.GeneratePackage(self.required_client_version, self.system_info)
        frecv = self.conn.recv(1024)
        self.log.logger.debug('client request data: %s' % frecv.decode())
        if ('HTTP/1.1' or "HTTP/2.0") in frecv.decode():
            response_start_line = "HTTP/1.1 200 OK\r\n"
            response_headers = "Server: Classified Server\r\n"
            response_body = _("<p>This server does not support http.</p>")
            response = response_start_line + response_headers + "\r\n" + response_body
            self.conn.send(bytes(response, encoding='utf-8'))
            self.log.logger.info(_('Disconnecting from %s: HTTP requests. Closing %s.') \
                                 % (self.addr, self.thread_name))
            self.conn.close()
            sys.exit()
        elif 'Non-HTTP/1.0 200' not in frecv.decode():
            self.log.logger.info(_('Disconnecting from %s: Unknown request. Closing %s.') \
                                 % (self.addr, self.thread_name))
            self.conn.close()
            sys.exit()
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
        self.log.logger.debug(_("Send: %s") % msg)
        bytes_msg = BLOWFISH.Encrypt(msg, self.bf_key)
        self.conn.send(bytes_msg)

    def recv(self, limit=8192):
        cipher_bytes_text = self.conn.recv(limit)
        text = BLOWFISH.Decrypt(cipher_bytes_text, self.bf_key)
        self.log.logger.debug(_("Get: %s.") % text)
        return text

    def IOThread(self):
        self.send(self.gpkg.Message("Success", "OK"))
        username = None  # Flake8 fix
        do_login = False
        while True:
            recv = self.recv()
            if recv['Type'] != "client/request":
                self.send(self.gpkg.BadRequest())
                continue
            args = recv['Data']
            cmdname = args['cmd']
            try:
                if cmdname == "login":
                    if 'UserObject' in dir(): # 检查UserObject对象是否被定义
                        if UserObject.online == True: # 若用户已上线则不操作
                            self.log.logger.info(
                                _("%s: User %s is already logged in.") % (self.addr, username)
                            )
                            self.send(
                                self.gpkg.Message("Already logged in", "Please logout first.")
                            )
                            continue
                    UserObject = Users(args['username'], db_prefix=self.db_prefix) # 初始化UserObject, 用**kwargs的方式给数据库前缀参数
                    UserObject.login(args['password'])
                    if UserObject.online == False:
                        if UserObject.user_exists != True:
                            self.log.logger.warn(
                                _("%s: Username is incorrect. Login failed.") % self.addr
                            )
                            self.send(
                                self.gpkg.Message(
                                    "Login FAILED", "Incorrect username or password.", 400
                                )
                            )
                        else:
                            self.log.logger.warn(
                                _("%s: User %s's password is incorrect. Login failed.") % (self.addr, username)
                            )
                            self.send(
                                self.gpkg.Message(
                                    "Login FAILED", "Incorrect username or password.", 400
                                )
                            )
                    else:
                        self.log.logger.info(
                            _("%s: User %s's password is match. Can login.")
                            % (self.addr, username)
                        )
                        self.send(self.gpkg.Message("SUCCESS", "Login Success!"))
                elif cmdname == "file":
                    try:
                        if not do_login == True:
                            raise PermissionError
                    except PermissionError:
                        self.send(self.gpkg.Forbidden("You must login first."))
                        continue
                    if args['action'] == 'get': # define get function
                        fileid = args['fileid']
                        dbconn = sqlite3.connect("./cfs-content/database/sqlite3.db")
                        dbcursor = dbconn.cursor()
                        dbfiles = dbcursor.execute(
                            "select id, content, author, protectionlevel from {0}file".format(self.db_prefix)
                        )
                        targetid = None
                        for row in dbfiles:
                            if row[0] == fileid:
                                targetid = row[0] # set name instead None
                                content = row[1]
                                author = row[2]
                                protectionlevel = int(row[3]) # patch if type != int
                        dbconn.close()
                        if targetid == None:
                            self.send(self.gpkg.FileNotFound('Ooops! File not found. Please check your input and try again.'))
                            continue
                        if protectionlevel > authlevel: # execute if the user is not enough to do that
                            if author != username: # deny if author != username
                                self.send(self.gpkg.Forbidden\
                                          (_("The security level required to request the document is higher than the current user level")))
                                continue
                        if args.get('gettype', None) == 'result' or args.get('gettype', None) == None:
                            result = replace.replacer.replaceTag("blocked", content, authlevel, self.ptext)
                        elif args['gettype'] == 'source':
                            if author == username:
                                result = content
                            elif 'admin' and 'editor' not in current_role:
                                self.send(self.gpkg.Forbidden(_("You are not allowed to modify this file")))
                                continue
                            else:
                                result = content
                        else:
                            raise ValueError('Invaild operation')
                        self.send(self.gpkg.Message("Result", result))
                    elif args['action'] == 'post':
                        fileid = args['fileid']
                        filedata = args['filedata']
                        ut = usertools.usertools(self.db_prefix)
                        dbconn = sqlite3.connect("./cfs-content/database/sqlite3.db")
                        dbcursor = dbconn.cursor()
                        files = dbcursor.execute(
                            "select id, protectionlevel from {0}file".format(self.db_prefix)
                        )
                        targetname = None
                        for row in files:
                            if row[0] == fileid:
                                targetid = row[0] # set name instead None
                                protectionlevel = int(row[1])
                        table_name = f"{self.db_prefix}file"
                        if targetid == None:
                            if 'editor' in current_role or ut.isAdmin(username):
                                dbcursor.execute(f"INSERT INTO {table_name} values(?, ?, ?, ?);", \
                                                 (fileid, '', -1, username))
                                protectionlevel = -1
                            else: # send forbidden response
                                self.send(self.gpkg.Forbidden())
                                continue
                        if ut.isAdmin(username) or 'editor' in current_role:
                            content = args['content']
                            dbcursor.execute(f"UPDATE {table_name} SET content=?, authlevel=? WHERE fileid=?;", \
                                             (filedata['content'], authlevel, fileid,))
                            dbconn.commit()
                            self.send(self.gpkg.Message('OK', 'Update success!'))
                        else:
                            self.send(self.gpkg.Forbidden())
                        dbconn.close()
                    elif args['action'] == 'rename':
                        pass
                    else:
                        self.send(self.gpkg.BadRequest())
                elif cmdname == "user":
                    ut = usertools.usertools(self.db_prefix)
                    if args['action'] == "add":
                        if do_login is False:
                            self.send(self.gpkg.Message("What?!", "You must login first."))
                            continue
                        if ut.isAdmin(username) is False:
                            self.log.logger.warn(_("%s: User %s tried to add a new user %s, but did not have the right to do so.") % (self.addr, username, args[2]))
                            self.send(
                                self.gpkg.Forbidden(
                                    "You are not an administrator, this command is not for you!"
                                )
                            )
                            continue
                        if ut.isUserExists(args['username']) is True:
                            self.send(self.gpkg.BadRequest("Are you serious??"))
                            continue
                        if ut.addUser(args['username'], args['password']) is False:
                            self.send(self.gpkg.Message("Error", "...", Code=500))
                        else:
                            self.send(self.gpkg.Message("Success", "Successfully added a new user."))
                        continue
                    elif args['action'] == "remove":
                        if do_login is False:
                            self.send(self.gpkg.Message("What?!", "You must login first."))
                            continue
                        if ut.isUserExists(args['username']) is False:
                            self.send(self.gpkg.BadRequest("The server couldn\'t find the user."))
                            continue
                        if ut.isAdmin(username) is False:
                            self.send(
                                self.gpkg.Forbidden(
                                    "You are not an administrator, this command is not for you!"
                                )
                            )
                            continue
                        if ut.removeUser(args['username']) is False:
                            self.send(self.gpkg.Message("Error", "Can\'t remove the user.", Code=500))
                        else:
                            self.send(self.gpkg.Message("Success", "Successfully removed the user."))
                    elif args['action'] == "passwd":
                        if do_login is False:
                            self.send(self.gpkg.Message("What?!", "You must login first."))
                            continue
                        username_exists = True
                        try:
                            assert args['username'] != None
                        except (AssertionError, NameError):
                            username_exists = False
                        if username_exists == True:
                            if ut.isAdmin(username) is False:
                                self.send(
                                    self.gpkg.Forbidden(
                                        "You are not an administrator, this command is not for you!"
                                    )
                                )
                                continue
                            if ut.passwd(args['username'], args['password']) is False:
                                self.send(self.gpkg.Message("Error", "...", Code=500))
                                continue
                            else:
                                self.send(self.gpkg.Message("Success", "Successfully changed the password."))
                                continue
                        else:
                            if ut.passwd(username, args[2]) is False:
                                self.send(self.gpkg.Message("Error", "...", Code=500))
                                continue
                            else:
                                self.send(self.gpkg.Message("Success", "Successfully changed the password."))
                    else:
                        self.send(self.gpkg.BadRequest())
        

                elif cmdname == "logout":
                    if do_login is False:
                        self.send(self.gpkg.Message("What?!", "You must login first."))
                        continue
                    do_login = False
                    self.log.logger.info(_('%s: User %s logged out.') % (self.addr, username))
                    self.send(self.gpkg.Message("OK", "Successfully logged out."))
                elif cmdname == "dir":
                    dbconn = sqlite3.connect("./cfs-content/database/sqlite3.db")
                    dbcursor = dbconn.cursor()
                    dbfiles = dbcursor.execute(
                        "select id, title, protectionlevel from {0}file".format(self.db_prefix)
                    )
                    filelist = {}
                    for row in dbfiles:
                        filelist[row[0]] = (row[1], row[2])
                    self.send(self.gpkg.Message("Result", filelist)) # send filelist
                elif cmdname == "disconnect":
                    self.conn.close()
                    sys.exit()
                else:
                    self.send(self.gpkg.BadRequest())
            except (NameError, ValueError):
                self.send(self.gpkg.BadRequest())
                continue
                
