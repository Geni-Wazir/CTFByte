from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha256
from models import *

# Check for invalid credentials entered by user
def credential_checker(form, field):
    username_entered = form.username.data
    password_entered = form.password.data

    # Check for username validity
    user_object = User.query.filter_by(username=username_entered).first()
    if user_object is None:
        raise ValidationError("Incorrect Username or Password Entered.")
    elif not pbkdf2_sha256.verify(password_entered, user_object.password):
        raise ValidationError("Incorrect Username or Password Entered.")

# Registraion Form Field Descriptors
class RegistrationForm(FlaskForm):
    username = StringField('username_label',validators=[
        InputRequired(message="Username can not be Blank"),
        Length(min=4,max=25,message="Username must be between 4 and 25 characters")
    ])
    password = PasswordField('password_label',validators=[
        InputRequired(message="Password can not be Blank"),
        Length(min=8,max=25,message="Password must be between 8 and 25 characters")
    ])
    confirm = PasswordField('confirm_label',validators=[
        InputRequired(message="Confirm Password can not be Blank"),
        EqualTo('password',message="The Two Passwords Must Match")
    ])
    submit_button = SubmitField('Create')

    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Username already exists! Select a different Username.")

# Login Form Field Dexcriptors        
class LoginForm(FlaskForm):
    username = StringField('username_label',validators=[
        InputRequired(message="Username can not be Blank")
    ])
    password = PasswordField('password_label',validators=[
        InputRequired(message="Password can not be Blank"),
        credential_checker
    ])
    submit_button = SubmitField('Create')