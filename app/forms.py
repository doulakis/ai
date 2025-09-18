from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    """Login form with email/username and password"""
    
    email_or_username = StringField(
        'Email or Username', 
        validators=[DataRequired(), Length(min=3, max=120)]
    )
    password = PasswordField(
        'Password', 
        validators=[DataRequired()]
    )
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """Registration form for new users"""
    
    username = StringField(
        'Username', 
        validators=[
            DataRequired(), 
            Length(min=3, max=20, message='Username must be between 3 and 20 characters')
        ]
    )
    email = StringField(
        'Email', 
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired(), 
            Length(min=8, message='Password must be at least 8 characters long')
        ]
    )
    password_confirm = PasswordField(
        'Confirm Password', 
        validators=[
            DataRequired(), 
            EqualTo('password', message='Passwords must match')
        ]
    )
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        """Check if username is already taken"""
        user = User.get_by_username(username.data)
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email(self, email):
        """Check if email is already registered"""
        user = User.get_by_email(email.data)
        if user:
            raise ValidationError('Email already registered. Please use a different email address.')


class PasswordResetRequestForm(FlaskForm):
    """Form to request password reset"""
    
    email = StringField(
        'Email', 
        validators=[DataRequired(), Email()]
    )
    submit = SubmitField('Request Password Reset')


class PasswordResetForm(FlaskForm):
    """Form to reset password with token"""
    
    password = PasswordField(
        'New Password', 
        validators=[
            DataRequired(), 
            Length(min=8, message='Password must be at least 8 characters long')
        ]
    )
    password_confirm = PasswordField(
        'Confirm Password', 
        validators=[
            DataRequired(), 
            EqualTo('password', message='Passwords must match')
        ]
    )
    submit = SubmitField('Reset Password')