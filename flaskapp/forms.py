from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, ValidationError
from flaskapp.models import User, Business

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
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
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RestaurantForm(FlaskForm):
    name = StringField('Restaurant Name',
                        validators=[DataRequired()])
    dish = StringField('What did you order?', validators=[DataRequired()])
    rating = DecimalField('Leave a rating (0 - 5 stars)', validators=[DataRequired(), NumberRange(min=0.0, max=5.0, message="Your rating must be between 0 and 5")])
    review = TextAreaField('Leave a review of your food')
    submit = SubmitField('Enter')

    def validate_name(self, name):
        business = Business.query.filter_by(name=name.data).first()
        if not business:
            raise ValidationError('That restaurant does not exist in the database :( ')
