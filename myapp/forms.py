from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField('SJSU Email', validators=[DataRequired()])
    password = PasswordField('Password')
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')

class RegisterForm(FlaskForm):
    email = StringField('SJSU Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeatPassword = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class GrantModeratorForm(FlaskForm):
    email = StringField('SJSU Email', validators=[DataRequired()])
    status = BooleanField('Moderator')
    submit = SubmitField('Grant')

class AddProfessorForm(FlaskForm):
    image = StringField('Image Link')
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('SJSU Email', validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    submit = SubmitField('Submit')