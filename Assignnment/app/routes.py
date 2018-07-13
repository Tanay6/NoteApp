from flask import Flask,Blueprint, jsonify, session, render_template, flash, redirect, url_for, current_app, request, abort, Response
from flask_wtf.csrf import CSRFProtect
from forms import *
from models import *
import datetime
from datetime import date
import base64
import time
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
#from database import db_session
from sqlalchemy import text,desc, update
import os
import os.path
#from os import listdir
import simplejson as json
# csrf_protect = CSRFProtect(app)
# api = restful.Api(app, decorators=[csrf_protect.exempt])

@app.route('/', methods=['GET','POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method =="POST":
        email = request.form['username']
        password = request.form['password']
        current_time = datetime.datetime.now()
        user = User()
        login_details = loggin_details()
        query = user.query.filter_by(email=email).first()
        if query is not None:
            if check_password_hash(query.password, password):
                session['username'] = request.form['username']
                session['user_id'] = query.id
                session['login'] = True
                login_details.login_time = current_time
                login_details.user_id = session['user_id']
                qry = loggin_details.query.filter_by(user_id=session['user_id']).first()
                print(qry)
                if qry is None:
                    db.session.add(login_details)
                    db.session.commit()
                else:
                    loggin_details.query.filter_by(user_id=session['user_id']).update(dict(login_time=current_time))        #remember to use 'dict' as datatype while using update clause(this convention may apply for flask application only 'Not Sure')
                    db.session.commit()
                return redirect(url_for('home_page'))
            return ("Password is not correct!")
        else:
            return redirect(url_for('login'))
    return render_template("index.html",form=form, error = error)
@app.route('/home/',defaults={'id':None})
@app.route('/home/<int:id>', methods=['GET','POST'])
def home_page(id):
    print("------------------Tanay------------------")
    print(id)
    error = None
    if request.method == 'GET':
        print(session)
        if not session['login']:
            print("Or the session is none")
            return redirect(url_for('login'))

        else:
            if id is None:
                print("Is it here??")
                qry = text('select user.id,user.firstname, user.lastname, user.email, loggin_details.login_time as last_time from user join loggin_details where user.id=loggin_details.user_id')
                data = db.engine.execute(qry)
                if data is not None:
                    return render_template("home.html", data=data,return_obj=None, error=error)
                else:
                    print ("No Data Found")
            else:
                #get all Dates of Particular user

                return render_template("home2.html")

    return "keep searching for the website!"

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['login']=False
    return redirect(url_for('login'))

@app.route ('/AjaxHandler/', methods = ['POST'])
def AjaxHandler():
    error = None
    folder_path = path_details()
    current_date = date.today()
    if request.method == 'POST':
        content = request.get_json()
        image = content['image']
        strtime = time.strftime("%Y%m%d-%H%M%S")
        starter = image.find(',')
        image_data = image[starter + 1:]
        image_data = bytes(image_data, encoding="ascii")
        username = session['username']
        today = datetime.datetime.now()
        day = str(today.year)+'.'+str(today.month)+'.'+str(today.day)
        current_dir = os.getcwd()
        stat_path = os.path.join(current_dir,'screenshot')
        new_dir = os.path.join( stat_path,username)
        new_dir1 = os.path.join(new_dir,day)
        print(new_dir1)
        print(new_dir)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        else:
            print('Folder exists!')
        if not os.path.exists(new_dir1):
            os.makedirs(new_dir1)
        else:
            print('Folder exists!')
        with open(new_dir1+"\/"+strtime+'.png', 'wb') as fh:
            fh.write(base64.decodebytes(image_data))
            fh.close()
        folder_path.path = new_dir1
        folder_path.today = current_date
        folder_path.path_id = session['user_id']
        print('-------------------------------------------checking-----------------------')
        print(session['user_id'])
        print(folder_path.path_id)
        db.session.add(folder_path)
        db.session.commit()
        return redirect(url_for('home_page'))
        # else:
        #     print('successfully saved!')
    else:
        return 'Image is not saved into Database!'
@app.route('/image_save/', methods=['GET','POST'])
def image_save():
    error = None
    username = session['username']
    today = datetime.datetime.today()
    current_dir = os.getcwd()
    print(current_dir)
    print('----------------------------------------------directory--------------------------------')
    os.mkdir('screenshot')
    os.chdir('screenshot')
    os.mkdir(username)
    os.chdir(username)
    os.mkdir(today)
    folder_path = os.chdir(today)

    newDir = current_dir + os.mkdir('screenshot')

    newDir1 = newDir.os.mkdir(username)
    newDir2 = os.mkdir(datetime.datetime.date())
    folder_path = os.listdir('newDir2')
    print(folder_path)
    # if request.method == 'POST':
@app.route ('/gallery/', methods=['GET','POST'])
def gallery():
    date_list = text('select date')
@app.route('/signup/', methods=['GET', 'POST'])
def SignUp():
    error = None
    form = SignupForm(request.form)
    info = User()
    # query1 = info.query.filter_by(email=request.form['Email'])
    # if query1 is None:
    if request.method == 'POST':
        if request.form['password'] ==  request.form['password2']:
            # print (request.form['password'])
            info.firstname = request.form['FirstName']
            # print(request.form['FirstName'])
            info.lastname = request.form['LastName']
            info.email = request.form['Email']
            password = generate_password_hash(request.form['password'])
            info.password = password

            db.session.add(info)
            db.session.commit()
            # redirect('/')
            return redirect(url_for('login'))
        else:
            print("Password does not match")
    return render_template("signup.html",title="SignUp", return_obj=None, form=form, error=error)

if __name__ == '__main__':
    db.create_all()
    app.secret_key ="123"
    app.run(host='127.0.0.1',port = 5000, debug=True)





