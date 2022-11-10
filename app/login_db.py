# functions to transfer login info btwn db and and front end

import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O



DB_FILE="login.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

# create table if table DNE
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='login';")
if c.fetchone() == None:
    c.execute("CREATE TABLE login('username' TEXT, 'password' TEXT)")

# if username already registered return false. Add login to DB otherwise
def signup(username, password):
    c.execute("SELECT username FROM login where username = ?;", [username]) # 2nd param need to be sequences
    if c.fetchone() == None:
        c.execute("INSERT INTO login VALUES(?, ?)", (username, password))
        return True
    return False
    


def verify (username, password):
    c.execute("SELECT password FROM login where username = ?;", [username])
    tmp = c.fetchone()
    if  tmp == None: # fetch all returns list of tuples
        return False
    elif tmp[0] == password:
        return True
    return False;

db.commit() #save changes
db.close()  #close database
