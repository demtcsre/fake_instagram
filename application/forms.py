from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min = 4, max = 8)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min = 8)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message = "Password must match!")])
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min = 4, max = 8)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min = 1)])
    submit = SubmitField("Login")

class EditProfile(FlaskForm):
    note = StringField("Note", validators=[DataRequired(), Length(min=5)])
    submit = SubmitField("Update Note")

class CreatePost(FlaskForm):
    note = StringField("Username", validators= [DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min = 4)])
    submit = SubmitField("Add Note")
    
class EditPost(FlaskForm):
    note = StringField("Note", validators=[DataRequired(), Length(min=5)])
    submit = SubmitField("Update Note")
