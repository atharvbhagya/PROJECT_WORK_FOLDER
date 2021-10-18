import re
from flask import Blueprint, render_template, url_for, redirect, request,flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from functools import wraps


auth= Blueprint('auth', __name__)
db= mysql.connector.connect(
    host="localhost",
    user="root",
    password="aaa",
    database="atharvbase",
 
   )
dbcur= db.cursor()

# wrap to authenticate the user
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Access Denied ! Please login')
            return redirect(url_for('auth.login'))
    return wrap




@auth.route('/login', methods=['POST','GET'])
def login():
    if request.method=='POST':
     username= request.form.get('username')
     password= request.form.get('password')
     sql3='select username,password from Users where username=(%s)'
     dbcur.execute(sql3,(username,))
     row= dbcur.fetchone()
     if len(row)>0 :
         if check_password_hash(row[1],password):
             session['logged_in'] = True
             session['username'] = username
             flash('You are successfully logged in !')
             return redirect(url_for('main.profile',username=username))
         else:
             flash('Your password is incorrect !')
             return redirect(url_for('auth.login'))    
     else:
         flash('This userame does not exist !')
         return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth.route('/signup', methods=['POST','GET'])
def signup():
    if request.method=='POST':
        username= request.form.get('username')
        password= request.form.get('password')
        email= request.form.get('email')

        sql1='select * from Users where username=(%s) and email=(%s)'
        dbcur.execute(sql1,(username,email))
        existing_user= dbcur.fetchall()


        if  len(existing_user)>0 :
            flash('This username and/or email already exists ! Choose different Username and/or email')
            return redirect(url_for('auth.signup'))
        password_entry=generate_password_hash(password,method='sha256')
        sql2='insert into Users(username,password,email) values(%s,%s,%s)'
        dbcur.execute(sql2,(username,password_entry,email))
        db.commit()

        return redirect(url_for('auth.login'))

    return render_template('signup.html')    

@auth.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('auth.login'))


