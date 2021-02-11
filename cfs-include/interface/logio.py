import sqlite3, sys

sys.path.append('../common')
import logkit


class logIO():
    def __init__(self, call_name, username):
        self.username = None
        self.do_login = False
        self.log = logkit.log(logname='Core.Threads.%s.LogIn/Out' % call_name, filepath='./cfs-content/log/threads.log')
        dbconn = sqlite3.connect('./cfs-content/database/sqlite3.db')
        dbcursor = dbconn.cursor()
        users = dbcursor.execute('select username, password, authlevel from auth')
        for row in users:
            if row[0] == username:
                self.username = username
                self.password = row[1]
                self.log.logger.debug('Found user %s, password is %s.' % (self.username, self.password))
                self.authlevel = row[2]
                break
        dbconn.close()

    def flushall(self):
        if not self.do_login == False:
            dbconn = sqlite3.connect('./cfs-content/database/sqlite3.db')
            dbcursor = dbconn.cursor()
            dbcursor.execute('insert into auth %s %s %s' % (self.username, self.password, self.authlevel))
            dbconn.close()
        self.__init__()

    def log_in(self, password):
        if self.do_login == True:
            return -1
        if bool(self.username) is False:
            return 2
        if password == self.password:
            self.do_login = True
            return 0
        else:
            return 1

    def change_password(self, old_password, password):
        if self.do_login == False:
            return False
        if not old_password == password:
            return False
        self.password = password
        self.flushall()
