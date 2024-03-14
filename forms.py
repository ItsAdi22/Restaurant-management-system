from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,HiddenField, TextAreaField, URLField, SelectField, RadioField, IntegerField, EmailField, FileField
from wtforms.validators import DataRequired, Email, Length, InputRequired, EqualTo


class SignupForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confpass = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class MenuForm(FlaskForm):
    item = HiddenField('Item')
    submit = SubmitField('Add to cart')

class PaymentForm(FlaskForm):
    ordering_type = SelectField('Ordering Type', choices=[('On premise', 'On premise'), ('Takeaway', 'Takeaway'), ('Delivery', 'Delivery')], validators=[DataRequired()])
    pay_via = SelectField('Pay Via', choices=[('Credit/Debit Card', 'Credit/Debit Card')], validators=[DataRequired()])
    table_no = StringField('Table No', validators=[DataRequired()])
    message = TextAreaField('Message', render_kw={'rows': 3}, description='Leave empty if you don\'t want to send any custom message')