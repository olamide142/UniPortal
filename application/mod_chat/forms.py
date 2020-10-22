from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class ChatForm(FlaskForm):
    # message         = StringField('name', validators=[DataRequired()])
    # description     = TextAreaField('description', validators=[DataRequired()])
    pass