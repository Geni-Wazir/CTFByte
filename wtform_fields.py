from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from models import *

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