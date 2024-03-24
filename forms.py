from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, TextAreaField, SelectField, EmailField, IntegerField
from wtforms.validators import Email, Length, InputRequired, EqualTo, NumberRange, URL

class SignupForm(FlaskForm):
    name = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    confpass = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class MenuForm(FlaskForm):
    item = HiddenField('Item',validators=[InputRequired()])
    submit = SubmitField('Add to cart')

class PaymentForm(FlaskForm):
    orderingType = SelectField('Ordering Type', choices=[('On premise', 'On premise'), ('Takeaway', 'Takeaway'), ('Delivery', 'Delivery')], validators=[InputRequired()])
    payVia = SelectField('Pay Via', choices=[('Credit/Debit Card', 'Credit/Debit Card')], validators=[InputRequired()])
    table_no = IntegerField('Table No', validators=[InputRequired()])
    message = TextAreaField('Message', render_kw={'rows': 3}, description='Leave empty if you don\'t want to send any custom message')
    submit = SubmitField('Submit')

#################################### ADMIN ROUTE FORMS BEGINS ####################################
    
class AddFoodForm(FlaskForm):
    foodtitle = StringField('Title', validators=[InputRequired()])
    fooddescription = StringField('Description', validators=[InputRequired()])
    foodurlimage = StringField('Image URL', validators=[InputRequired(), URL()])
    foodprice = IntegerField('Price', validators=[InputRequired(), NumberRange(min=10)])
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

class MarketingForm(FlaskForm):
    subject = StringField('Subject', validators=[InputRequired()], render_kw={"placeholder": "Try our delicious new menu items today!"})
    message = TextAreaField('Message', validators=[InputRequired()], render_kw={"placeholder": "Dear valued customers,\n\nWe are excited to announce that we have added some new and delicious menu items to our restaurant! Come and try our mouth-watering new dishes that are sure to satisfy your taste buds.\n\nWhether you're in the mood for a juicy burger, a hearty pasta dish, or a fresh salad, we've got something for everyone. Our talented chefs have been hard at work creating these new menu items, and we can't wait for you to try them.\n\nSo why not stop by our restaurant today and experience our delicious new menu for yourself? We promise you won't be disappointed!\n\nThank you for your continued patronage.\n\nSincerely,\n[Your Restaurant Name]"})
    submit = SubmitField('Send Email!')

class CompleteOrderForm(FlaskForm):
    form_type_add = HiddenField("Form Type", default="form4",validators=[InputRequired()])
    stripeid = HiddenField('Stripe ID', validators=[InputRequired()])
    submit = SubmitField('Complete Order')

class DeleteOrderForm(FlaskForm):
    form_type_del = HiddenField("Form Type", default="form5",validators=[InputRequired()])
    stripeid = HiddenField('Stripe ID', validators=[InputRequired()])
    submit = SubmitField('Delete Order')

class LoginAsUserForm(FlaskForm):
    form_type_loginuser = HiddenField()
    loginas_name = HiddenField(validators=[InputRequired()])
    loginas_email = HiddenField(validators=[InputRequired(), Email()])
    submit = SubmitField('Login as user')

class DeleteUserAccForm(FlaskForm):
    form_type_deluser = HiddenField(default="admin_deluseracc",validators=[InputRequired()])
    deluserMail = HiddenField(validators=[InputRequired()])
    submit = SubmitField('Delete Account', render_kw={"class": "btn btn-danger"})

class AddAdminAccForm(FlaskForm):
    form_type_addadmin = HiddenField(default="admin_AddAddAcc",validators=[InputRequired()])
    newAdminName = StringField('Username', validators=[InputRequired()], render_kw={"class": "form-control", "placeholder": "username"})
    newAdminEmail = EmailField('Admin Email', validators=[InputRequired(), Email()], render_kw={"class": "form-control", "placeholder": "Admin Email"})
    submit = SubmitField('Create Account', render_kw={"class": "btn btn-primary"})

class DelAdminAccForm(FlaskForm):
    form_type_deladmin = HiddenField('admin_delAddacc',validators=[InputRequired()])
    delAddMail = HiddenField('Email',validators=[InputRequired(), Email()])
    submit = SubmitField('Delete Account', render_kw={"class": "btn btn-danger"})

#################################### ADMIN ROUTE FORMS ENDS ####################################
    
class AdminLoginForm(FlaskForm):
    adminUsername = StringField('Username', validators=[InputRequired()],render_kw={"placeholder": "Enter your username"})
    adminPassword = PasswordField('Password', validators=[InputRequired()],render_kw={"placeholder": "Enter your password"})
    submit = SubmitField('Submit')

class AdminRegistForm(FlaskForm):
    setUsername = StringField('Set Username', validators=[InputRequired()], render_kw={"placeholder": "Set Username"})
    setEmail = EmailField('Set Email', validators=[InputRequired(), Email()], render_kw={"placeholder": "Set Email"})
    setPassword = PasswordField('Set Password', validators=[InputRequired()], render_kw={"placeholder": "Set Password"})
    submit = SubmitField('Submit')

class AdminOTPForm(FlaskForm):
    formotp = IntegerField('Enter OTP', validators=[InputRequired()], render_kw={"placeholder": "Enter OTP"})
    submit = SubmitField('Submit')

class AdminForgetPassForm(FlaskForm):
    adminforgetMail = EmailField('Email', validators=[InputRequired(), Email()], render_kw={"placeholder": "Enter your email"})
    submit = SubmitField('Submit')

class AdminForgetPassOTPForm(FlaskForm):
    form_type_forgetotp = HiddenField('Form Type', default='admin_forgetOTP')
    formotp = IntegerField('Enter OTP', validators=[InputRequired()], render_kw={"placeholder": "Enter OTP"})
    submit = SubmitField('Submit')

class AdminSetNewPassForm(FlaskForm):
    newPass = PasswordField('Set New Password', validators=[InputRequired()], render_kw={"placeholder": "Set New Password"})
    newConfPass = PasswordField('Confirm New Password', validators=[InputRequired(), EqualTo('newPass', message='Passwords must match')], render_kw={"placeholder": "Confirm New Password"})
    submit = SubmitField('Submit')