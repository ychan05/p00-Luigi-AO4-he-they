from flask import Flask, render_template, session, request, redirect
from login_db import signup, verify
from story_db import get_latest, get_titles, create_story, edit_story

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

@app.route('/home', methods=['GET'])
def home():
  if not session:
    return redirect('/')
  titles = get_titles(session['username'])
  stories = get_latest(session['username'])
  return render_template('homepage.html', name=session['username'], len = len(titles), titles=titles, stories=stories)


@app.route('/logout')
def logout():
  session.pop('username')
  return redirect('/')
  
if __name__ == '__main__':
  app.debug = True
  app.run()
