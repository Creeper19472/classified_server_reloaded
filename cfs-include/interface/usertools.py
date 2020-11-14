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


def add_user(username, password, authlevel=0, isadmin=0):
    dbconn = sqlite3.connect("./cfs-content/database/sqlite3.db")
    dbcursor = dbconn.cursor()
    userslist = dbcursor.execute("select username from auth")
    for row in userslist:
        if row[0] == username:
            return False
    dbcursor.execute(
        """insert into auth values('%s', '%s', %s, %s);""" % username,
        password,
        authlevel,
        isadmin,
    )
    dbconn.close()
    return True


def change_password(username, password):
    pass
