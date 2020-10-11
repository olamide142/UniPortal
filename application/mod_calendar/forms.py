from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField
from wtforms.validators import DataRequired

class CreateEventForm(FlaskForm):
    date        = DateField('data', validators=[DataRequired()])
    time        = TimeField('time', validators=[DataRequired()])
    title       = StringField('title', validators=[DataRequired()])
    module_id   = StringField('module_id', validators=[DataRequired()])