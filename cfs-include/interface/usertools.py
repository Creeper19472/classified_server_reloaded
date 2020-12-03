import sys, sqlite3


def isAdmin(username):
    db_username = None
    dbconn = sqlite3.connect("./cfs-content/database/sqlite3.db")
    dbcursor = dbconn.cursor()
    userslist = dbcursor.execute("select username, isadmin from auth")
    for row in userslist:
        if row[0] == username:
            db_username = row[0]
            isadmin = row[1]
            break
    dbconn.close()
    if db_username == None:
        return False
    if isadmin == 1:
        return True
    else:
        return False


def isUserExists(username):
    dbconn = sqlite3.connect("./cfs-content/database/sqlite3.db")
    dbcursor = dbconn.cursor()
    userslist = dbcursor.execute("select username from auth")
    for row in userslist:
        if row[0] == username:
            return True
    return False

def addUser(username, password, authlevel=0, isadmin=0):
    dbconn = sqlite3.connect("./cfs-content/database/sqlite3.db")
    dbcursor = dbconn.cursor()
    userslist = dbcursor.execute("select username from auth")
    for row in userslist:
        if row[0] == username:
            return False
    dbcursor.execute(
        """insert into auth values(?, ?, ?, ?);""", (username, password, authlevel, isadmin,))
    dbconn.commit()
    dbconn.close()
    return True

def removeUser(username):
    dbconn = sqlite3.connect("./cfs-content/database/sqlite3.db")
    dbcursor = dbconn.cursor()
    userslist = dbcursor.execute("select username, isadmin from auth")
    for row in userslist:
        if row[0] == username:
            if row[1] == 1:
                return False
            else:
                break
    dbcursor.execute("delete from auth where username = ?", (username,))
    dbconn.commit()
    dbconn.close()
    return True
    
def passwd(username, password):
    db_username = None
    dbconn = sqlite3.connect("./cfs-content/database/sqlite3.db")
    dbcursor = dbconn.cursor()
    userslist = dbcursor.execute("select username from auth")
    for row in userslist:
        if row[0] == username:
            db_username = row[0]
            break
    if db_username == None:
        return False
    dbcursor.execute("update auth set password = ? where username = ?", (password, username,))
    dbconn.commit()
    dbconn.close()
    return True
    
