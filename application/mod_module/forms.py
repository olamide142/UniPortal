from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class CreateModuleForm(FlaskForm):
    name        = StringField('name', validators=[DataRequired()])
    session     = StringField('session', validators=[DataRequired()])