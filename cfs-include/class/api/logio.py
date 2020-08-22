import sqlite3

class logIO():
    def __init__(self):
        dbconn = sqlite3.connect('./cfs-content/database/sqlite3.db')
        dbcursor = dbconn.cursor()
        self.settings = dict(dbcursor.execute('select key, value from server'))
        self.users = dict(dbcursor.execute('select username, password, authlevel from auth'))
        dbconn.close()

    def flushall(self):
        self.__init__()

    def log_in(self, username, password):
        pass
        
