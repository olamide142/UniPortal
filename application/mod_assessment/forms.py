from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, TextAreaField, FileField
from wtforms.validators import DataRequired

class AssessmentForm(FlaskForm):
    title       = StringField('title', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    file        = FileField('file', validators=[DataRequired()])
    due_date    = DateField('due_date', validators=[DataRequired()])
    due_time    = TimeField('due_time', validators=[DataRequired()])