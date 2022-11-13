# functions to transfer story info btwn db and and front end

import sqlite3   #enable control of an sqlite database

DB_FILE="story.db"

# making a story
def create_story(name, text, user, time):
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()     
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", [name])
    print("hi")
    if not c.fetchone():
        c.execute(f"CREATE TABLE {name}('content' TEXT, 'contribution' TEXT, 'user' TEXT, 'time' TEXT);")
        c.execute(f"INSERT INTO {name} VALUES(?, ?, ?, ?);", (text, text, user, time))
        # creating the story also happens to be the first contribution
        #db.commit() 
        #db.close() 
        print("tru")
        return True 

    else:
        print("fals")
        return False
        # the story failed to create

def edit_story(name, text, user, time):
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()               
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", [name])
    # the story cannot be edited as it does not exist
    if not c.fetchone():  
        return False

    else:
        c.execute(f"SELECT content FROM {name};")
        all_text = c.fetchone()
        print(all_text)
        c.execute(f"INSERT INTO {name} VALUES(?, ?, ?, ?);", (all_text, text, user, time))
        db.commit() 
        db.close() 
        return True

create_story("fallPCS", "a long time ago we started APCS", "bwang", "11/12/22")
edit_story("fallPCS", "the teacher was named Mykolyk", "ylc", "11/12/22")