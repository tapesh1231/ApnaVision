from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from flask_wtf.file import FileField, FileAllowed

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class DeviceForm(FlaskForm):
    name = StringField('Device Name', validators=[DataRequired()])
    device_type = SelectField('Device Type', 
                             choices=[('light', 'Light'), 
                                     ('fan', 'Fan'), 
                                     ('ac', 'AC'), 
                                     ('other', 'Other')],
                             validators=[DataRequired()])
    submit = SubmitField('Add Device')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
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

class AdvancedDeviceForm(FlaskForm):
    name = StringField('Device Name', validators=[DataRequired()])
    device_type = SelectField('Device Type', 
                            choices=[('light', 'Light'), 
                                    ('fan', 'Fan'), 
                                    ('ac', 'AC'), 
                                    ('sensor', 'Sensor'),
                                    ('other', 'Other')],
                            validators=[DataRequired()])
    ip_address = StringField('IP Address', validators=[DataRequired()])
    location = StringField('Location')
    submit = SubmitField('Add Device')

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    about_me = StringField('About me', validators=[Length(max=140)])
    profile_image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')