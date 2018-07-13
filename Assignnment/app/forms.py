from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    remember_me = BooleanField('Remember Me')


class SignupForm(FlaskForm):
    FirstName = StringField('FirstName', validators=[DataRequired()])
    LastName = StringField('LastName', validators=[DataRequired()])
    Email = EmailField(label="Email",validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm your password', validators=[DataRequired()])
    #remember_me = BooleanField('Remember Me')

class DeleteForm(FlaskForm):
  submit = SubmitField('Confirm')
#
# <form method="post">
#   {{ form.csrf_token }}
#   {{ form.submit }}
# </form>

class LogoutForm(FlaskForm):
    def __init__(self,arg):
        self.arg = arg





