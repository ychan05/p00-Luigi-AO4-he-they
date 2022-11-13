# functions to transfer story info btwn db and and front end

import sqlite3   #enable control of an sqlite database

DB_FILE="story.db"

def create_table(c):
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='stories';")
    if not c.fetchone():
        c.execute("CREATE TABLE stories('id' INT, 'title' TEXT, 'story' TEXT, 'latest' TEXT, 'contributor' TEXT);")

# making a story
def create_story(title, text, user):
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()               
    create_table(c)
    
    c.execute("SELECT COUNT(DISTINCT id) FROM stories;")
    id = c.fetchone()[0] + 1# assign id by tally
    c.execute("INSERT INTO stories VALUES(?, ?, ?, ?, ?);", (id, title, text, text, user))
    db.commit() 
    db.close()  

# edit story
# prereq: story exist
def edit_story(id, text, user):
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()               

    c.execute("SELECT story FROM stories WHERE id = ? ORDER BY story DESC LIMIT 1;", str(id))
    story = c.fetchone()[0] + ' ' + text 
    title =  c.execute("SELECT title FROM stories WHERE id = ?;", str(id)).fetchone()[0]
    c.execute("INSERT INTO stories VALUES(?, ?, ?, ?, ?);", (str(id), title, story, text, user))
    db.commit() 
    db.close()  

