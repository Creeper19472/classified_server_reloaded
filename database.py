import sqlite3

dbconn = sqlite3.connect("./cfs-content/database/sqlite3.db")
dbcursor = dbconn.cursor()
### END SQLITE3 ###

contents = dbcursor.execute("select title, content, protectionlevel from cfs_file")
for row in contents:
    print("title = %s" % row[0])
    print("content = %s" % row[1])
    print("level = %s" % row[2])
