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
import pandas as pd
from underthesea import word_tokenize, sent_tokenize
from datetime import datetime


app = Flask(__name__)
app.secret_key = "lethanhdat"
dirname = os.getcwd()

##########################--- DATA OWNER CUSTOM ---#############################
MAIL_USERNAME = 'nnktcbkr@gmail.com'
MAIL_PASSWORD = 'pcpteiclywtbsnqa'
ROOT_DOMAIN = 'http://127.0.0.1:5000'
EMAIL_SUBJECT = 'Thư mời đánh giá'
LIFETIME_SESSION = 5
################################################################################

############################### ROLE ###########################################
ANNOTATOR_ROLE = '0'
DATA_OWNER_ROLE = '1'
UPLOAD_FOLDER = 'static/upload'

# config Mail   ----------------------------------------------------------------
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

mail = Mail(app)

# handle error 404  ------------------------------------------------------------
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

# set life time session --------------------------------------------------------
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=LIFETIME_SESSION)

######################################## LOGIN #################################

# login index ------------------------------------------------------------------
@app.route('/login')
def get_login():
    return redirect(url_for('index'))

# check role and session in login   --------------------------------------------
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

# login with username, password ------------------------------------------------
@app.route('/', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    passwordhash = hashlib.md5(password.encode()).hexdigest()
    session['username'] = username
    result = select_role_by_username_password(username, password)
    if result != None:
        user_role = result[1]
        if check_role(user_role)==True:
            return redirect(url_for('admin_index'))
        else:
            return redirect(url_for('user_index'))
    else:
        return render_template('login.html', error="Sai tài khoản hoặc mật khẩu")

# user login    ----------------------------------------------------------------
@app.route('/user')
def user_index():
    if 'username' in session:
        username = session['username']
        user_role = select_role(username)
        if user_role!= None:
            if check_role(user_role[0])==False:
                project = session['project']
                # token = select_token_by_data_id(data)
                # task = select_task_by_project_id(project)
                return redirect(url_for('review', project=project)) 
                # return render_template('user.html',data= data, token = token, project = project, result=username, success="Đăng nhập thành công")
            else:
                return redirect(url_for('admin_index'))
    else:
        return redirect(url_for('index'))

# review textclass ------------------------------------------------
@app.route('/user/review', methods=['GET'])
def review():
    if 'username' in session:
        username = session['username']
        user_role = select_role(username)
        if user_role!= None:
            if check_role(user_role[0])==False:
                try: 
                    project = request.args['project']
                    number = int(session['number'])
                except:
                    project = session['project']
                    number = 5
                finally:

                    task = select_task_by_project_id(project)
                    
                    if task == "textclass":
                        tag = select_tag_textclass_by_project_id(project)
                        datas = []
                        temp = select_data_id_by_project_id(project, username, task)
                        if number > len(temp):
                            return redirect(url_for('review_done'))
                        while len(datas) < number:
                            dt = random.choice(temp)
                            if dt not in datas:
                                datas.append(dt)
                        sent = []
                        for dt in datas:
                            sent.append(select_sent_by_id(dt))
                        return render_template('textclass.html', project=project, datas=datas, sent=sent, number=number, tag=tag, task=task)
                    
                    if task == "pos":
                        datas = []
                        temp = select_data_id_by_project_id(project, username, task)
                        if number > len(temp):
                            return redirect(url_for('review_done'))
                        while len(datas) < number:
                            dt = random.choice(temp)
                            if dt not in datas:
                                datas.append(dt)
                        
                        tokens = []
                        for dt in datas:
                            tokens.append(select_token_by_data_id(dt))

                        tag = select_tag_pos_by_project_id(project)
                        return render_template('pos.html', project=project, tag=tag, datas=datas, tokens=tokens, task=task,number=number)
                    
                    if task == "ner":
                        datas = []
                        temp = select_data_id_by_project_id(project, username, task)
                        if number > len(temp):
                            return redirect(url_for('review_done'))
                        while len(datas) < number:
                            dt = random.choice(temp)
                            if dt not in datas:
                                datas.append(dt)

                        tokens = []
                        for dt in datas:
                            tokens.append(select_token_by_data_id(dt))

                        tag = select_tag_ner_by_project_id(project)
                        return render_template('pos.html', project=project, tag=tag, datas=datas, tokens=tokens, task=task,number=number)


                    if task == "parsing":
                        datas = []
                        temp = select_data_id_by_project_id(project, username, task)
                        if number > len(temp):
                            return redirect(url_for('review_done'))
                        while len(datas) < number:
                            dt = random.choice(temp)
                            if dt not in datas:
                                datas.append(dt)
                        
                        tokens = []
                        for dt in datas:
                            tokens.append(select_token_by_data_id(dt))
                        
                        lentoken=[]
                        for i in tokens:
                            lentoken.append(len(i))
                            
                        tag = select_tag_parsing_by_project_id(project)
                        return render_template('parsing.html', project=project, tag=tag, datas=datas, tokens=tokens, task=task, number=number, lentoken=lentoken)
            
            else:
                return redirect(url_for('admin_index'))
    else:
        return redirect(url_for('index'))

    # return render_template('textclass.html', project=project, data=data, tag=tag, lentag=lentag)
    
# review textclass ------------------------------------------------
@app.route('/user/review', methods=['POST'])
def textclass_post():
    username = session['username']
    project = request.args['project']
    task = select_task_by_project_id(project)
    number = int(request.form['number'])

    if task == "textclass":
        for i in range(0, number):
            review_textclass = request.form["id_{id}".format(id=str(i))]
            review_textclass_tag = request.form.getlist("tag_{id}".format(id=str(i)))

            for tag in review_textclass_tag:
                if tag != '':
                    insert_text_class(review_textclass, tag, username)
            
        return redirect(url_for('review_done'))

    if task == "pos":

        for i in range(0, number):
            review_id = request.form["id_{id}".format(id=str(i))]
            review_token_pos = request.form.getlist("token_{id}".format(id=str(i)))
            review_tag_pos = request.form.getlist("tag_{id}".format(id=str(i)))

            print(review_id, review_token_pos, review_tag_pos)
            for i in range(len(review_token_pos)):
                if review_tag_pos[i] != '':
                    insert_pos(review_id, review_token_pos[i], review_tag_pos[i], username)
       
        return redirect(url_for('review_done'))

    
    if task == "ner":

        for i in range(0, number):
            review_id = request.form["id_{id}".format(id=str(i))]
            review_token_ner = request.form.getlist("token_{id}".format(id=str(i)))
            review_tag_ner = request.form.getlist("tag_{id}".format(id=str(i)))

            print(review_id, review_token_ner, review_tag_ner)
            for i in range(len(review_token_ner)):
                if review_tag_ner[i] != '':
                    insert_ner(review_id, review_token_ner[i], review_tag_ner[i], username)
       
        return redirect(url_for('review_done'))


    if task == "parsing":

        for i in range(0, number):
            review_id = request.form["id_{id}".format(id=str(i))]
            review_tag_parsing = request.form.getlist("parsing_{id}".format(id=str(i)))
            print(review_id, review_tag_parsing)
            
            if review_tag_parsing != []:
                for i in range(len(review_tag_parsing)):
                    rv = review_tag_parsing[i].split(' ')
                    insert_parsing(review_id, rv[1], rv[2], rv[0], username)
        return redirect(url_for('review_done'))


# Thank you  ----------------------------------------------------------------
@app.route('/user/review/done')
def review_done():
    return render_template('thankyou.html')

# admin login   ----------------------------------------------------------------
@app.route('/admin')
def admin_index():
    if 'username' in session:
        username = session['username']
        user_role = select_role(username)
        if user_role!= None:
            if check_role(user_role[0])==True:
                project = select_all_project()
                return render_template('admin.html', username=username, project=project)
            else:
                return render_template('503.html')
    else:
        return redirect(url_for('index'))

################################ LOGIN BY LINK #################################

# login by link from data owner ------------------------------------------------
# @app.route('/login/username=<username>&password=<password>', methods=['GET'])
# def get_api_login(username, password):
#     if 'username' not in session:
#         return render_template('login.html', username=username, password=password)
#     else:
#         username = session['username']
#         user_role = select_role(username)
#         if user_role != None:
#             if check_role(user_role[0])==True:
#                 return redirect(url_for('admin_index'))
#             else:
#                 return redirect(url_for('user_index'))
#         else:
#             return redirect(url_for('get_register')) 

# login by link from data owner ------------------------------------------------
@app.route('/login/project=<project>&number=<number>&username=<username>&password=<password>', methods=['GET'])
def get_api_login_1(project, number, username, password):
    if 'username' not in session:
         return render_template('login.html', username=username, password=password)
    else:
        username_session = session['username']
        if username_session != username:
            session.pop('username', None)
            session.pop('project', None)
            return redirect(url_for('get_api_login_1', project=project, number=number, username=username, password=password))
        else:
            user_role = select_role(username_session)
            if user_role != None:
                if check_role(user_role[0])==True:
                    return redirect(url_for('admin_index'))
                else:
                    return redirect(url_for('user_index', project=project))    
            else:
                return redirect(url_for('get_register')) 

# login by link from data owner ------------------------------------------------
# @app.route('/login/username=<username>&password=<password>', methods=['POST'])
# def post_api_login(username, password):

#     usernameform = request.form['username']
#     passwordform = request.form['password']

#     if usernameform == username and passwordform == password:
#         result = select_role_by_username_password(username, password)
#         if result != None:
#             session['username'] = username
#             user_role = result[1]
#             if check_role(user_role)==True:
#                 return redirect(url_for('admin_index'))
#             else:
#                 return redirect(url_for('user_index'))
#     else:
#         return render_template('login.html', error="Sai tài khoản hoặc mật khẩu")

@app.route('/login/project=<project>&number=<number>&username=<username>&password=<password>', methods=['POST'])
def post_api_login_1(project, number, username, password):

    usernameform = request.form['username']
    passwordform = request.form['password']

    if usernameform == username and passwordform == password:
        result = select_role_by_username_password(username, password)
        if result != None:
            session['username'] = username
            user_role = result[1]
            if check_role(user_role)==True:
                return redirect(url_for('admin_index'))
            else:
                session['project'] = project
                session['number'] = number
                return redirect(url_for('user_index', project = project))
        else: 
            return redirect(url_for('login',error="Sai tài khoản hoặc mật khẩu"))
    else:
        return render_template('login.html', error="Sai tài khoản hoặc mật khẩu")

####################################### LOGOUT #################################

# logout    --------------------------------------------------------------------
@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('index'))

