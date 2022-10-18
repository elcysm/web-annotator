from flask import Flask, request
from flask import send_file
from datetime import timedelta
from flask import render_template, session, redirect, url_for
from flask_mail import Mail, Message
import sqlite3
import os
import hashlib
import random
import string
import pandas as pd
from nltk import word_tokenize as en_word_tokenize, sent_tokenize as en_sent_tokenize
from underthesea import word_tokenize as vie_word_tokenize, sent_tokenize as vie_sent_tokenize
import json
import collections
import csv
import pytz
import datetime as dt

app = Flask(__name__)
app.secret_key = "lethanhdat"
dirname = os.getcwd()


import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

##########################--- DATA OWNER CUSTOM ---#############################
MAIL_USERNAME = 'webbasedannotator@gmail.com'
MAIL_SERVICE_PASSWORD = 'eblqqukvfjguceyp'
ROOT_DOMAIN = 'http://127.0.0.1:5000'
EMAIL_SUBJECT = 'REVIEW INVITATION'
EMAIL_FORGOT_SUBJECT = 'CHANGE PASSWORD'

LIFETIME_SESSION = 24
################################################################################

############################### ROLE ###########################################
ANNOTATOR_ROLE = '0'
DATA_OWNER_ROLE = '1'
UPLOAD_FOLDER = 'static/upload'
DOWNLOAD_FOLDER = 'static/download'

# config Mail   ----------------------------------------------------------------
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_SERVICE_PASSWORD
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] =  DOWNLOAD_FOLDER


mail = Mail(app)

# handle error 404  ------------------------------------------------------------
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

# set life time session --------------------------------------------------------
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=LIFETIME_SESSION)

######################################## LOGIN #################################

# login index ------------------------------------------------------------------
@app.route('/login')
def get_login():
    return redirect(url_for('index'))

# check role and session in login   --------------------------------------------
@app.route('/')
def index():
    if 'username' not in session:
        print(session)
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
# @app.route('/', methods=['POST'])
# def login():
#     username = request.form['username']
#     password = request.form['password']
#     # passwordhash = hashlib.md5(password.encode()).hexdigest()
#     result = select_role_by_username_password(username, password)
#     if result != None:
#         session['username'] = username
#         user_role = result[1]
#         if check_role(user_role)==True:
#             return redirect(url_for('admin_index'))
#         else:
#             return redirect(url_for('user_index'))
#     else:
#         return render_template('login.html', error="Sai tài khoản hoặc mật khẩu")



# validate login with username, password ------------------------------------------------
@app.route('/username=<username>&password=<password>', methods=['POST'])
def validate(username, password):
    result = select_role_by_username_password(username, password)
    if result != None:
        session['username'] = username
        user_role = result[1]
        if check_role(user_role)==True:
            return "True"
        else:
            return "False"
    else:
        return "Invalid"


@app.route('/forgot_password', methods=['GET'])
def forgot_password():
    return render_template('forgot_password.html')


@app.route('/forgot_password/username=<username>', methods=['POST'])
def forgot_password22(username):
    email_select = select_email_by_username(username)
    if email_select!= None:
        email = email_select[0]
        msg = Message(
            EMAIL_FORGOT_SUBJECT,
            sender = MAIL_USERNAME, 
            recipients = [email],
        )

        link = ROOT_DOMAIN+'/change_password?username={username}&isEmail=True'.format(username=username)
        msg.html = render_template('admin/email_password_content.html', email=email, username=username, link=link)
        mail.send(msg)

        return '{}'.format(link)
    else:
        return 'Invalid'


@app.route('/change_password', methods=['GET'])
def change_password():
    username = request.args['username']
    isEmail = request.args['isEmail']

    if isEmail == 'True':
        session['isEmail'] = 'True'
    else: 
        session['isEmail'] = 'False'

    if session['isEmail'] == 'True' and 'username' not in session:
        if 'changepassword' not in session:
            session['changepassword'] = username
        if username == session['changepassword']:
            return render_template('change_password.html', username=username)
        else:
            return render_template('403.html')

    elif session['isEmail'] == 'False' and 'username' in session:
        session['changepassword'] = username
        if 'changepassword' in session:
            if session['username'] == session['changepassword']:
                return render_template('change_password.html', username=username)
            else:
                return render_template('403.html')
        else:
            return render_template('403.html')

    else:
            return render_template('403.html')


@app.route('/change_password', methods=['POST'])
def change_password_post():
    username = request.args['username']
    password = request.args['password']
    update_password_by_username(username, password)
    session.clear()
    return "OK"


# user index    ----------------------------------------------------------------
@app.route('/user')
def user_index():
    if 'username' in session:
        username = session['username']
        user_role = select_role(username)
        if user_role!= None:
            if check_role(user_role[0])==False:
                return redirect(url_for('review')) 
            else:
                return redirect(url_for('admin_index'))
    else:
        return redirect(url_for('index'))

################################ LOGIN BY LINK #################################

# login by link from data owner ------------------------------------------------
@app.route('/login/project=<project>&username=<username>&password=<password>', methods=['GET'])
def get_api_login(project, username, password):
    if 'username' not in session:
         return render_template('login.html', username=username, password=password)
    else:
        # username_session = session['username']
        # if username_session != username:
        #     session.pop('username', None)
        #     session.pop('project', None)
        #     return redirect(url_for('get_api_login', project=project, number=number, username=username, password=password))
        # else:
        user_role = select_role(username)
        if user_role != None:
            if check_role(user_role[0])==True:
                return redirect(url_for('admin_index'))
            else:
                return redirect(url_for('user_index'))    
        else:
            return redirect(url_for('get_register')) 


# login by link from data owner ------------------------------------------------

@app.route('/login/username=<username>&password=<password>', methods=['POST'])
def validate_annotator(username, password):
    result = select_role_by_username_password(username, password)
    if result != None:
        session['username'] = username
        user_role = result[1]
        if check_role(user_role)==False:
            return "True"
        else:
            return "False"
    else: 
        return "Invalid"
        
# # login by link from data owner ------------------------------------------------
# @app.route('/login/project=<project>&number=<number>&username=<username>&password=<password>', methods=['POST'])
# def post_api_login(project, number, username, password):

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
#                 session['number'] = number
#                 return redirect(url_for('user_index'))
#         else: 
#             return redirect(url_for('login',error="Sai tài khoản hoặc mật khẩu"))
#     else:
#         return render_template('login.html', error="Sai tài khoản hoặc mật khẩu")

####################################### LOGOUT #################################

# logout    --------------------------------------------------------------------
@app.route('/logout')
def logout():
   session.clear()
   return redirect(url_for('index'))

################################### USER REVIEW ################################

