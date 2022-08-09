import re
from flask import Flask, request
from datetime import timedelta
from flask import render_template, session, redirect, url_for
import sqlite3
import os
import hashlib



app = Flask(__name__)
app.secret_key = "lethanhdat"
dirname = os.getcwd()

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', result=username, success="")
    else:
        return render_template('login.html',
        error="",
        success="")

    
@app.route('/login')
def get_login():
    return redirect(url_for('index'))
    
@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('index'))

@app.route('/', methods=['POST'])
def login():
   username = request.form['username']
   password = request.form['password']
   passwordhash = hashlib.md5(password.encode()).hexdigest()
   session['username'] = username
   connection = sqlite3.connect(dirname + '\data.db')
   cursor = connection.cursor()
   query = "SELECT username FROM user WHERE username = '{name}' AND password = '{passw}'".format(name = username, passw = passwordhash)
   cursor.execute(query)
   result = cursor.fetchone()
   connection.commit()
   if result != None:
        return render_template('index.html', result=result[0], success="Đăng nhập thành công!")
   else:
        return render_template('login.html', error="Sai tài khoản hoặc mật khẩu")


@app.route('/register', methods=['GET'])
def get_register():
    return render_template('register.html', error="")


@app.route('/register', methods=['POST'])
def register():
   username = request.form['username']
   email = request.form['email']
   password = request.form['password']
   re_password = request.form['re_password']
   if password != re_password:
        return render_template('register.html', error="Mật khẩu không khớp")
   else:
        connection = sqlite3.connect(dirname + '\data.db')
        cursor = connection.cursor()
        query1 = "SELECT * FROM user WHERE username = '{name}' OR email = '{email}'".format(name = username, email = email)
        cursor.execute(query1)
        result = cursor.fetchone()
        connection.commit()
        if result == None:
            passwordhash = hashlib.md5(password.encode()).hexdigest()
            query2 = "INSERT INTO user VALUES ('{name}','{passw}','{mail}')".format(name = username, mail = email, passw = passwordhash)
            cursor.execute(query2)
            connection.commit()
            return render_template('email_verify.html', email=email, success="Đăng kí thành công")
        else:
            return render_template('register.html', error="Username hoặc email đã tồn tại!")


app.run(debug=True)