################################ ADMIN / INVITATION ############################

# invitation get    ------------------------------------------------------------
@app.route('/admin/invitation', methods=['GET'])
def get_invitation():
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        user_admin = session['username']
        user_role = select_role(user_admin)
        if user_role!= None:
            if check_role(user_role[0])==True:
                username = generate_username()
                password = generate_password()
                project = select_project()
                project_id = request.args['project']

                number = select_number_data_of_project(project_id)

                return render_template('invitation.html',
                    username=username,
                    user_admin=user_admin,
                    password=password,
                    project=project,
                    project_id=project_id,
                    number=number,
                    len=len(project))
            else:
                return render_template('503.html')
        return redirect(url_for('index'))

# invitation post   ------------------------------------------------------------
@app.route('/admin/invitation', methods=['POST'])
def post_invitation():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    project_id = request.form['project']
    number = request.form.get('number')

    insert_annotator(username, email, password)

    msg = Message(
        EMAIL_SUBJECT,
        sender = MAIL_USERNAME, 
        recipients = [email],
        )
    link = ROOT_DOMAIN+'/login/project={project_id}&number={number}&username={username}&password={password}'.format(project_id=project_id, number=number, username=username, password=password)
    msg.html = render_template('welcome.html', username=username, password=password, link=link, project_id = project_id)
    mail.send(msg)
    
    session['email'] = email
    session['link'] = link
    return redirect(url_for('register_successfully', email=email, link=link, success="Gửi thành công")) 

