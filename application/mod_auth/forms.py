from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import *

class SignupForm(FlaskForm):
    username = StringField('name', validators=[DataRequired("Username can't be empty")])
    email = StringField('Email',  validators=[InputRequired("Please enter your email address.")])
    first_name = StringField('first_name')
    last_name = StringField('last_name')
    password = StringField('password')


