from flask import Flask, render_template, session, request, redirect
from login_db import signup, verify

app = Flask(__name__)

# testing purposes
user = 'frodo' 
passwd = 'baggins'

app.secret_key = "HI" # dummy key

@app.route('/', methods=['GET'])
def login():
  if 'username' in session:
    return redirect('/home') # displ homepage if has cookies
  return render_template('login.html')

@app.route('/auth', methods=['POST'])
def authenticate():
  # will check if info is in db later on
  if request.form['username'] != user and request.form['username'] != passwd: 
    return render_template('login.html', status='Incorrect login info')
  
  session['username'] = request.form['username']
  return redirect('/home')

@app.route('/home', methods=['GET'])
def home():
  return render_template('homepage.html')

@app.route('/logout')
def logout():
  session.pop('username')
  return redirect('/')
  
if __name__ == '__main__':
  app.debug = True
  app.run()
