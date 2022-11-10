# functions to transfer login info btwn db and and front end

import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O



DB_FILE="login.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

#==========================================================
if db == None:
    c.execute(f"CREATE TABLE login('username' TEXT, 'password' TEXT)")
def signup (username, password):
    if c.execute(f"SELECT username FROM login where username == '{username}';") == None:
        c.execute(f"INSERT INTO login('{username}', '{password}')")
        return True
    else:
        return False
    


def verify (username, password):
    if c.execute(f"SELECT password FROM login where username == '{username}';") == password:
        print(c.execute(f"SELECT password FROM login where username == '{username}';"))
        return True
    return False


#==========================================================

signup("aaa", "aaaa")
signup("bbb", "bbbb")
print(verify("aaa", "aaa"))
print(verify("aaa", "aaaa"))

db.commit() #save changes
db.close()  #close database
