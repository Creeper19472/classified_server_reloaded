import sys, sqlite3


class usertools:
    def __init__(self, db_prefix):
        self.db_prefix = db_prefix
        
    def isAdmin(self, username):
        db_username = None
        dbconn = sqlite3.connect("./cfs-content/database/sqlite3.db")
        dbcursor = dbconn.cursor()
        userslist = dbcursor.execute("select username, role from {0}auth".format(self.db_prefix))
        for row in userslist:
            if row[0] == username:
                db_username = row[0]
                role = row[1]
                break
        dbconn.close()
        if db_username == None:
            return False
        if 'admin' in role:
            return True
        else:
            return False

    def isUserExists(self, username):
        dbconn = sqlite3.connect("./cfs-content/database/sqlite3.db")
        dbcursor = dbconn.cursor()
        userslist = dbcursor.execute("select username from {0}auth".format(self.db_prefix))
        for row in userslist:
            if row[0] == username:
                return True
        return False

    def addUser(self, username, password, authlevel=0, isadmin=0):
        dbconn = sqlite3.connect("./cfs-content/database/sqlite3.db")
        dbcursor = dbconn.cursor()
        userslist = dbcursor.execute("select username from {0}auth".format(self.db_prefix))
        for row in userslist:
            if row[0] == username:
                return False
        dbcursor.execute(
            """insert into {0}auth values(?, ?, ?, ?);""".format(self.db_prefix), (username, password, authlevel, isadmin,))
        dbconn.commit()
        dbconn.close()
        return True

    def removeUser(self, username):
        dbconn = sqlite3.connect("./cfs-content/database/sqlite3.db")
        dbcursor = dbconn.cursor()
        userslist = dbcursor.execute("select username, authlevel from {0}auth".format(self.db_prefix))
        for row in userslist:
            if row[0] == username:
                if row[1] == 1:
                    return False
                else:
                    break
        dbcursor.execute("delete from {0}auth where username = ?".format(self.db_prefix), (username,))
        dbconn.commit()
        dbconn.close()
        return True
        
    def passwd(self, username, password):
        db_username = None
        dbconn = sqlite3.connect("./cfs-content/database/sqlite3.db")
        dbcursor = dbconn.cursor()
        userslist = dbcursor.execute("select username from {0}auth".format(self.db_prefix))
        for row in userslist:
            if row[0] == username:
                db_username = row[0]
                break
        if db_username == None:
            return False
        dbcursor.execute("update {0}auth set password = ? where username = ?".format(self.db_prefix), (password, username,))
        dbconn.commit()
        dbconn.close()
        return True
    
