from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import *

class ProfileForm(FlaskForm):
    firstname              = StringField('firstname', validators=[DataRequired()])
    lastname               = StringField('signup_email',  validators=[InputRequired()])