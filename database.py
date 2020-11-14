import sqlite3

dbconn = sqlite3.connect("./cfs-content/database/sqlite3.db")
dbcursor = dbconn.cursor()
### END SQLITE3 ###

settings = dict(dbcursor.execute("select key, value from server"))
print(settings)
for row in settings:
    print("Key = %s" % row[0])
    print("Value = %s" % row[1])
