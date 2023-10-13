from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from application.utils import exists_email, not_exists_email, exists_username

class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min = 4), exists_username])
    fullname = StringField("Fullname", validators=[DataRequired(), Length(min = 4)])
    email = EmailField("Email", validators=[DataRequired(), Length(min = 8)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min = 8)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message = "Password must match!")])
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class EditProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), exists_username])
    fullname = StringField("Fullname", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), exists_email])
    password = PasswordField("Password", validators=[DataRequired()])
    profile_pic = FileField("Bio", validators=[FileAllowed(["jpg", "png", "jpeg"])])
    bio = StringField("Bio", validators=[DataRequired()])
    submit = SubmitField("Update Profile")

class ResetPasswordForm(FlaskForm):
    old_password = PasswordField("Old Password", validators=[DataRequired(), Length(min=8)])
    new_password        = PasswordField("New Password", validators=[DataRequired(), Length(min=8)])
    confirm_new_password = PasswordField("Confirm New Password", validators=[DataRequired(), Length(min=8), EqualTo("new_password")])
    submit              = SubmitField("Reset Password")

class ForgotPasswordForm(FlaskForm):
    email = PasswordField("Email", validators=[DataRequired(), not_exists_email])
    recaptcha = RecaptchaField()
    submit = SubmitField("Send verification link to email")

class VerificationResetPasswordForm(FlaskForm):
    password        = PasswordField("New Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm New Password", validators=[DataRequired(), Length(min=8), EqualTo("new_password")])
    submit = SubmitField("Reset Password")

class CreatePostForm(FlaskForm):
    post = FileField("picture", validators=[DataRequired(), FileAllowed(["jpg", "png", "jpeg"])])
    caption = StringField("Caption")
    submit = SubmitField("Upload Post")
    
class EditPost(FlaskForm):
    caption = StringField("New Caption")    
    submit = SubmitField("Update Note")