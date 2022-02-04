from flask_app import app
from flask import render_template, redirect,session,request, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/register', methods=['POST'])
def register():
    if User.validate(request.form) ==False:
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data={
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':pw_hash
        }
    user_id=User.save(data)
    session['logged_in_user']=user_id
    return redirect ('/success')

@app.route('/success')
def create_user():
    User.save(request.form)
    return render_template('success.html')

@app.route('/logged', method=['POST'])
def login():
    session['email']=request.form['email']
    