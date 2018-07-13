import sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.sqlite import BLOB
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask import session
from flask import Flask, session
from werkzeug.security import check_password_hash, generate_password_hash
# app = Flask(__name__)
# app.config.from_object(Config)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Default1@localhost/test'
# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
# # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
# db = SQLAlchemy(app)


app = Flask(__name__)
# csrf = CSRFProtect(app)
app.secret_key = '123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Default1@localhost/test'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(120), index=False, unique=False, nullable=False)
    lastname = db.Column(db.String(120), index=False, unique=False, nullable = False)
    email = db.Column(db.String(120), index=False, unique=True, nullable = False)
    password = db.Column(db.String(128))


class loggin_details(db.Model):
    __tablename__='loggin_details'
    timeid = db.Column(db.Integer, primary_key = True)
    login_time = db.Column(db.DateTime, index=True, unique=False, nullable=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='SET NULL'))


class path_details(db.Model):
    __tablename__ = 'path_details'
    id = db.Column(db.Integer, primary_key = True)
    path = db.Column(db.Text())
    today = db.Column('date', db.Date, nullable=False)       # 'date' actually means for column name within the path_details table
    path_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='SET NULL'))