# invitation success    --------------------------------------------------------
@app.route('/admin/invitation/success', methods=['GET'])
def register_successfully():
    email = request.args['email']
    link = request.args['link']
    return render_template('sent_successfully.html', email=email, link=link, success="Gửi thành công")

# create new project    --------------------------------------------------------
@app.route('/admin/new_project', methods=['GET'])
def get_new_project():
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        user_admin = session['username']
        user_role = select_role(user_admin)
        if user_role !=None:
            if check_role(user_role[0])==True:
                projects = select_project_name()
                return render_template('new_project.html', user_admin=user_admin, projects=projects)
            else:
                return render_template('503.html')

# create new project    --------------------------------------------------------
@app.route('/admin/new_project', methods=['POST'])
def post_new_project():
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        user_admin = session['username']
        user_role = select_role(user_admin)
        if user_role!= None:
            if check_role(user_role[0])==True:
                project_id = generate_code()

                project_name = request.form['project_name']
                language = request.form['language']


                task = request.form['task']
                method = request.form['method']
                label = request.form.getlist('label')

                
                # now = datetime.now()
                # dt_string = now.strftime('%d/%m/%Y %H:%M:%S')
                # print(now)

                # insert
                insert_project(project_id, project_name, language, task, method)
                insert_label(task, label, project_id)

                uploaded_file = request.files['file']
                if uploaded_file.filename != '':
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
                    uploaded_file.save(file_path) 
                    data = read_file(file_path)  
                    
                    for i, row in data.iterrows():
                        
                        insert_sentences(row[4], project_id)
                        
                return redirect(url_for('admin_index'))

        else:
            return render_template('503.html')

