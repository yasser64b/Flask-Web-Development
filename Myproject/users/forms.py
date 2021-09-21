# Form Based Imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

# User Based Imports
from flask_login import current_user
from myproject.models import User




class LoginForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()] , render_kw={"placeholder": "Email address"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(),Email()] , render_kw={"placeholder": "Email address"})
    username = StringField('Username', validators=[DataRequired()] , render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')] , render_kw={"placeholder": " passwrod"})
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()] , render_kw={"placeholder": " Confirm password"})
    submit = SubmitField('Register (free)!')

    def validate_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def validate_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')


class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def validate_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')
