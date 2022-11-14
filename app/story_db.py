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
    return id

# edit story
# prereq: story exist
def edit_story(id, text, user):
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()               

    c.execute("SELECT story FROM stories WHERE id = ? ORDER BY story DESC LIMIT 1;", [str(id)])
    story = c.fetchone()[0] + ' ' + text 
    title =  c.execute("SELECT title FROM stories WHERE id = ?;", [str(id)]).fetchone()[0]
    c.execute("INSERT INTO stories VALUES(?, ?, ?, ?, ?);", (str(id), title, story, text, user))
    db.commit() 
    db.close()  

# get ids of stories a user has contributed to
def get_ids(user):
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()
    return c.execute("SELECT id FROM stories WHERE contributor = ?", [user]).fetchall()
    db.close()

# get titles of stories a user has contributed to
def get_titles(user):
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()
    return c.execute("SELECT title FROM stories WHERE contributor = ?", [user]).fetchall()
    db.close()

# get latest ver. of stories user has contributed to 
def get_latest(user):
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()
    ids = get_ids(user)
    stories = []
    for i in range(0, len(ids)):
        tmp = c.execute("SELECT story FROM stories WHERE id = ? ORDER BY story DESC LIMIT 1;", [str(ids[i][0])]).fetchone()[0]
        stories.append(tmp)
    return stories

# get all info associated with a story
def get_story(id):
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()
    c.execute("SELECT * FROM stories WHERE id = ? ORDER BY story DESC LIMIT 1;", [id])
    temp = c.fetchall()
    db.close()
    return temp

# get ids of all stories
def unique_ids():
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()
    c.execute("SELECT DISTINCT id FROM stories;")
    return c.fetchall()

def all_titles():
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()
    ids = unique_ids()
    titles = []
    for i in range(0, len(ids)):
        tmp = c.execute("SELECT DISTINCT title FROM stories WHERE id = ?", [str(ids[i][0])]).fetchone()[0]
        titles.append(tmp)
    db.close()
    return titles