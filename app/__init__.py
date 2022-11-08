from flask import Flask, render_template, session, request, redirect

app = Flask(__name__)

app.secret_key = "HI" # dummy key

@app.route('/', methods=['GET'])
def login():
  if 'username' in session:
    return redirect('/home') # displ homepage if has cookies
  return render_template('login.html')

@app.route('/auth', methods=['POST'])
def authenticate():
  
if __name__ == '__main__':
  app.debug = True
  app.run()
