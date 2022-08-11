import re
from flask import Flask, request
from datetime import timedelta
from flask import render_template, session, redirect, url_for
from flask_mail import Mail, Message
import sqlite3
import os
import hashlib
import random
import string



app = Flask(__name__)
app.secret_key = "lethanhdat"
dirname = os.getcwd()

# Data Owner Custom 
MAIL_USERNAME = 'webbasedannotator@gmail.com'
MAIL_PASSWORD = 'eblqqukvfjguceyp'
ROOT_DOMAIN = 'http://127.0.0.1:5000'
EMAIL_SUBJECT = 'Thư mời đánh giá'

#
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/')
def index():
    if 'username' not in session:
        return render_template('login.html',
        error="",
        success="")
    else:
        username = session['username']
        user_role = select_role(username)
        if user_role != None:
            if check_role(user_role[0])==True:
                return redirect(url_for('admin_index'))
            else:
                return redirect(url_for('user_index'))
        else:
            return redirect(url_for('get_register')) 
        
@app.route('/', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    passwordhash = hashlib.md5(password.encode()).hexdigest()
    session['username'] = username
    result = select_role_by_username_password(username, password)[1]
    if result != None:
        user_role =  result[0]
        if check_role(user_role)==True:
            return redirect(url_for('admin_index'))
        else:
            return redirect(url_for('user_index'))
    else:
        return render_template('login.html', error="Sai tài khoản hoặc mật khẩu")

@app.route('/user')
def user_index():
    if 'username' in session:
        username = session['username']
        user_role = select_role(username)[0]
        if check_role(user_role)==False:
            return render_template('user.html', result=username, success="Đăng nhập thành công")
        else:
            return redirect(url_for('admin_index'))
    else:
        return render_template('login.html',
        error="",
        success="")
        
@app.route('/admin')
def admin_index():
    if 'username' in session:
        username = session['username']
        user_role = select_role(username)[0]
        if check_role(user_role)==True:
            return render_template('admin.html', result=username, success="Đăng nhập thành công")
        else:
            return render_template('503.html')
    else:
        return render_template('login.html',
        error="",
        success="")

@app.route('/admin/invitation', methods=['POST'])
def post_invitation():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    connection = connect_to_db()
    cursor = connection.cursor()

    passwordhash = hashlib.md5(password.encode()).hexdigest()
    query1 = "INSERT INTO user VALUES ('{name}','{passw}','{mail}', '0')".format(name = username, mail = email, passw = passwordhash)
    cursor.execute(query1)
    connection.commit()

    msg = Message(
        EMAIL_SUBJECT,
        sender = MAIL_USERNAME, 
        recipients = [email],
        )
    
    link = ROOT_DOMAIN+'/login/username={username}&password={password}'.format(username=username, password=password)
    msg.html = render_template('welcome.html', username=username, password=password, link=link)
    mail.send(msg)

    return render_template('email_verify.html', email=email, success="Đăng kí thành công")

@app.route('/login/username=<username>&password=<password>', methods=['GET'])
def get_api_login(username, password):
    return render_template('login.html', username=username, password=password)

@app.route('/login/username=<username>&password=<password>', methods=['POST'])
def post_api_login(username, password):
    result = select_role_by_username_password(username, password)[0]

    if result != None:
        session['username'] = username 
        return redirect(url_for('user_index'))
    else:
        return render_template('login.html', error="Sai tài khoản hoặc mật khẩu")

@app.route('/admin/invitation', methods=['GET'])
def get_invitation():
    if 'username' not in session:
        return render_template('login.html',
        error="",
        success="")
    else:
        username = session['username']
        user_role = select_role(username)[0]
        if check_role(user_role)==True:
            username = generate_username()
            password = generate_password()
            return render_template('invitation.html',
                username=username,
                password=password)
        else:
            return render_template('503.html')

@app.route('/login')
def get_login():
    return redirect(url_for('index'))
    
@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('index'))

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
        connection = connect_to_db()
        cursor = connection.cursor()
        query1 = "SELECT * FROM user WHERE username = '{name}' OR email = '{email}'".format(name = username, email = email)
        cursor.execute(query1)
        result = cursor.fetchone()
        connection.commit()
        if result == None:
            passwordhash = hashlib.md5(password.encode()).hexdigest()
            query2 = "INSERT INTO user VALUES ('{name}','{passw}','{mail}','1')".format(name = username, mail = email, passw = passwordhash)
            cursor.execute(query2)
            connection.commit()
            return render_template('email_verify.html', email=email, success="Đăng kí thành công")
        else:
            return render_template('register.html', error="Username hoặc email đã tồn tại!")

# function
def generate_password():
    length = 16       
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    all = lower + upper + num
    temp = random.sample(all,length)
    password = "".join(temp)
    return password

def generate_username():
    length = 6
    lower = string.ascii_lowercase
    num = string.digits
    all = lower + num
    temp = random.sample(all,length)
    username = "".join(temp)
    return 'user_' + username

def check_role(user_role):
    if user_role == '1':
        return True
    else:
        return False

def connect_to_db():
    conn = sqlite3.connect(dirname + '\data.db')
    return conn

def select_role(username):
    connection = connect_to_db()
    cursor = connection.cursor()
    query1 = "SELECT role FROM user WHERE username = '{name}'".format(name = username)
    cursor.execute(query1)
    result = cursor.fetchone()
    connection.commit()
    return result

def select_role_by_username_password(username, password):
    connection = connect_to_db()
    cursor = connection.cursor()
    passwordhash = hashlib.md5(password.encode()).hexdigest()
    query = "SELECT username, role FROM user WHERE username = '{name}' AND password = '{passw}'".format(name = username, passw = passwordhash)
    cursor.execute(query)
    result = cursor.fetchone()
    connection.commit()
    return result

app.run(debug=True)