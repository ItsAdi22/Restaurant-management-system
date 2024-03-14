from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,HiddenField, DateField, URLField, SelectField, RadioField, IntegerField, EmailField, FileField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    userName = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confpass = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class BeverageForm(FlaskForm):
    item = HiddenField('Item')
    price = HiddenField('Price')
    submit = SubmitField('Add to cart')