# user review get    -----------------------------------------------------------
@app.route('/user/review', methods=['GET'])
def review():
    if 'username' in session:
        username = session['username']
        user_role = select_role(username)
        if user_role!= None:
            if check_role(user_role[0])==False:
                number = select_number_by_annotator(username)
                try: 
                    project = request.args['project']
                    project_temp = select_project_id_by_annotator(username)
                    if project != project_temp:
                        return redirect(url_for('review', project = project_temp))
                except:
                    project = select_project_id_by_annotator(username)
                    return redirect(url_for('review', project = project))
                else:

                    task = select_task_by_project_id(project)
                    method = select_method_by_project_id(project)
                    
                    if task == "textclass" and method == "0":
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
                        return render_template('annotator/task_textclass.html', 
                                                project=project, 
                                                datas=datas, 
                                                sent=sent, 
                                                number=number, 
                                                tag=tag, 
                                                task=task, 
                                                username=username)
                    
                    if task == "pos" and method == "0":
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
                        return render_template('annotator/task_pos.html', 
                                                project=project, 
                                                tag=tag, 
                                                datas=datas, 
                                                tokens=tokens, 
                                                task=task,
                                                number=number, 
                                                username=username)
                    
                    if task == "ner" and method == "0":
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

                        tag = select_tag_ner_by_project_id(project)
                        return render_template('annotator/task_ner.html', 
                                                project=project, 
                                                tag=tag, 
                                                datas=datas, 
                                                tokens=tokens, 
                                                task=task,
                                                number=number, 
                                                lentoken=lentoken, 
                                                username=username)


                    if task == "parsing" and method == "0":
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
                        return render_template('annotator/task_parsing.html', 
                                                project=project, 
                                                tag=tag, 
                                                datas=datas, 
                                                tokens=tokens, 
                                                task=task, 
                                                number=number, 
                                                lentoken=lentoken, 
                                                username=username)


                    if task == "aspect" and method == "0":
                        tag = select_tag_aspect_by_project_id(project)
                        tag_entity = select_tag_aspect_entity_by_project_id(project)
                        tag_attribute = select_tag_aspect_attribute_by_project_id(project)

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
                        return render_template('annotator/task_aspect.html', 
                                                project=project, 
                                                datas=datas, 
                                                sent=sent, 
                                                number=number, 
                                                tag=tag, 
                                                tag_entity=tag_entity, 
                                                tag_attribute=tag_attribute, 
                                                task=task, 
                                                username=username)


                    if task == "paraphrase" and method == "1":

                        datas = []
                        sent1 = []
                        sent2 = []
                        temp = select_data_id_by_project_id(project, username, task)
                        if number > len(temp):
                            return redirect(url_for('review_done'))
                        while len(datas) < number:
                            dt = random.choice(temp)
                            if dt not in datas:
                                datas.append(dt)
                        for dt in datas:
                            temp = select_sent_by_id(dt).split('~')
                            sent1.append(temp[0])
                            sent2.append(temp[1])

                        return render_template('annotator/task_paraphrase.html', 
                                                project=project, 
                                                datas=datas, 
                                                sent1=sent1, 
                                                sent2=sent2, 
                                                number=number, 
                                                task=task, 
                                                username=username)
                    
                    if task == "multimodal" and method == "0":

                        datas = []
                        img_src = []
                        text = []
                        temp = select_data_id_by_project_id(project, username, task)
                        if number > len(temp):
                            return redirect(url_for('review_done'))
                        while len(datas) < number:
                            dt = random.choice(temp)
                            if dt not in datas:
                                datas.append(dt)
                        for dt in datas:
                            temp = select_sent_by_id(dt).split('~')
                            img_src.append(temp[0])
                            text.append(temp[1])

                        return render_template('annotator/task_multimodal.html', 
                                                project=project, 
                                                datas=datas, 
                                                img_src=img_src, 
                                                text=text, 
                                                number=number, 
                                                task=task, 
                                                username=username)
            else:
                return redirect(url_for('admin_index'))
    else:
        return redirect(url_for('index'))
    
# user review post    ----------------------------------------------------------
@app.route('/user/review', methods=['POST'])
def review_post():
    username = session['username']
    project = request.args['project']
    task = select_task_by_project_id(project)
    number = int(request.form['number'])

    
    vietnam=pytz.timezone('Asia/Ho_Chi_Minh')

    now = dt.datetime.now()

    vietnam_now = now.astimezone(vietnam).strftime("%d/%m/%Y %H:%M:%S")

    count = 0

    if task == "textclass":
        for i in range(0, number):
            review_textclass = request.form["id_{id}".format(id=str(i))]
            review_textclass_tag = request.form.getlist("tag_{id}".format(id=str(i)))
            
            temp = 0
            for tag in review_textclass_tag:
                if tag != '':
                    temp += 1
                    insert_text_class(review_textclass, tag, username)
            if temp != 0:
                count +=1
        if count != 0:   
            insert_notice(username, count, vietnam_now)
        return redirect(url_for('review_done'))

    if task == "pos":

        for i in range(0, number):
            review_id = request.form["id_{id}".format(id=str(i))]
            review_token_pos = request.form.getlist("token_{id}".format(id=str(i)))
            review_tag_pos = request.form.getlist("tag_{id}".format(id=str(i)))

            temp = 0
            for i in range(len(review_token_pos)):
                if review_tag_pos[i] != '':
                    temp += 1
                    temp_token = review_token_pos[i].replace("'","''")
                    insert_pos(review_id, temp_token, review_tag_pos[i], username)
            if temp != 0:
                count +=1
        if count != 0:
            insert_notice(username, count, vietnam_now)
        return redirect(url_for('review_done'))

    
    if task == "ner":

        for i in range(0, number):
            review_id = request.form["id_{id}".format(id=str(i))]
            review_token_ner = request.form.getlist("token_{id}".format(id=str(i)))
            review_tag_ner = request.form.getlist("tag_{id}".format(id=str(i)))


            temp = 0
            for i in range(len(review_token_ner)):
                
                if review_tag_ner[i] != '' and review_token_ner[i] != '':
                    temp += 1
                    temp_token = review_token_ner[i].replace("'","''")
                    insert_ner(review_id, temp_token, review_tag_ner[i], username)

            if temp != 0:
                count +=1
        if count != 0:
            insert_notice(username, count, vietnam_now)
        return redirect(url_for('review_done'))


    if task == "parsing":

        for i in range(0, number):
            review_id = request.form["id_{id}".format(id=str(i))]
            review_tag_parsing = request.form.getlist("parsing_{id}".format(id=str(i)))
            
            if review_tag_parsing != []:
                count +=1
                for i in range(len(review_tag_parsing)):
                    rv = review_tag_parsing[i].split(' ')
                    temp_token_1 = rv[1].replace("'","''")
                    temp_token_2 = rv[2].replace("'","''")

                    insert_parsing(review_id, temp_token_1, temp_token_2, rv[0], username)
        if count != 0:
            insert_notice(username, count, vietnam_now)
        return redirect(url_for('review_done'))


    if task == "aspect":
        for i in range(0, number):
            review_aspect = request.form["id_{id}".format(id=str(i))]
            review_aspect_tag_entity = request.form.getlist("tag_entity_{id}".format(id=str(i)))[0]
            review_aspect_tag_attribute = request.form.getlist("tag_attribute_{id}".format(id=str(i)))[0]
            review_aspect_tag = request.form.getlist("tag_{id}".format(id=str(i)))[0]


            
            temp = 0
            if review_aspect_tag != '' and review_aspect_tag_entity != '' and review_aspect_tag_attribute != '':
                temp += 1
                insert_aspect(review_aspect, review_aspect_tag_entity, review_aspect_tag_attribute, review_aspect_tag, username)
                    
            if temp != 0:
                count +=1
        if count != 0:   
            insert_notice(username, count, vietnam_now)
        return redirect(url_for('review_done'))

    if task == "paraphrase":
        for i in range(0, number):
            review_paraphrase = request.form["id_{id}".format(id=str(i))]
            review_paraphrase_tag = request.form.getlist("tag_{id}".format(id=str(i)))
            
            temp = 0
            for tag in review_paraphrase_tag:
                if tag != '':
                    temp += 1
                    insert_paraphrase(review_paraphrase, tag, username)
            if temp != 0:
                count +=1
        if count != 0:   
            insert_notice(username, count, vietnam_now)
        return redirect(url_for('review_done'))

    if task == "multimodal":
        for i in range(0, number):
            review_multimodal = request.form["id_{id}".format(id=str(i))]
            review_multimodal_img_tag = request.form.getlist("img_tag_{id}".format(id=str(i)))
            review_multimodal_text_tag = request.form.getlist("text_tag_{id}".format(id=str(i)))

            temp = 0
            temp_img_tag = ''
            temp_text_tag = ''

            for i in range(0, 3):
                if review_multimodal_img_tag[i] != '':
                    temp_img_tag = review_multimodal_img_tag[i]
                if review_multimodal_text_tag[i] != '':
                    temp_text_tag = review_multimodal_text_tag[i]

            if temp_img_tag != '' and temp_text_tag != '':
                temp += 1
                insert_multimodal(review_multimodal, temp_img_tag, temp_text_tag, username)
            if temp != 0:
                count +=1
        if count != 0:   
            insert_notice(username, count, vietnam_now)
        return redirect(url_for('review_done'))

