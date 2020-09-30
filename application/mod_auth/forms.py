from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import *

class SignupForm(FlaskForm):
    username = StringField('username', validators=[DataRequired("Username can't be empty")])
    email = StringField('email',  validators=[InputRequired("Please enter your email address.")])
    first_name = StringField('first_name', validators=[DataRequired("Firstname can't be empty")])
    last_name = StringField('last_name', validators=[DataRequired("Lastname can't be empty")])
    password = StringField('password', validators=[DataRequired("Paaword can't be empty")])


class SigninForm(FlaskForm):
    username = StringField('username', validators=[DataRequired("Username can't be empty")])
    password = StringField('password', validators=[DataRequired("Password can't be empty")])