from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class UserForm(FlaskForm):
    full_names = StringField("Full Names", validators=[DataRequired(), Length(min=4, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email(message='Invalid email address')])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo("confirm"), Length(min=8, max=80)])
    confirm = PasswordField('Confirm')
    submit = SubmitField('submit')


class LoginForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(), Email(message="Invalid email address")])
    password = PasswordField("Password", validators=[DataRequired(),Length(min=8, max=80)])
    submit = SubmitField('submit')


class UpdateAccount(FlaskForm):
    full_names = StringField("Full Names", validators=[DataRequired(), Length(min=4, max=50)])
    email = StringField("Email",validators=[DataRequired(), Email(message="Invalid email address")])
    image = FileField("Update File Image",validators=[FileAllowed(['jpg','png','jpeg'])])
    linkedin = StringField("Linkedin")
    twitter = StringField("Linkedin")
    fb = StringField("Linkedin")
    submit = SubmitField('Submit')




