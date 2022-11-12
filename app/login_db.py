# functions to transfer login info btwn db and and front end

import sqlite3   #enable control of an sqlite database

DB_FILE="login.db"

# create table if table DNE
def create_table(c):
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='login';")
    if not c.fetchone():
        c.execute("CREATE TABLE login('username' TEXT, 'password' TEXT)")

# if username already registered return false. Add login to DB otherwise
def signup(username, password):
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()               
    create_table(c)
    
    # check if username is unique
    c.execute("SELECT username FROM login where username = ?;", [username]) # 2nd param need to be a sequence
    if not c.fetchone() and password:
        c.execute("INSERT INTO login VALUES(?, ?)", (username, password))
        db.commit() 
        db.close()  
        return True

    db.close()  
    return False
    
# verify if user exists in db
def verify (username, password):
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()               
    create_table(c)

    c.execute("SELECT password FROM login where username = ?;", [username])
    tmp = c.fetchone()
    if not tmp: 
        return False
    elif tmp[0] == password:
        db.close()  
        return True

    db.close()  
    return False;


