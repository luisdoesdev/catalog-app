from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])

class DeleteForm(FlaskForm):
    pass