################################### ADMIN REGISTER ############################# 

# admin register get    --------------------------------------------------------
@app.route('/register', methods=['GET'])
def get_register():
    if check_account_exist():
        return render_template('register.html', error="")
    else:
        return render_template('503.html')

# admin register post   --------------------------------------------------------
@app.route('/register', methods=['POST'])
def register():
    if check_account_exist():
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        re_password = request.form['re_password']
        if password != re_password:
            return render_template('register.html', error="Mật khẩu không khớp")
        else:
            insert_data_owner(username, email, password)
            return render_template('email_verify.html', email=email, success="Đăng kí thành công")
    else:
        return render_template('503.html')

###################################### FUNCTION ################################

# generate password ------------------------------------------------------------
def generate_password():
    length = 16       
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    all = lower + upper + num
    temp = random.sample(all,length)
    password = "".join(temp)
    return password

# generate username ------------------------------------------------------------
def generate_username():
    length = 6
    lower = string.ascii_lowercase
    num = string.digits
    all = lower + num
    temp = random.sample(all,length)
    username = "".join(temp)
    return 'user_' + username

# generate code ----------------------------------------------------------------
def generate_code():
    length = 8
    lower = string.ascii_lowercase
    num = string.digits
    all = lower + num
    temp = random.sample(all,length)
    code = "".join(temp)
    return code

# check role user / admin   ----------------------------------------------------
def check_role(user_role):
    if user_role == '1':
        return True
    else:
        return False

############################### DATABASE CRUD METHOD ###########################

# connect to database   --------------------------------------------------------
def connect_to_db():
    conn = sqlite3.connect(dirname + '\data.db')
    return conn

# ----------------------------- SELECT -----------------------------------------

# select role by username   ----------------------------------------------------
def select_role(username):
    connection = connect_to_db()
    cursor = connection.cursor()
    query1 = "SELECT role FROM user WHERE username = '{name}'".format(name = username)
    cursor.execute(query1)
    result = cursor.fetchone()
    connection.commit()
    return result

# select role by username, password --------------------------------------------
def select_role_by_username_password(username, password):
    connection = connect_to_db()
    cursor = connection.cursor()
    passwordhash = hashlib.md5(password.encode()).hexdigest()
    query = "SELECT username, role FROM user WHERE username = '{name}' AND password = '{passw}'".format(name = username, passw = passwordhash)
    cursor.execute(query)
    result = cursor.fetchone()
    connection.commit()
    return result

# check account exist   --------------------------------------------------------
def check_account_exist():
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT * FROM user"
    cursor.execute(query)
    result = cursor.fetchone()
    connection.commit()
    if result == None:
        return True
    return False

# select data_id by sentence  -------------------------------------------------
def select_data_id(sent):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT id FROM Data WHERE sent = '{sent}'".format(sent = sent)
    cursor.execute(query)
    result = cursor.fetchone()
    return result

# select data_id by project id  ------------------------------------------------
def select_data_id_by_project_id(project_id, username, task):
    if task == "pos":
        tsk = "POS"
    if task == "ner":
        tsk = "NER"
    if task == "parsing":
        tsk = "Parsing"
    if task == "textclass":
        tsk = "TextClass"
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT id FROM Data WHERE project_id = '{id}' AND id NOT IN (SELECT data_id FROM '{task}' WHERE username = '{username}')".format(id = project_id, task = tsk, username = username)
    cursor.execute(query)
    result = []
    for id in cursor:
        result.append(id[0])
    return result

