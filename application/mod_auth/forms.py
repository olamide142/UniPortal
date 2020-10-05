from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import *

class SignupForm(FlaskForm):
    signup_username        = StringField('signup_username', validators=[DataRequired("Username can't be empty")])
    signup_email           = StringField('signup_email',  validators=[InputRequired("Please enter your email address.")])
    signup_firstname      = StringField('signup_firstname', validators=[DataRequired("Firstname can't be empty")])
    signup_lastname       = StringField('signup_lastname', validators=[DataRequired("Lastname can't be empty")])
    signup_password        = StringField('password', validators=[DataRequired("Paaword can't be empty")])


class SigninForm(FlaskForm):
    login_username            = StringField('login_username', validators=[DataRequired("Username can't be empty")])
    login_password            = StringField('login_password', validators=[DataRequired("Password can't be empty")])