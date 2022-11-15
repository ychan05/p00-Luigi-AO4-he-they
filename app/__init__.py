from flask import Flask, render_template, session, request, redirect
from login_db import signup, verify
from story_db import get_latest, get_titles, create_story, edit_story, get_story, get_ids, unique_ids, all_titles

app = Flask(__name__)

app.secret_key = "HI" # dummy key

@app.route('/', methods=['GET'])
def login():
  if 'username' in session:
    return redirect('/home') # go to displ homepage if has cookies
  return render_template('login.html')


@app.route('/register', methods=['GET'])
def register():
  if 'username' in session:
    return redirect('/home') # go to displ homepage if has cookies
  return render_template('registration.html')

# verify username not in use
@app.route('/verify', methods=['GET', 'POST'])
def make_account():
  if request.method != 'POST':
    return redirect('/')
  
  if not signup(request.form['username'], request.form['password']):
    if not request.form['password']:
      return render_template('registration.html', status='enter a password')
    return render_template('registration.html', status='username in use')
  
  session['username'] = request.form['username']
  return redirect('/home')

# authenticate login
@app.route('/auth', methods=['GET', 'POST'])
def authenticate():
  if request.method != 'POST':
    return redirect('/')

  # check if user in db
  if not verify(request.form['username'], request.form['password']): 
    return render_template('login.html', status='Incorrect login info')
  
  session['username'] = request.form['username']
  return redirect('/home')

# homepage. displays stories contributed to
@app.route('/home', methods=['GET'])
def home():
  if not session:
    return redirect('/')
  titles = get_titles(session['username'])
  stories = get_latest(session['username'])
  return render_template('homepage.html', name=session['username'], len = len(titles), titles=titles, stories=stories)

# view a story
@app.route('/view/<story_id>', methods=['GET'])
def view(story_id):
  story = get_story(story_id)[0]
  id_list = []
  for tupl in get_ids(session['username']):
    id_list.append(tupl[0])
  if story[0] in id_list:
    return render_template('story.html', name=story[1], user_id=story[4], content=story[2])
  else:
    return redirect('/edit/' + str(story_id))

# html page for making new story
@app.route('/create', methods=['GET'])
def create():
  return render_template('create.html')

# add new story to db
@app.route('/make', methods=['GET', 'POST'])
def make():
  if not request.form['title'] or request.form['content']:
    return redirect('/create')
  story_id = create_story(request.form['title'], request.form['content'], session['username'] )
  return redirect('/view/' + str(story_id))

# html page for editing story
@app.route('/edit/<story_id>', methods=['GET'])
def edit(story_id):
  for i in get_ids(session['username']):
    if int(story_id) in i:
      return redirect('/view/' + str(story_id))
  story = get_story(story_id)[0]
  return render_template('edit.html', name=story[1], user_id=story[4], content=story[3], story_id=story[0], story_path="/add/"+str(story[0]))

# add edited story to db
@app.route('/add/<story_id>', methods=['GET', 'POST'])
def add(story_id):
  if not request.form['content']:
    return redirect('/edit/' + str(story_id))
  id = edit_story(story_id, request.form['content'], session['username'] )
  return redirect('/view/' + str(story_id))

# browse all stories  
@app.route('/browse', methods=['GET'])
def browse():
  ids = unique_ids()
  return render_template('browse.html', contributed=get_ids(session['username']), len=len(ids),ids=ids, titles=all_titles())
# logout
@app.route('/logout')
def logout():
  session.pop('username')
  return redirect('/')
  
if __name__ == '__main__':
  app.debug = True
  app.run()