# review done -> thank you  ----------------------------------------------------
@app.route('/user/review/done')
def review_done():
    username = session['username']
    return render_template('annotator/anno_review_done.html', username=username)

######################################## ADMIN #################################

# admin index   ----------------------------------------------------------------
@app.route('/admin')
def admin_index():
    if 'username' in session:
        username = session['username']
        user_role = select_role(username)
        if user_role!= None:
            if check_role(user_role[0])==True:
                num_project = select_number_of_project()
                num_annot = select_number_of_colaborator()
                num_task = int(select_number_of_task())
                task = select_all_task()
                tasks = []
                for i in task:
                    if i == "ner":
                        tasks.append('Named Entity Recognition')
                    if i == "pos":
                        tasks.append('Part-Of-Speech Tagging')
                    if i == "textclass":
                       tasks.append('Text Classification')
                    if i == "parsing":
                       tasks.append('Dependency Parsing')
                    if i == "aspect":
                       tasks.append('Aspect-based Sentiment')
                    if i == "paraphrase":
                       tasks.append('Paraphrase Detection')
                    if i == "multimodal":
                       tasks.append('MultiModal Sentiment')
                
                notice = select_notice()
                count_notif = 0
                for i in notice:
                    if i[2] == "0":
                        count_notif += 1

                return render_template('admin/admin_dashboard.html', username=username, num_project=num_project,
                num_annot= num_annot,
                num_task = num_task,
                tasks = tasks,
                notice=notice,
                count_notif=count_notif,
                success="Đăng nhập thành công")
            else:
                return render_template('403.html')
    else:
        return redirect(url_for('index'))

################################ ADMIN / PROJECT ###############################

# admin project index   --------------------------------------------------------
@app.route('/admin/project', methods=['GET'])
def admin_project():
    if 'username' in session:
        username = session['username']
        user_role = select_role(username)
        if user_role!= None:
            if check_role(user_role[0])==True:
                project = select_all_project()
                return render_template('admin/project.html', username=username, project=project)
            else:
                return render_template('403.html')
    else:
        return redirect(url_for('index'))

# admin delete project  --------------------------------------------------------
@app.route('/admin/project/delete', methods=['DELETE'])
def admin_delete_project():
    if 'username' in session:
        username = session['username']
        user_role = select_role(username)
        if user_role!= None:
            if check_role(user_role[0])==True:
                project_id = request.args['project_id']
                delete_project_by_id(project_id)
                return '0'
            else:
                return render_template('403.html')
    else:
        return redirect(url_for('index'))

# admin delete project  --------------------------------------------------------
@app.route('/admin/collaborator/delete', methods=['DELETE'])
def admin_delete_annotator():
    if 'username' in session:
        username = session['username']
        user_role = select_role(username)
        if user_role!= None:
            if check_role(user_role[0])==True:
                annotator_username = request.args['annotator_username']
                delete_annotator_by_username(annotator_username)
                return '0'
            else:
                return render_template('403.html')
    else:
        return redirect(url_for('index'))

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
                return render_template('admin/new_project.html', username=user_admin, projects=projects)
            else:
                return render_template('403.html')

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

                if task == "paraphrase" and method == "1" :
                    print("Log: Create Task: Paraphrase Detection")
                elif task == "multimodal" and method == "0" :
                    print("Log: Create Task: Multi Modal")
                else: 
                    insert_label(task, label, project_id)

                # insert
                insert_project(project_id, project_name, language, task, method)

                if task == "aspect" and method == "0":
                    label_entity = request.form.getlist('label_entity')
                    label_attribute = request.form.getlist('label_attribute')
                    
                    for tag in label_entity:
                        insert_tag_aspect_entity(" ".join(tag.split()), project_id)
                    for tag in label_attribute:
                        insert_tag_aspect_attribute(" ".join(tag.split()), project_id)

                
                connection = connect_to_db()
                cursor = connection.cursor()

                uploaded_file = request.files['file']
                if uploaded_file.filename != '':
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
                    uploaded_file.save(file_path) 
                    read_file(file_path, project_id, language, connection, cursor, task, method)
                        
                return redirect(url_for('admin_project'))

        else:
            return render_template('403.html')

# download project    ----------------------------------------------------------
@app.route('/admin/download')
def download():
    if 'username' in session:
        username = session['username']
        user_role = select_role(username)
        if user_role!= None:
            if check_role(user_role[0])==True:
                project = request.args['project']
                type = request.args['type']
                write_file(project, type)
                return redirect(url_for('admin_project'))
            else:
                return render_template('403.html')
    else:
        return redirect(url_for('index'))

################################ ADMIN / COLLAB ################################

# admin collab   ---------------------------------------------------------------
@app.route('/admin/collaborator')
def collaborator_index():
    if 'username' in session:
        username = session['username']
        user_role = select_role(username)
        if user_role!= None:
            if check_role(user_role[0])==True:
                annotator = select_username()
                number_review = []
                for i in annotator:
                    number_review.append(select_number_review_by_username(i[0], i[2]))
                len_annotator = len(annotator)
                return render_template('admin/collaborator.html', 
                username = username, 
                annotator = annotator, 
                number_review = number_review, 
                len_annotator = len_annotator)
            else:
                return render_template('403.html')
    else:
        return redirect(url_for('index'))

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
                project_id = request.args['project_id']
                number = select_number_data_of_project(project_id)
                return  '{}'.format(number) 
            else:
                return render_template('403.html')
        return redirect(url_for('index'))

