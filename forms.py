from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, TextAreaField, SelectField, EmailField, IntegerField
from wtforms.validators import DataRequired, Email, Length, InputRequired, EqualTo, NumberRange, URL


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
    table_no = IntegerField('Table No', validators=[DataRequired()])
    message = TextAreaField('Message', render_kw={'rows': 3}, description='Leave empty if you don\'t want to send any custom message')
    submit = SubmitField('Submit')

# admin section forms
    
class AddFoodForm(FlaskForm):
    foodtitle = StringField('Title', validators=[InputRequired()])
    fooddescription = StringField('Description', validators=[InputRequired()])
    foodurlimage = StringField('Image URL', validators=[InputRequired(), URL()])
    foodprice = IntegerField('Price', validators=[InputRequired(), NumberRange(min=0)])
    method = SelectField('Category', choices=[('/beverages', 'Beverages'), ('/breakfast', 'Breakfast'), ('/lunch', 'Lunch / Dinner')], validators=[InputRequired()])
    submit = SubmitField('Submit')

class DeleteFoodForm(FlaskForm):
    form_type = HiddenField('Form Type', validators=[InputRequired()], render_kw={"value": "admin_delfood"})
    foodName = StringField('Food Item Title', validators=[InputRequired()])
    foodCategory = SelectField('Category', choices=[('beverages', 'Beverages'), ('breakfast', 'Breakfast'), ('lunch', 'Lunch / Dinner')], validators=[InputRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Delete', render_kw={"class": "btn btn-danger form-control"})

class StripeKeysForm(FlaskForm):
    stripeApiKey = StringField('Stripe Api Key', validators=[InputRequired()])
    stripePubKey = StringField('Stripe Publishable Key', validators=[InputRequired()])
    submit = SubmitField('Submit')