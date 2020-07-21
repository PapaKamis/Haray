from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from haray.models import User
from flask_login import current_user
from wtforms.fields.html5 import DateField



class RegistrationForm(FlaskForm):
    firstname = StringField('First name',
                            validators=[DataRequired(), Length(min=2, max=15)])
    lastname = StringField('Last name',
                           validators=[DataRequired(), Length(min=2, max=15)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=15)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=2, max=20)])

    dob = DateField('Date of Birth', format='%Y-%m-%d')

    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('This username already exists. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(username=email.data).first()

        if user:
            raise ValidationError('This email is already registered.')


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=15)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=2, max=20)])
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    firstname = StringField('First name',
                            validators=[DataRequired(), Length(min=2, max=15)])
    lastname = StringField('Last name',
                           validators=[DataRequired(), Length(min=2, max=15)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=15)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    dob = DateField('Date of Birth', format='%Y-%m-%d')

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update Info')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username already exists. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(username=email.data).first()
            if user:
                raise ValidationError('This email is already registered.')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