# invitation post   ------------------------------------------------------------
@app.route('/admin/invitation/email=<email>&project_id=<project_id>&number=<number>', methods=['POST'])
def post_invitation(email,project_id,number):
   
    username = generate_username()
    password = generate_password()

    insert_annotator(username, email, password, project_id, number)
    task = select_task_by_project_id(project_id)
    task_name = ''
    if task == "ner":
        task_name = 'Named Entity Recognition'
    if task == "pos":
        task_name = 'Part-of-Speech Tagging'
    if task == "textclass":
        task_name = 'Text Classification'
    if task == "parsing":
        task_name = 'Dependency Parsing'
    if task == "aspect":
        task_name = 'Aspect-based Sentiment'
    if task == "paraphrase":
        task_name = 'Paraphrase Detection'
    if task == "multimodal":
        task_name = 'MultiModal Sentiment'
        
    msg = Message(
        EMAIL_SUBJECT,
        sender = MAIL_USERNAME, 
        recipients = [email],
        )

    link = ROOT_DOMAIN+'/login/project={project_id}&username={username}&password={password}'.format(project_id=project_id, username=username, password=password)
    msg.html = render_template('admin/email_content.html', username=username, password=password, link=link, project_id = project_id, task=task_name)
    mail.send(msg)

    return '{} {}'.format(link, email) 

# # invitation success    --------------------------------------------------------
# @app.route('/admin/invitation/success', methods=['GET'])
# def register_successfully():
#     link = session['link']
#     email = session['email']
#     return '{} {}'.format(link, email) 

################################### ADMIN REGISTER ############################# 

# admin register get    --------------------------------------------------------
@app.route('/register', methods=['GET'])
def get_register():
    if check_account_exist():
        return render_template('admin/register.html', error="")
    else:
        return render_template('403.html')

# admin register post   --------------------------------------------------------
@app.route('/register', methods=['POST'])
def register():
    if check_account_exist():
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        re_password = request.form['re_password']
        if password != re_password:
            return render_template('admin/register.html', error="Mật khẩu không khớp")
        else:
            insert_data_owner(username, email, password)
            return render_template('admin/email_verify.html', email=email, success="Đăng kí thành công")
    else:
        return render_template('403.html')

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
    length = 8
    lower = string.ascii_lowercase
    num = string.digits
    all = lower + num
    temp = random.sample(all,length)
    username = "".join(temp)
    return 'user_' + username

# generate code ----------------------------------------------------------------
def generate_code():
    length = 10
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

# get tag   --------------------------------------------------------------------
def get_tag(task):
    if task == 'pos':
        return 'POS'
    if task == 'ner':
        return 'NER'
    if task == 'parsing':
        return 'Parsing'
    if task == 'textclass':
        return 'TextClass'
    if task == 'aspect':
        return 'Aspect'
    if task == 'paraphrase':
        return 'Paraphrase'
    if task == 'multimodal':
        return 'MultiModal'