# select data_id by project id  ------------------------------------------------
def select_sent_by_id(id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT sent FROM Data WHERE id = '{id}'".format(id = id)
    cursor.execute(query)
    result = cursor.fetchone()[0]
    return result

# select project_id by name ----------------------------------------------------
def select_project_id(name):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT id FROM Project WHERE name = '{name}'".format(name = name)
    cursor.execute(query)
    result = cursor.fetchone()
    return result

# select all project    --------------------------------------------------------
def select_project():
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT id, name FROM Project"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

# select_project_id    --------------------------------------------------------
def select_project_id():
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT id FROM Project"
    cursor.execute(query)
    result = []
    for id in cursor:
        result.append(id[0])
    return result

def select_all_project():
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT * FROM Project"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

# select_project_id    --------------------------------------------------------
def select_project_name():
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT name FROM Project"
    cursor.execute(query)
    result = []
    for id in cursor:
        result.append(id[0])
    return result
# select token by data id   ----------------------------------------------------
def select_token_by_data_id(id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT word FROM Tokenize where data_id = '{id}'".format(id = id)
    cursor.execute(query)
    result = []
    for id in cursor:
        result.append(id[0])
    return result

# select task by project id ----------------------------------------------------
def select_task_by_project_id(id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT task FROM Project WHERE id = '{id}'".format(id = id)
    cursor.execute(query)
    result = cursor.fetchone()[0]
    return result

# select tag texclass by project id --------------------------------------------
def select_tag_textclass_by_project_id(project_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT tag FROM TagTextClass where project_id = '{id}'".format(id = project_id)
    cursor.execute(query)
    result = []
    for id in cursor:
        result.append(id[0])
    return result

# select tag pos by project id  ------------------------------------------------
def select_tag_pos_by_project_id(project_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT tag FROM TagPOS where project_id = '{id}'".format(id = project_id)
    cursor.execute(query)
    result = []
    for id in cursor:
        result.append(id[0])
    return result

# select tag ner by project id  ------------------------------------------------
def select_tag_ner_by_project_id(project_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT tag FROM TagNER where project_id = '{id}'".format(id = project_id)
    cursor.execute(query)
    result = []
    for id in cursor:
        result.append(id[0])
    return result

# select tag parsing by project id  ------------------------------------------------
def select_tag_parsing_by_project_id(project_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT tag FROM TagParsing where project_id = '{id}'".format(id = project_id)
    cursor.execute(query)
    result = []
    for id in cursor:
        result.append(id[0])
    return result

# select number of data in project id   --------------------------------------------
def select_number_data_of_project(project_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT id FROM Data where project_id = '{id}'".format(id = project_id)
    cursor.execute(query)
    count = 0
    for i in cursor:
        count += 1
    return count

# ------------------------------- INSERT ---------------------------------------

# insert annotator  ------------------------------------------------------------
def insert_annotator(username, email, password):
    connection = connect_to_db()
    cursor = connection.cursor()
    passwordhash = hashlib.md5(password.encode()).hexdigest()
    query1 = "INSERT INTO user VALUES ('{name}','{passw}','{mail}', '{role}')".format(name = username, mail = email, passw = passwordhash, role = ANNOTATOR_ROLE)
    cursor.execute(query1)
    connection.commit()

# insert data owner  ------------------------------------------------------------
def insert_data_owner(username, email, password):
    connection = connect_to_db()
    cursor = connection.cursor()
    passwordhash = hashlib.md5(password.encode()).hexdigest()
    query2 = "INSERT INTO user VALUES ('{name}','{passw}','{mail}', '{role}')".format(name = username, mail = email, passw = passwordhash, role = DATA_OWNER_ROLE)
    cursor.execute(query2)
    connection.commit()

# ### CREATE NEW PROJECT ###
def insert_project(project_id, project_name, language, task, method):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "INSERT INTO Project (id, name, language, task, method) VALUES ('{id}', '{name}', '{lang}', '{tsk}', '{mthd}')".format(id = project_id, name = project_name, lang = language, tsk = task, mthd = method)
    cursor.execute(query)
    connection.commit()

# ### INSERT INPUT DATA ###

# insert sentence to database   ------------------------------------------------
def insert_sentences(data, project_id):
    sent_list = data_to_sentences(data)

    connection = connect_to_db()
    cursor = connection.cursor()

    for sent in sent_list:
        id = generate_code()
        query = "INSERT INTO Data (id, sent, project_id) VALUES ('{id}', '{text}', '{proj_id}')".format(id = id, text = sent, proj_id = project_id)
        cursor.execute(query)
        connection.commit()

        insert_tokenize(sent, id)

# insert tokenize to database   ------------------------------------------------
def insert_tokenize(sent, data_id):
    word_list = sentence_to_tokens(sent)
    
    connection = connect_to_db()
    cursor = connection.cursor()
    for word in word_list:
        query = "INSERT INTO Tokenize (data_id, word) VALUES ('{dt_id}','{token}')".format(dt_id = data_id, token = word)
        cursor.execute(query)
        connection.commit()

# ### INSERT TAG ###

# insert tag NER    ------------------------------------------------------------
def insert_tag_ner(tag_ner, proj_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "INSERT INTO TagNER (tag, project_id) VALUES ('{tag}', '{proj_id}')".format(tag = tag_ner, proj_id = proj_id)
    cursor.execute(query)
    connection.commit()

# insert tag POS    ------------------------------------------------------------
def insert_tag_pos(tag_pos, proj_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "INSERT INTO TagPOS (tag, project_id) VALUES ('{tag}', '{proj_id}')".format(tag = tag_pos, proj_id = proj_id)
    cursor.execute(query)
    connection.commit()

# insert tag Parsing    --------------------------------------------------------
def insert_tag_parsing(tag_parsing, proj_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "INSERT INTO TagParsing (tag, project_id) VALUES ('{tag}', '{proj_id}')".format(tag = tag_parsing, proj_id = proj_id)
    cursor.execute(query)
    connection.commit()

# insert tag Text Classification    --------------------------------------------
def insert_tag_text_class(tag_text_class, proj_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "INSERT INTO TagTextClass (tag, project_id) VALUES ('{tag}', '{proj_id}')".format(tag = tag_text_class, proj_id = proj_id)
    cursor.execute(query)
    connection.commit()

# insert tag by task
def insert_label(task, label, proj_id):
    if task == "textclass":
        for tag in label:
            insert_tag_text_class(" ".join(tag.split()), proj_id)
    if task == "parsing":
        for tag in label:
            insert_tag_parsing(" ".join(tag.split()), proj_id)
    if task == "pos":
        for tag in label:
            insert_tag_pos(" ".join(tag.split()), proj_id)
    if task == "ner":
        for tag in label:
            insert_tag_ner(" ".join(tag.split()), proj_id)

# ### INSERT REVIEW ###

# insert review NER ------------------------------------------------------------
def insert_ner(data_id, token, tag_ner, username):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "INSERT INTO NER (data_id, token, tag, username) VALUES ('{dt_id}', '{tk}', '{tag}', '{user}')".format(dt_id = data_id, tk = token, tag = tag_ner, user = username)
    cursor.execute(query)
    connection.commit()

# insert review POS ------------------------------------------------------------
def insert_pos(data_id, token, tag_pos, username):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "INSERT INTO POS (data_id, token, tag, username) VALUES ('{dt_id}', '{tk}', '{tag}', '{user}')".format(dt_id = data_id, tk = token, tag = tag_pos, user = username)
    cursor.execute(query)
    connection.commit()
    
# insert review Parsing --------------------------------------------------------
def insert_parsing(data_id, token_1, token_2, tag_parsing, username):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "INSERT INTO Parsing (data_id, token_1, token_2, tag, username) VALUES ('{dt_id}', '{tk_1}', '{tk_2}', '{tag}', '{user}')".format(dt_id = data_id, tk_1 = token_1, tk_2 = token_2, tag = tag_parsing, user = username)
    cursor.execute(query)
    connection.commit()

# insert review Text Classification --------------------------------------------
def insert_text_class(data_id, tag_text_class, username):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "INSERT INTO TextClass (data_id, tag, username) VALUES ('{dt_id}', '{tag}', '{user}')".format(dt_id = data_id, tag = tag_text_class, user = username)
    cursor.execute(query)
    connection.commit()

# Upload CSV File --------------------------------------------
def read_file(filePath):
    # CVS Column Names
    # col_names = ['first_name','last_name','address', 'street', 'state' , 'zip']
    # Use Pandas to parse the CSV file
    csvData = pd.read_csv(filePath, header=None, encoding='utf8')
    # Loop through the Rows
    return csvData
    # for i,row in csvData.iterrows():
    #         print(i,row['first_name'],row['last_name'],row['address'],row['street'],row['state'],row['zip'],)

############################### HANDLE INPUT DATA ##############################

# split data to sentences   ----------------------------------------------------
def data_to_sentences(data):
    sent_list = sent_tokenize(data)
    return sent_list

# split sentence to tokenizes   ------------------------------------------------
def sentence_to_tokens(sent):
    word_list = word_tokenize(sent)
    return word_list

app.run(debug=True)