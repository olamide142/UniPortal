from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class CreateModuleForm(FlaskForm):
    name            = StringField('name', validators=[DataRequired()])
    session         = StringField('session', validators=[DataRequired()])
    code            = StringField('code', validators=[DataRequired()])
    description     = TextAreaField('description', validators=[DataRequired()])


class CreateTopicForm(FlaskForm):
    title           = StringField('title', validators=[DataRequired()])
    description     = TextAreaField('description', validators=[DataRequired()])