################################### READ FILE ##################################
def read_file(filePath, project_id, language, connection, cursor, task, method):
    ext = os.path.splitext(filePath)[1]
    if ext == ".csv":
        data = pd.read_csv(filePath, header=0, encoding='utf-8')
        # csvData = ""
        if task == "paraphrase" and method == "1":
            for i, row in data.iterrows():
                temp1 = row[1]
                temp2 = row[2]
                temp1 = temp1.replace("'", "''")
                temp2 = temp2.replace("'", "''")
                if '.' not in temp1:
                    temp1 = temp1.strip() + '. '
                if '.' not in temp2:
                    temp2 = temp2.strip() + '. '
                
                temp = temp1 + '~' + temp2
                
                insert_sentences(temp, project_id, language, connection, cursor)
            connection.commit()
        elif task == "multimodal" and method == "0":
            for i, row in data.iterrows():
                temp1 = row[1]
                temp2 = row[2]
                temp1 = temp1.replace("'", "''")
                temp2 = temp2.replace("'", "''")
                if '.' not in temp1:
                    temp1 = temp1.strip() + '. '
                if '.' not in temp2:
                    temp2 = temp2.strip() + '. '
                
                temp = temp1 + '~' + temp2
                
                insert_sentences(temp, project_id, language, connection, cursor)
            connection.commit()
        else:
            for i, row in data.iterrows():
                temp_1 = row[0]
                temp = temp_1.replace("'", "''")
                temp = temp.strip() + '. '
            
                insert_sentences(temp, project_id, language, connection, cursor)
            connection.commit()
            
    elif ext == ".txt":
        with open(filePath, encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            temp1 = line
            temp = temp1.replace('\n', ' ')
            if language == "eng":
                temp = temp.replace("'", "''")
            else:
                temp = temp.replace("'", " ")

            # if language == "eng":
            #     temp = line.replace('\n', ' ')
            #     temp = temp.replace("'", "''")
            # else:
            #     temp = line.replace('\n', ' ')
            #     temp = temp.replace("'", " ")
            # if '.' not in temp:
            #     temp = temp.strip() + '. '
            # if '. ' not in temp:
            #     temp = temp + ' '
            insert_sentences(temp, project_id, language, connection, cursor)
        connection.commit()

################################### EXPORT DATA ################################
# write file   -----------------------------------------------------------------
def write_file(project_id, type):
    if type == 'csv':
        write_file_csv(project_id)
    elif type == 'json':
        write_file_json(project_id)
# write file csv    ------------------------------------------------------------
def write_file_csv(project_id):
    task = select_task_by_project_id(project_id)
    with open(os.path.join(app.config['DOWNLOAD_FOLDER'],"{id}.csv".format(id=project_id)), 'w', newline='', encoding='UTF-8') as file:
        writer = csv.writer(file)
        if task == "pos":
            header = ['', 'sentences', 'tag', 'token']
            writer.writerow(header)
            datas = select_sent_and_id_by_project_id(project_id, task)
            count=1
            for dt in datas:
                id = dt[0]
                review = select_review_pos(id)
                # Truong hop data da co nguoi review
                if len(review) != 0:
                    uname = ""
                    for rv_part in review:
                        if rv_part[2] != uname:
                            data_review = [count, dt[1], rv_part[0], rv_part[1]]
                            uname = rv_part[2]
                        else:
                            data_review = ['', '', rv_part[0], rv_part[1]]
                        writer.writerow(data_review)
                    count+=1
        if task == "ner":
            header = ['', 'sentences', 'tag', 'token']
            writer.writerow(header)
            datas = select_sent_and_id_by_project_id(project_id, task)
            count=1
            for dt in datas:
                id = dt[0]
                review = select_review_ner(id)
                # Truong hop data da co nguoi review
                if len(review) != 0:
                    uname = ""
                    for rv_part in review:
                        if rv_part[2] != uname:
                            data_review = [count, dt[1], rv_part[0], rv_part[1]]
                            uname = rv_part[2]
                        else:
                            data_review = ['', '', rv_part[0], rv_part[1]]
                        
                        writer.writerow(data_review)
                    count+=1
        if task == "parsing":
            header = ['', 'sentences', 'tag', 'start', 'end']
            writer.writerow(header)
            datas = select_sent_and_id_by_project_id(project_id, task)
            count=1
            for dt in datas:
                id = dt[0]
                review = select_review_parsing(id)
                # Truong hop data da co nguoi review
                if len(review) != 0:
                    uname = ""
                    for rv_part in review:
                        if rv_part[3] != uname:
                            data_review = [count, dt[1], rv_part[2], rv_part[0], rv_part[1]]
                            uname = rv_part[3]
                        else:
                            data_review = ['', '', rv_part[2], rv_part[0], rv_part[1]]
                        writer.writerow(data_review)
                    count+=1
        if task == "textclass":
            header = ['', 'sentences', 'tag']
            writer.writerow(header)
            datas = select_sent_and_id_by_project_id(project_id, task)
            count=1
            for dt in datas:
                id = dt[0]
                review = select_review_textclass(id)
                # Truong hop data da co nguoi review
                if len(review) != 0:
                    uname = ""
                    for rv_part in review:
                        if rv_part[1] != uname:
                            data_review = [count, dt[1], rv_part[0]]
                            uname = rv_part[1]
                        else:
                            data_review = ['', '', rv_part[0]]
                        writer.writerow(data_review)
                    count+=1
                
# write file json   ------------------------------------------------------------
def write_file_json(project_id):
    task = select_task_by_project_id(project_id)
    review_list = []
    temp = []
    datas = select_sent_and_id_by_project_id(project_id, task)
    count=1
    if task == "ner":
        for dt in datas:
            id = dt[0]
            review = select_review_ner(id)
            # Truong hop data da co nguoi review
            if len(review) != 0:
                uname = review[0][2]
                dem=1
                d = collections.OrderedDict()
                d['id'] = count
                d['sent'] = dt[1].replace('"', '')
                for rv_part in review:
                    if rv_part[2] == uname:
                        temp.append({"tag": rv_part[1], "token": rv_part[0]})
                        dem+=1
                    else:
                        count+=1
                        dem=1
                        d['ner'] = temp
                        review_list.append(d)
                        d = collections.OrderedDict()
                        d['id'] = count
                        d['sent'] = dt[1].replace('"', '')
                        temp = []
                        temp.append({"tag": rv_part[1], "token": rv_part[0]})
                        dem+=1
                        uname = rv_part[2]
                    if rv_part == review[-1]:
                        d['ner'] = temp
                        review_list.append(d)
                        temp = []
                count+=1
    elif task == "pos":
        for dt in datas:
            id = dt[0]
            review = select_review_pos(id)
            # Truong hop data da co nguoi review
            if len(review) != 0:
                uname = review[0][2]
                dem=1
                d = collections.OrderedDict()
                d['id'] = count
                d['sent'] = dt[1].replace('"', '')
                for rv_part in review:
                    if rv_part[2] == uname:
                        temp.append({"tag": rv_part[1], "token": rv_part[0]})
                        dem+=1
                    else:
                        count+=1
                        dem=1
                        d['pos'] = temp
                        review_list.append(d)
                        d = collections.OrderedDict()
                        d['id'] = count
                        d['sent'] = dt[1].replace('"', '')
                        temp = []
                        temp.append({"tag": rv_part[1], "token": rv_part[0]})
                        dem+=1
                        uname = rv_part[2]
                    if rv_part == review[-1]:
                        d['pos'] = temp
                        review_list.append(d)
                        temp = []
                count+=1
    elif task == "parsing":
        for dt in datas:
            id = dt[0]
            review = select_review_parsing(id)
            # Truong hop data da co nguoi review
            if len(review) != 0:
                uname = review[0][3]
                dem=1
                d = collections.OrderedDict()
                d['id'] = count
                d['sent'] = dt[1].replace('"', '')
                for rv_part in review:
                    if rv_part[3] == uname:
                        temp.append({"tag": rv_part[2], "start": rv_part[0], "end": rv_part[1]})
                        dem+=1
                    else:
                        count+=1
                        dem=1
                        d['parsing'] = temp
                        review_list.append(d)
                        d = collections.OrderedDict()
                        d['id'] = count
                        d['sent'] = dt[1].replace('"', '')
                        temp = []
                        temp.append({"tag": rv_part[2], "start": rv_part[0], "end": rv_part[1]})
                        dem+=1
                        uname = rv_part[3]
                    if rv_part == review[-1]:
                        d['parsing'] = temp
                        review_list.append(d)
                        temp = []
                count+=1
    elif task == "textclass":
        for dt in datas:
            id = dt[0]
            review = select_review_textclass(id)
            # Truong hop data da co nguoi review
            if len(review) != 0:
                uname = review[0][1]
                dem=1
                d = collections.OrderedDict()
                d['id'] = count
                d['sent'] = dt[1].replace('"', '')
                for rv_part in review:
                    if rv_part[1] == uname:
                        temp.append({"tag": rv_part[0]})
                        dem+=1
                    else:
                        count+=1
                        dem=1
                        d['textclass'] = temp
                        review_list.append(d)
                        d = collections.OrderedDict()
                        d['id'] = count
                        d['sent'] = dt[1].replace('"', '')
                        temp = []
                        temp.append({"tag": rv_part[0]})
                        dem+=1
                        uname = rv_part[1]
                    if rv_part == review[-1]:
                        d['textclass'] = temp
                        review_list.append(d)
                        temp = []
                count+=1
    elif task == "aspect":
        temp1 = []
        for dt in datas:
            id = dt[0]
            review = select_review_aspect(id)
            # Truong hop data da co nguoi review
            if len(review) != 0:
                uname = review[0][3]
                ent = review[0][0]
                dem=1
                d = collections.OrderedDict()
                d['id'] = count
                d['sent'] = dt[1].replace('"', '')
                for rv_part in review:
                    if rv_part[3] == uname:
                        if rv_part[0] == ent:
                            temp1.append({"attribute": rv_part[1], "tag": rv_part[2]})
                        else:
                            temp.append({"entity": ent, "review": temp1})
                            temp1 = []
                            ent = rv_part[0]
                            temp1.append({"attribute": rv_part[1], "tag": rv_part[2]})
                    else:
                        count+=1
                        dem=1
                        temp.append({"entity": ent, "review": temp1})
                        temp1 = []
                        ent = rv_part[0]
                        d['aspect'] = temp
                        review_list.append(d)
                        d = collections.OrderedDict()
                        d['id'] = count
                        d['sent'] = dt[1].replace('"', '')
                        temp = []
                        temp1.append({"attribute": rv_part[1], "tag": rv_part[2]})
                        dem+=1
                        uname = rv_part[3]

                    if rv_part == review[-1]:
                        temp.append({"entity": ent, "review": temp1})
                        temp1 = []
                        ent = rv_part[0]
                        d['aspect'] = temp
                        review_list.append(d)
                        temp = []
                count+=1
    elif task == "paraphrase":
        for dt in datas:
            id = dt[0]
            review = select_review_paraphrase(id)
            # Truong hop data da co nguoi review
            if len(review) != 0:
                
                for rv_part in review:
                    d = collections.OrderedDict()
                    d['id'] = count
                    temp = dt[1].replace('"', '')
                    temp = temp.split("~")
                    d['sent1'] = temp[0]
                    d['sent2'] = temp[1]
                    d['tag'] = rv_part[0]
                    count += 1
                    review_list.append(d)
    elif task == "multimodal":
        for dt in datas:
            id = dt[0]
            review = select_review_multimodal(id)
            # Truong hop data da co nguoi review
            if len(review) != 0:
                
                for rv_part in review:
                    d = collections.OrderedDict()
                    d['id'] = count
                    temp = dt[1].replace('"', '')
                    temp = temp.split("~")
                    d['image'] = [{"image": temp[0], "tag": rv_part[0]}]
                    d['text'] = [{"text": temp[1], "tag": rv_part[1]}]
                    count += 1
                    review_list.append(d)
    j = json.dumps(review_list, ensure_ascii=False)
    with open(os.path.join(app.config['DOWNLOAD_FOLDER'],"{id}.json".format(id=project_id)), 'w', encoding='UTF-8') as file:
        file.write(j)

############################### DATABASE CRUD METHOD ###########################

# connect to database   --------------------------------------------------------
def connect_to_db():
    conn = sqlite3.connect(dirname + '\data.db')
    return conn

# connect to database   --------------------------------------------------------
def vacuum_db():
    conn = connect_to_db()
    conn.execute('VACUUM')

# export database   --------------------------------------------------------
@app.route('/exportDatabase')
def downloadFile ():
    path = "data.db"
    return send_file(path, as_attachment=True)

###################################### SELECT ##################################

# select role by username   ----------------------------------------------------
def select_role(username):
    connection = connect_to_db()
    cursor = connection.cursor()
    query1 = "SELECT role FROM user WHERE username = '{name}'".format(name = username)
    cursor.execute(query1)
    result = cursor.fetchone()
    connection.commit()
    return result

# select email by username   ----------------------------------------------------
def select_email_by_username(username):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT email FROM user WHERE username = '{username}'".format(username = username)
    cursor.execute(query)
    result = cursor.fetchone()
    return result

# select username, role by username --------------------------------------------
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

# select data_id by sentence  --------------------------------------------------
def select_data_id(sent):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT id FROM Data WHERE sent = '{sent}'".format(sent = sent)
    cursor.execute(query)
    result = cursor.fetchone()
    return result

# select data_id (reviewed) by project id (for download)  ----------------------
def select_data_id_by_project_id(project_id, username, task):
    if task == "pos":
        tsk = "POS"
    if task == "ner":
        tsk = "NER"
    if task == "parsing":
        tsk = "Parsing"
    if task == "textclass":
        tsk = "TextClass"
    if task == "aspect":
        tsk = "Aspect"
    if task == "paraphrase":
        tsk = "Paraphrase"
    if task == "multimodal":
        tsk = "MultiModal"
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT id FROM Data WHERE project_id = '{id}' AND id NOT IN (SELECT data_id FROM '{task}' WHERE username = '{username}')".format(id = project_id, task = tsk, username = username)
    cursor.execute(query)
    result = []
    for id in cursor:
        result.append(id[0])
    return result

# select data_id by id  --------------------------------------------------------
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

# select id, name from all project    ------------------------------------------
def select_project():
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT id, name FROM Project"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

# select id from all project    ------------------------------------------------
def select_project_id():
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT id FROM Project"
    cursor.execute(query)
    result = []
    for id in cursor:
        result.append(id[0])
    return result

# select all project    -------------------------------------------------------- 
def select_all_project():
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT * FROM Project"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

# select name from all project    ----------------------------------------------
def select_project_name():
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT name FROM Project"
    cursor.execute(query)
    result = []
    for id in cursor:
        result.append(id[0])
    return result

# select number review by username (annotator)   -------------------------------
def select_number_review_by_username(username, project_id):
    task = select_task_by_project_id(project_id)
    connection = connect_to_db()
    cursor = connection.cursor()
    if task == "ner":
        query = "SELECT DISTINCT data_id, username FROM NER WHERE username = '{uname}'".format(uname = username)
    elif task == "pos":
        query = "SELECT DISTINCT data_id, username FROM POS WHERE username = '{uname}'".format(uname = username)
    elif task == "parsing":
        query = "SELECT DISTINCT data_id, username FROM Parsing WHERE username = '{uname}'".format(uname = username)
    elif task == "textclass":
        query = "SELECT DISTINCT data_id, username FROM TextClass WHERE username = '{uname}'".format(uname = username)
    elif task == "aspect":
        query = "SELECT DISTINCT data_id, username FROM Aspect WHERE username = '{uname}'".format(uname = username)
    elif task == "paraphrase":
        query = "SELECT DISTINCT data_id, username FROM Paraphrase WHERE username = '{uname}'".format(uname = username)
    elif task == "multimodal":
        query = "SELECT DISTINCT data_id, username FROM MultiModal WHERE username = '{uname}'".format(uname = username)
    cursor.execute(query)
    count = 0
    for i in cursor:
        count += 1
    return count

# select token by data id   ----------------------------------------------------
def select_token_by_data_id(id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT sent FROM Data where id = '{id}'".format(id = id)
    cursor.execute(query)
    sent = cursor.fetchone()[0]

    query1 = "SELECT Project.language FROM Project, Data where Data.id = '{id}' AND Data.project_id = Project.id".format(id = id)
    cursor.execute(query1)
    lang = cursor.fetchone()[0]

    result = sentence_to_tokens(sent, lang)
    return result

# select task by project id ----------------------------------------------------
def select_task_by_project_id(id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT task FROM Project WHERE id = '{id}'".format(id = id)
    cursor.execute(query)
    result = cursor.fetchone()[0]
    return result

# select method by project id ----------------------------------------------------
def select_method_by_project_id(id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT method FROM Project WHERE id = '{id}'".format(id = id)
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

# select tag parsing by project id  --------------------------------------------
def select_tag_parsing_by_project_id(project_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT tag FROM TagParsing where project_id = '{id}'".format(id = project_id)
    cursor.execute(query)
    result = []
    for id in cursor:
        result.append(id[0])
    return result

# select tag aspect by project id  --------------------------------------------
def select_tag_aspect_by_project_id(project_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT tag FROM TagAspect where project_id = '{id}'".format(id = project_id)
    cursor.execute(query)
    result = []
    for id in cursor:
        result.append(id[0])
    return result

# select tag aspect entity by project id  --------------------------------------------
def select_tag_aspect_entity_by_project_id(project_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT tag_entity FROM TagAspectEntity where project_id = '{id}'".format(id = project_id)
    cursor.execute(query)
    result = []
    for id in cursor:
        result.append(id[0])
    return result

# select tag aspect attribute by project id  --------------------------------------------
def select_tag_aspect_attribute_by_project_id(project_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT tag_attribute FROM TagAspectAttribute where project_id = '{id}'".format(id = project_id)
    cursor.execute(query)
    result = []
    for id in cursor:
        result.append(id[0])
    return result


# select number of data in project id   ----------------------------------------
def select_number_data_of_project(project_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT id FROM Data where project_id = '{id}'".format(id = project_id)
    cursor.execute(query)
    count = 0
    for i in cursor:
        count += 1
    return count

# select username infor (annotator)   ------------------------------------------
def select_username():
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT user.username, user.email, user.project_id, project.name FROM user, project where user.role = '{role}' and user.project_id = project.id".format(role = ANNOTATOR_ROLE)
    cursor.execute(query)
    result = cursor.fetchall()
    return result

# select project_id_by_annotator   ------------------------------------------
def select_project_id_by_annotator(username):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT project_id FROM user where username = '{username}'".format(username = username)
    cursor.execute(query)
    result = cursor.fetchone()[0]
    return result

# select number_of_data_by_annotator   ------------------------------------------
def select_number_by_annotator(username):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT number FROM user where username = '{username}'".format(username = username)
    cursor.execute(query)
    result = cursor.fetchone()[0]
    return result

# select numbers of project   --------------------------------------------------
def select_number_of_project():
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT COUNT(id) FROM Project"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    return result

# select numbers of collaborator   ---------------------------------------------
def select_number_of_colaborator():
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT COUNT(username) FROM user where role = '{role}'".format(role = ANNOTATOR_ROLE)
    cursor.execute(query)
    result = cursor.fetchone()[0]
    return result

# select numbers of task   -----------------------------------------------------
def select_number_of_task():
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT COUNT(DISTINCT task) FROM Project"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    return result

# select all task with distinct   ----------------------------------------------
def select_all_task():
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT DISTINCT task FROM Project"
    cursor.execute(query)
    result = []
    for id in cursor:
        result.append(id[0])
    return result

# select id, sent (reviewed) by project id  ------------------------------------
def select_sent_and_id_by_project_id(project_id, task):
    tsk = get_tag(task)
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT id, sent FROM Data where project_id = '{id}' AND id IN (SELECT data_id FROM '{tsk}')".format(tsk = tsk, id = project_id)
    cursor.execute(query)
    result = cursor.fetchall()
    return result

# select review pos  -----------------------------------------------------------
def select_review_pos(data_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT token, tag, username FROM POS where data_id = '{id}' ORDER BY username".format(id = data_id)
    cursor.execute(query)
    result = cursor.fetchall()
    return result

# select review ner  -----------------------------------------------------------
def select_review_ner(data_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT token, tag, username FROM NER where data_id = '{id}' ORDER BY username".format(id = data_id)
    cursor.execute(query)
    result = cursor.fetchall()
    return result

# select review parsing  -------------------------------------------------------
def select_review_parsing(data_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT token_1, token_2, tag, username FROM Parsing where data_id = '{id}' ORDER BY username".format(id = data_id)
    cursor.execute(query)
    result = cursor.fetchall()
    return result

# select review aspect  -------------------------------------------------------
def select_review_aspect(data_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT tag_entity, tag_attribute, tag, username FROM Aspect where data_id = '{id}' ORDER BY  username, tag_entity".format(id = data_id)
    cursor.execute(query)
    result = cursor.fetchall()
    return result

# select review textclass  -----------------------------------------------------
def select_review_textclass(data_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT tag, username FROM TextClass where data_id = '{id}' ORDER BY username".format(id = data_id)
    cursor.execute(query)
    result = cursor.fetchall()
    return result

# select review paraphrase  -------------------------------------------------------
def select_review_paraphrase(data_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT tag, username FROM Paraphrase where data_id = '{id}' ORDER BY username".format(id = data_id)
    cursor.execute(query)
    result = cursor.fetchall()
    return result

# select review multimodal  -------------------------------------------------------
def select_review_multimodal(data_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT img_tag, text_tag, username FROM MultiModal where data_id = '{id}' ORDER BY username".format(id = data_id)
    cursor.execute(query)
    result = cursor.fetchall()
    return result

# select notice  ---------------------------------------------------------------
def select_notice():
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "SELECT ReviewNoti.username, ReviewNoti.number_review, ReviewNoti.seen, ReviewNoti.last_modified, user.project_id, Project.name FROM ReviewNoti, Project, user where Project.id = user.project_id and user.username = ReviewNoti.username ORDER BY ReviewNoti.id DESC"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

###################################### INSERT ##################################

# insert annotator  ------------------------------------------------------------
def insert_annotator(username, email, password, project_id, number):
    connection = connect_to_db()
    cursor = connection.cursor()
    passwordhash = hashlib.md5(password.encode()).hexdigest()
    query1 = "INSERT INTO user VALUES ('{name}','{passw}','{mail}', '{role}', '{project_id}', {number})".format(name = username, mail = email, passw = passwordhash, role = ANNOTATOR_ROLE, project_id=project_id, number=number)
    cursor.execute(query1)
    connection.commit()

# insert data owner  ------------------------------------------------------------
def insert_data_owner(username, email, password):
    connection = connect_to_db()
    cursor = connection.cursor()
    passwordhash = hashlib.md5(password.encode()).hexdigest()
    query2 = "INSERT INTO user VALUES ('{name}','{passw}','{mail}', '{role}', '{project_id}', {number})".format(name = username, mail = email, passw = passwordhash, role = DATA_OWNER_ROLE, project_id='', number='')
    cursor.execute(query2)
    connection.commit()

# create new project
def insert_project(project_id, project_name, language, task, method):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "INSERT INTO Project (id, name, language, task, method) VALUES ('{id}', '{name}', '{lang}', '{tsk}', '{mthd}')".format(id = project_id, name = project_name, lang = language, tsk = task, mthd = method)
    cursor.execute(query)
    connection.commit()

# insert review notification  ------------------------------------------------------------
def insert_notice(username, number, date):
    connection = connect_to_db()
    cursor = connection.cursor()
    query1 = "INSERT INTO ReviewNoti (username, number_review, seen, last_modified) VALUES ('{username}','{number_review}','0', '{date}')".format(username = username, number_review = number, date = date)
    cursor.execute(query1)
    connection.commit()

# ### INSERT INPUT DATA ###

# insert sentence to database   ------------------------------------------------
def insert_sentences(data, project_id, language, connection, cursor):
    
    # sent_list = data_to_sentences(data, language)

    # for sent in sent_list:
    try:
        id = generate_code()
        # start = time.time()
        query = "INSERT INTO Data (id, sent, project_id) VALUES ('{id}', '{text}', '{proj_id}')".format(id = id, text = data, proj_id = project_id)
        cursor.execute(query)
    except:
        print(data)
    
    # start1 = time.time()
    # connection.commit()
    # end2 = time.time()
    # print("\n"f"{(end2 - start1)} secs.")=


    
    

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

# insert tag aspect   --------------------------------------------
def insert_tag_aspect(tag_aspect, proj_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "INSERT INTO TagAspect (tag, project_id) VALUES ('{tag}', '{proj_id}')".format(tag = tag_aspect, proj_id = proj_id)
    cursor.execute(query)
    connection.commit()

# insert tag aspect entity  --------------------------------------------
def insert_tag_aspect_entity(tag_aspect_entity, proj_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "INSERT INTO TagAspectEntity (tag_entity, project_id) VALUES ('{tag}', '{proj_id}')".format(tag = tag_aspect_entity, proj_id = proj_id)
    cursor.execute(query)
    connection.commit()

# insert tag aspect attribute  --------------------------------------------
def insert_tag_aspect_attribute(tag_aspect_attribute, proj_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "INSERT INTO TagAspectAttribute (tag_attribute, project_id) VALUES ('{tag}', '{proj_id}')".format(tag = tag_aspect_attribute, proj_id = proj_id)
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
    if task == "aspect":
        for tag in label:
            insert_tag_aspect(" ".join(tag.split()), proj_id)

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

# insert review Paraphrase Detection --------------------------------------------
def insert_paraphrase(data_id, tag_paraphrase, username):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "INSERT INTO Paraphrase (data_id, tag, username) VALUES ('{dt_id}', '{tag}', '{user}')".format(dt_id = data_id, tag = tag_paraphrase, user = username)
    cursor.execute(query)
    connection.commit()

# insert review MultiModal --------------------------------------------
def insert_multimodal(data_id, img_tag, text_tag, username):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "INSERT INTO MultiModal (data_id, img_tag, text_tag, username) VALUES ('{dt_id}', '{img_tag}', '{text_tag}', '{user}')".format(dt_id = data_id, img_tag = img_tag, text_tag = text_tag, user = username)
    cursor.execute(query)
    connection.commit()


# insert review Aspect --------------------------------------------
def insert_aspect(data_id, tag_entity, tag_attribute, tag, username):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "INSERT INTO Aspect (data_id, tag_entity, tag_attribute, tag, username) VALUES ('{dt_id}', '{tag_entity}', '{tag_attribute}', '{tag}', '{user}')".format(dt_id = data_id, tag_entity = tag_entity, tag_attribute = tag_attribute, tag = tag,  user = username)
    cursor.execute(query)
    connection.commit()


###################################### DELETE ##################################
def delete_project_by_id(project_id):
    task = select_task_by_project_id(project_id)

    connection = connect_to_db()
    cursor = connection.cursor()
    query1 = "DELETE FROM Project WHERE id = '{id}'".format(id = project_id)
    query2 = "DELETE FROM Data WHERE project_id = '{id}'".format(id = project_id)

    if task == 'pos':
        query3 = "DELETE FROM TagPOS WHERE project_id = '{id}'".format(id = project_id)
        query4 = "DELETE FROM POS WHERE data_id IN (SELECT id FROM Data WHERE project_id = '{id}')".format(id = project_id)
    if task == 'ner':
        query3 = "DELETE FROM TagNER WHERE project_id = '{id}'".format(id = project_id)
        query4 = "DELETE FROM NER WHERE data_id IN (SELECT id FROM Data WHERE project_id = '{id}')".format(id = project_id)
    if task == 'parsing':
        query3 = "DELETE FROM TagParsing WHERE project_id = '{id}'".format(id = project_id)
        query4 = "DELETE FROM Parsing WHERE data_id IN (SELECT id FROM Data WHERE project_id = '{id}')".format(id = project_id)
    if task == 'textclass':
        query3 = "DELETE FROM TagTextClass WHERE project_id = '{id}'".format(id = project_id)
        query4 = "DELETE FROM TextClass WHERE data_id IN (SELECT id FROM Data WHERE project_id = '{id}')".format(id = project_id)
    if task == 'aspect':
        query3 = "DELETE FROM TagAspect WHERE project_id = '{id}'".format(id = project_id)
        query4 = "DELETE FROM Aspect WHERE data_id IN (SELECT id FROM Data WHERE project_id = '{id}')".format(id = project_id)
        query6 = "DELETE FROM TagAspectEntity WHERE project_id = '{id}'".format(id = project_id)
        query7 = "DELETE FROM TagAspectAttribute WHERE project_id = '{id}'".format(id = project_id)
        cursor.execute(query6)
        cursor.execute(query7)
    if task == 'paraphrase':
        query3 = "DELETE FROM Paraphrase WHERE data_id IN (SELECT id FROM Data WHERE project_id = '{id}')".format(id = project_id)
        query4 = ""
    if task == 'multimodal':
        query3 = "DELETE FROM MultiModal WHERE data_id IN (SELECT id FROM Data WHERE project_id = '{id}')".format(id = project_id)
        query4 = ""


    query5 = "DELETE FROM user WHERE project_id = '{id}'".format(id = project_id)

    cursor.execute(query5)
    cursor.execute(query4)
    cursor.execute(query3)
    cursor.execute(query2)
    cursor.execute(query1)
    connection.commit()
    vacuum_db()

def delete_annotator_by_username(username):
    project_id = select_project_id_by_annotator(username)
    task = select_task_by_project_id(project_id)

    connection = connect_to_db()
    cursor = connection.cursor()
    query1 = "DELETE FROM user WHERE username = '{username}'".format(username = username)
    if task == 'pos':
        query2 = "DELETE FROM POS WHERE username = '{username}'".format(username = username)
    if task == 'ner':
        query2 = "DELETE FROM NER WHERE username = '{username}'".format(username = username)
    if task == 'parsing':
        query2 = "DELETE FROM Parsing WHERE username = '{username}'".format(username = username)
    if task == 'textclass':
        query2 = "DELETE FROM TextClass WHERE username = '{username}'".format(username = username)
    if task == 'aspect':
        query2 = "DELETE FROM Aspect WHERE username = '{username}'".format(username = username)

    query3 = "DELETE FROM ReviewNoti WHERE username = '{username}'".format(username = username)

    cursor.execute(query1)
    cursor.execute(query2)
    cursor.execute(query3)
    connection.commit()


############################# UPDATE DATA ###################################
def update_password_by_username(username, password):
    connection = connect_to_db()
    cursor = connection.cursor()
    passwordhash = hashlib.md5(password.encode()).hexdigest()
    query = "UPDATE user SET password = '{passwordhash}' where username = '{username}'".format(passwordhash = passwordhash, username = username)
    cursor.execute(query)
    connection.commit()

############################### HANDLE INPUT DATA ##############################

# split data to sentences   ----------------------------------------------------
def data_to_sentences(data, language):
    if language == "eng":
        sent_list = en_sent_tokenize(data)
    elif language == "vie":
        sent_list = vie_sent_tokenize(data)
    return sent_list

# split sentence to tokenizes   ------------------------------------------------
def sentence_to_tokens(sent, language):
    if language == "eng":
        word_list = en_word_tokenize(sent)
    elif language == "vie":
        word_list = vie_word_tokenize(sent)
    return word_list


app.run(debug=True)
