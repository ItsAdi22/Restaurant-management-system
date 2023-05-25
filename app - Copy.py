from flask import Flask, render_template, url_for, redirect, request, session, flash
from flask_mysqldb import MySQL
from flask_mail import Mail,Message
import re
import stripe
import datetime
import random

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

app = Flask(__name__)

tableno = None
additionalNote = None
otp = None

app.config["SECRET_KEY"] = "CAFE_SECRET"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "hoteltest"

app.config['MAIL_DEFAULT_SENDER'] = 'Vintage Cafe <emailfortestpurpose0@gmail.com>'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'emailfortestpurpose0@gmail.com'
app.config['MAIL_PASSWORD'] = 'hlxjlodkamntudcq'

mysql = MySQL(app)
mail = Mail(app)

def sendemail(email,body,subject):
   try:
      msg = Message('New login detected', recipients=[email], body=body)
      mail.send(msg)
      print('Login Email Sent')

   except Exception as e:
      return render_template('error.html',e=e)     
   

@app.route('/')
def index():
   return render_template('index.html',title='Cafe')


@app.route('/beverages',methods=['GET','POST'])
def coffee():
   if request.method=='POST':
      coffeetitle = request.form.get('coffeetitle')
      coffeedescription = request.form.get('coffeedescription')
      coffeeurlimage = request.form.get('coffeeurlimage')
      coffeprice = request.form.get('coffeprice')

      try:
         cursor = mysql.connection.cursor()
         cursor.execute("CREATE TABLE IF NOT EXISTS coffee (user_id INT AUTO_INCREMENT PRIMARY KEY ,title VARCHAR(255), description VARCHAR(255), imagelink VARCHAR(255),price INT(255));")
      except Exception as e:
         return render_template("error.html",e=e)   
         
      else:
         sql = "INSERT INTO coffee(title,description,imagelink,price) VALUES(%s,%s,%s,%s)"
         value = (coffeetitle,coffeedescription,coffeeurlimage,coffeprice)
         cursor.execute(sql,value)
         mysql.connection.commit()
         cursor.close()
         return redirect(url_for('coffee'))
   else:

      try:
         cursor = mysql.connection.cursor()
         cursor.execute("SELECT title,description,imagelink,price FROM coffee")
         value = cursor.fetchall()
         cursor.close()
         
         if not value:
            flash("No Items In The Menu!")
            return redirect(request.referrer)
         else:
            return render_template('coffee.html', value=value)


      except Exception as e:
         return render_template("error.html",e=e)


@app.route('/breakfast',methods=['GET','POST'])
def breakfast():
   if request.method=='POST':
      breaktitle = request.form.get('breaktitle')
      breakdescription = request.form.get('breakdescription')
      breakurlimage = request.form.get('breakurlimage')
      breakfastprice = request.form.get('breakfastprice')

      cursor = mysql.connection.cursor()
      try:
         cursor.execute("CREATE TABLE IF NOT EXISTS breakfast (user_id INT AUTO_INCREMENT PRIMARY KEY ,title VARCHAR(255), description VARCHAR(255), imagelink VARCHAR(255),price INT(255));")
      finally:
         sql = "INSERT INTO breakfast(title,description,imagelink,price) VALUES(%s,%s,%s,%s)"
         value = (breaktitle,breakdescription,breakurlimage,breakfastprice)
         cursor.execute(sql,value)
         mysql.connection.commit()
         cursor.close()
         return redirect(url_for('breakfast'))
   else:
      try:
         cursor = mysql.connection.cursor()
         cursor.execute("SELECT title,description,imagelink,price FROM breakfast")
         value = cursor.fetchall()
         cursor.close()
         if not value:
            flash("No Items In The Menu!")
            return redirect(request.referrer)
            
         else:
            return render_template('breakfast.html', value=value)

      except Exception as e:
         return render_template("error.html",e=e)


@app.route('/lunch',methods=['GET','POST'])
def lunch():
   if request.method=='POST':
      lunchtitle = request.form.get('lunchtitle')
      lunchdescription = request.form.get('lunchdescription')
      lunchurlimage = request.form.get('lunchurlimage')
      lunchprice = request.form.get('lunchprice')
      cursor = mysql.connection.cursor()
      try:
         cursor.execute("CREATE TABLE IF NOT EXISTS lunch (user_id INT AUTO_INCREMENT PRIMARY KEY ,title VARCHAR(255), description VARCHAR(255), imagelink VARCHAR(255),price INT(255));")

      except Exception as e:
         return str(e)
      finally:
         sql = "INSERT INTO lunch(title,description,imagelink,price) VALUES(%s,%s,%s,%s)"
         value = (lunchtitle,lunchdescription,lunchurlimage,lunchprice)
         cursor.execute(sql,value)
         mysql.connection.commit()
         cursor.close()
         return redirect(url_for('lunch'))
   else:
      
      try:
         cursor = mysql.connection.cursor()
         cursor.execute("SELECT title,description,imagelink,price FROM lunch")
         value = cursor.fetchall()
         cursor.close()

         if not value:
            flash("No Items In The Menu!")
            return redirect(request.referrer)
         else:
            return render_template('lunch.html', value=value)

      except Exception as e:
         return render_template("error.html",e=e)


@app.route('/addtocart',methods=["GET","POST"])
def addtocart():
      if request.method == 'POST':
         item = request.form['item']
         price = request.form['price']
         
         try:
            email = session['email']

         except Exception as e:
            flash("Please login to add items in cart")
            return redirect(url_for('login'))
         
         try:
            cursor = mysql.connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS cart (id INT AUTO_INCREMENT PRIMARY KEY ,item VARCHAR(255), quantity int(255), price INT(255) ,total INT(255), email VARCHAR(255))")

         except Exception as e:
            return render_template('error.html',e=e)
         
         else:
            cursor.execute("SELECT item FROM cart WHERE email = %s AND item = %s", (email,item))
            item_found = cursor.fetchone()

            if item_found is not None:
               cursor.execute("SELECT quantity FROM cart WHERE email = %s AND item = %s", (email, item))
               quantity_db = cursor.fetchone()
               quantity_db_formatted = quantity_db[-1]

               newQuantity = quantity_db_formatted + 1
               cursor.execute("UPDATE cart SET quantity = %s WHERE item = %s", (newQuantity, item))
               
               newTotal = int(float(price) * int(newQuantity))
               cursor.execute("UPDATE cart SET total = %s WHERE item = %s", (newTotal, item))
              
               mysql.connection.commit()
               

            else:   
               quantity = 1
               sql = "INSERT INTO cart(item,quantity,price,total,email) VALUES(%s,%s,%s,%s,%s)"
               value = (item,quantity,price,int(quantity*price),email)
               cursor.execute(sql,value)
               mysql.connection.commit()
               
               session['ecart'] = 'empty_cart'

            cursor.execute("SELECT SUM(quantity) FROM cart WHERE email = %s", (email,))
            tQuantity = cursor.fetchone()
            tQuantityFmt = tQuantity[0]
            print(tQuantityFmt)
         session['tQuantityFmt'] = tQuantityFmt   
         cursor.close()
         flash(f'{item} added to cart')
         return redirect(request.referrer)
      else:
         return redirect(url_for('cart'))      

@app.route('/cart')
def cart():
   if 'name' in session:         
      try:
         email = session['email']
         cursor = mysql.connection.cursor()
         
         #stripe publishable key
         cursor.execute("SELECT pubkey FROM stripekeys")
         pubkey = cursor.fetchone()
         
         if pubkey is not None:
            pubkey_formatted = pubkey[-1]

         elif pubkey is None:
            pubkey_formatted = 'None'
            flash("Payment Gateway is not configured ")
         
         cursor.execute('SELECT item FROM cart WHERE email = %s',(email,))
         item = cursor.fetchall()
         print("item is: ",item)
         
         if item:
            session['ecart'] = 'empty_cart'

         cursor.execute('SELECT quantity FROM cart WHERE email = %s',(email,))
         quantity = cursor.fetchall()
         
         cursor.execute('SELECT price FROM cart WHERE email = %s',(email,))
         price = cursor.fetchall()

         cursor.execute('SELECT total FROM cart WHERE email = %s',(email,))
         total = cursor.fetchall()

         cursor.execute('SELECT SUM(total) FROM cart WHERE email = %s',(email,))
         total_column = cursor.fetchone()

         return render_template("cart.html",item=item,quantity=quantity,price=price,total=total,total_column=total_column,pubkey_formatted=pubkey_formatted)

      except Exception as e:
         return render_template("error.html",e=e)

   elif not'name' in session:
      return redirect(url_for('login'))


@app.route('/empty')
def empty():
         try:
            email = session['email']
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT item,price FROM cart WHERE email = %s',(email,))
            emptycart = cursor.fetchall()

            if emptycart:
                cursor.execute('DELETE FROM cart WHERE email = %s',(email,))
                mysql.connection.commit()
                session.pop('ecart',None)
                session.pop('tQuantityFmt',None)
                flash('Cart has been cleared!')
                

                return redirect(request.referrer)
            else:
                flash('Could not empty the cart')
                
                return redirect(url_for('cart'))
         except Exception as e:
            return render_template('error.html', e=e)


@app.route('/myorders')
def myorders():
    if 'name' in session:
        email = session['email']
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT item FROM orders WHERE email = %s", (email,))
            item = cursor.fetchall()
            
            cursor.execute("SELECT price FROM orders WHERE email = %s", (email,))
            price = cursor.fetchall()

            cursor.execute("SELECT stripeid FROM orders WHERE email = %s", (email,))
            stripeid = cursor.fetchall()
            return render_template('myorders.html', item=item,price=price, stripeid=stripeid)
        except Exception as e:
            return render_template("error.html", e=e)
      

@app.route('/admin/login',methods=['POST','GET'])
def adminlogin():
   if 'admin' not in session:
      if request.method == 'POST':
         adminUsername = request.form['adminUsername']
         adminPassword = request.form['adminPassword']
         
         try:
            cursor = mysql.connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS adminusers (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), adminmail VARCHAR(255), password VARCHAR(255), verified VARCHAR(255))")
            cursor.execute('SELECT * FROM adminusers')
            
         except Exception as e:
            flash("Database Error: " + str(e))
            return redirect(request.referrer)
         else:
            adminfound = cursor.fetchone()
            if adminfound is not None:
               print("admins: ",adminfound)
               cursor.execute('SELECT adminmail FROM adminusers WHERE username = %s AND password IS NOT NULL AND password = %s', (adminUsername, adminPassword,))
               adminlogged = cursor.fetchone()
               if adminlogged:
                  adminMail = adminlogged[0]
                  session['admin'] = adminMail
                  print(f"Admin session started as: {adminMail}")
               else:
                  flash("Incorrect Email/Password")
               
               return redirect(url_for('admin'))
            else:
               flash("No admin accounts exists")
               return render_template('adminlogin.html',noacc=True)
      else:
         return render_template('adminlogin.html')
   else:
      return redirect(url_for('admin'))

@app.route('/adminauth',methods=['POST','GET'])
def adminauth():
   if request.method == 'POST':
      adminUsername = request.form['setUsername']
      adminEmail = request.form['setEmail']
      adminPassword = request.form['setPassword']

      try:
         cursor = mysql.connection.cursor()
         sql = "INSERT INTO adminusers(username,adminmail,password,verified) VALUES(%s,%s,%s,%s)"
         value = (adminUsername,adminEmail,adminPassword,0)
         cursor.execute(sql,value)
         mysql.connection.commit()
         cursor.close()
         flash("Admin account created successfully!")

      except Exception as e:
         return render_template('error.html',e=e)

      else:
         return redirect(url_for('admin'))
   else:
      return redirect(url_for('admin'))

@app.route('/admin/verify',methods=['POST','GET'])
def verifyadmin():
   if 'admin' in session:
      adminMail = session.get('admin')
      global otp
      if request.method == 'POST':
         formotp = request.form['formotp']
         try:

            if int(formotp) == otp:
               try:
                  cursor = mysql.connection.cursor()
                  cursor.execute('UPDATE adminusers SET verified = True WHERE adminmail = %s',(adminMail,))
                  cursor.fetchone()
               except Exception as e:
                  flash(str(e))
                  return redirect(request.referrer)
               else:
                  mysql.connection.commit()
                  cursor.close()
                  flash("Your account is now verified!")
            
                  return redirect(url_for('admin'))
            else:
               flash(f"OTP IS INVALID!, Please check your inbox for new OTP")
               return redirect(url_for('admin'))
         
         except Exception as e:
            flash("Please enter integer value")
            return redirect(url_for('verifyadmin'))

      else:
      
         try:
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT verified from adminusers WHERE adminmail = %s ',(adminMail,))
            isVerified = cursor.fetchone()
            isVerifiedFormatted = isVerified[0]

         except Exception as e:
            flash(str(e))
            return redirect(url_for('admin'))

         else:
            if isVerifiedFormatted == str(0):
               otp = random.randint(100000, 999999)
               print('otp is', otp)

               try:
                  body = f'Your Otp: {otp}'
                  msg = Message('Vintage Cafe OTP', recipients=[adminMail], body=body)
                  mail.send(msg)
                  print('OTP SENT!')

               except Exception as e:
                  flash(str(e))
                  return redirect(url_for('admin'))
               else:
                  flash(f"Otp has been sent to the following email: {adminMail}")
                  return render_template('adminotp.html')  
            else:
               flash("Your account is already verified!")
               return redirect(url_for('admin'))
   else:
      return redirect(url_for('index'))


@app.route('/adminout',methods=['POST','GET'])
def adminout():
   if request.method == 'POST':
      session.pop('admin',None)
      return redirect(url_for('adminlogin'))
   else:
      return redirect(url_for('index'))


@app.route('/admin/forget-pass',methods=['GET','POST'])
def forgetpass():

   if request.method == 'POST':   
      adminforgetMail = request.form['adminforgetMail']      
      
      try:
         cursor = mysql.connection.cursor()
         cursor.execute('SELECT * FROM adminusers where adminmail = %s',(adminforgetMail,))
         adminAccExists = cursor.fetchone()
         print(f'**********AdminAccExists: {adminAccExists}**********')

      except Exception as e:
         flash(str(e))
         return redirect(request.referrer)

      else:
         if adminAccExists is not None:
            
            try:
               session['forgetmail'] = adminforgetMail
               global otp
               otp = random.randint(100000, 999999)
               body = f'Your Otp: {otp}'
               msg = Message('Vintage Cafe OTP', recipients=[adminforgetMail], body=body)
               mail.send(msg)
               print('OTP SENT!')

            except Exception as e:
               flash(str(e))
               return redirect(url_for('admin'))
         
            else:
               flash(f"Otp to reset password has been sent to the following email: {adminforgetMail}")
            return render_template('adminforgetotp.html')  
         
         else:
            flash("Admin account does not exists.")
            return redirect(url_for('forgetpass'))

   else:
      flash("We will send you OTP on your email for verification")
      return render_template('adminforget.html')
      

@app.route('/admin/forget-pass/verify',methods=['POST','GET'])
def otpverify():
   if request.method == 'POST':
      formotp = request.form.get('formotp')
      global otp

      if otp == int(formotp):
         print("OTP VERIFIED SUCCESSFULLY!!!")
         return render_template('adminsetnewpass.html')
      else:
         flash("Invalid OTP")
         return redirect(url_for('forgetpass'))
   else:
      return redirect(url_for('admin'))


@app.route('/admin/set-new-pass',methods=['POST','GET'])
def setnewpass():
   if request.method == 'POST':
      newpass = request.form.get("newPass")
      newConfPass = request.form.get("newConfPass")
      
      if str(newpass) == str(newConfPass):  
         sessionForgetMail = session.get('forgetmail')
         print(f'sessionforgetmail is {sessionForgetMail} *********************************')
         
         try:
            cursor = mysql.connection.cursor()
            sql = 'UPDATE adminusers SET password = %s  Where adminmail = %s'
            cursor.execute(sql, (newpass, sessionForgetMail))
            mysql.connection.commit()
         
         except Exception as e:
            flash(str(e))
            return redirect(request.referrer)

         else:
            cursor.execute('SELECT username FROM adminusers where adminmail = %s',(sessionForgetMail,))
            username = cursor.fetchone()
            usernamefmt = username[0]
            
            body = f'''Admin Password has been successfully updated
            
            Admin Credentials:
            
            username: {usernamefmt}
            password: Your Password
            '''
            msg = Message('Vintage Cafe | Admin Password Updated', recipients=[sessionForgetMail], body=body)
            mail.send(msg)
            session.pop('forgetmail',None)
            session.pop('admin',None)

            flash("Admin Password updated Successfully!")

            return redirect(url_for('admin'))

      else:
         flash("Password doesn't match with confirm password field !")
         return redirect(url_for('forgetpass'))
   
   else:
      return redirect(url_for('admin'))


@app.route('/admin')
@app.route('/admin/')
def admin():
   if 'admin' in session:
      adminMail = session.get('admin')
      try:
         cursor = mysql.connection.cursor()
         cursor.execute('SELECT verified from adminusers WHERE adminmail = %s ',(adminMail,))
         isVerified = cursor.fetchone()
         isVerifiedFormatted = isVerified[0]
         
      except Exception as e:
         return render_template("error.html",e=e)

      else:
         if isVerifiedFormatted == str(0):
            return redirect(url_for('verifyadmin'))

   #create table and fetch stripe keys
      try:
         cursor.execute("CREATE TABLE IF NOT EXISTS stripekeys (id INT AUTO_INCREMENT PRIMARY KEY, apikey VARCHAR(255), pubkey VARCHAR(255))")
         cursor.execute('SELECT apikey,pubkey from stripekeys')
         keys = cursor.fetchone()

      except Exception as e:
         return render_template('error.html',e=e)
      else:
         if keys is not None:
            apikey = keys[0]   
            pubkey = keys[1]   

         else:
            apikey = 'Enter_api_key'
            pubkey = 'Enter_public_key'

      #create table and fetch email auth details
      try:
         cursor.execute("CREATE TABLE IF NOT EXISTS emailauth (id INT AUTO_INCREMENT PRIMARY KEY, mail_default_sender VARCHAR(255), mail_server VARCHAR(255), mail_port INT(100), mail_tls VARCHAR(255), mail_ssl VARCHAR(255), mail_username VARCHAR(255), mail_password VARCHAR(255))")
         cursor.execute('SELECT mail_default_sender, mail_server, mail_port, mail_tls, mail_ssl, mail_username, mail_password from emailauth')
         emailauth = cursor.fetchone()
      except Exception as e:
         return render_template('error.html',e=e)
      else:
         if emailauth is not None:
            mail_default_sender = emailauth[0]
            mail_server = emailauth[1]
            mail_port = emailauth[2]
            mail_tls = emailauth[3]
            mail_ssl = emailauth[4]
            mail_username = emailauth[5]
            mail_password = emailauth[6]
         else:
            mail_default_sender = 'Enter_value_here'
            mail_server = 'Enter_value_here'
            mail_port = 'Enter_value_here'
            mail_tls = 'Enter_value_here'
            mail_ssl = 'Enter_value_here'
            mail_username = 'Enter_value_here'
            mail_password = 'Enter_value_here'


         return render_template('admin.html', title = "Admin",apikey=apikey,pubkey=pubkey,mail_default_sender=mail_default_sender,mail_server=mail_server,mail_port=mail_port,mail_tls=mail_tls,mail_ssl=mail_ssl,mail_username=mail_username,mail_password=mail_password)
   else:
      return redirect(url_for('adminlogin'))  


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',e=e)

    
####################################################################

@app.route('/login',methods=['GET', 'POST'])
def login():


    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            cursor = mysql.connection.cursor()
        except:
            flash("Couldn't connect to the database")
            return render_template('login.html',title = 'Database Error')  
        else:    

            try:
                
               cursor.execute('SELECT * FROM login WHERE email = %s AND password IS NOT NULL AND password = %s', (email, password,))
               account = cursor.fetchone()
               if account:
                     session['email'] = email
                     cursor.execute('SELECT name FROM login WHERE email = %s AND password = %s', (email, password,))
                     username = cursor.fetchone()
                     if username:
                        username_formatted = username[-1]
                        
                        session['name'] = username_formatted
                        
                        #email part
                        ip_address = request.remote_addr
                        now = datetime.datetime.now()
                        current_date = now.strftime("%Y-%m-%d")
                        current_time = now.strftime("%H:%M:%S")
                        name = session.get("name")
                        body = f'''Hello {name},
                              We wanted to inform you that a new login was detected on your account.

                              Details of the login are as follows:
                              - Date: {current_date}
                              - Time: {current_time}
                              - IP Address: {ip_address}

                              If this was not you, please contact us immediately and change your password.
                              '''
                        try:
                           msg = Message('New login detected', recipients=[email], body=body)
                           mail.send(msg)
                           print('Login Email Sent')

                        except Exception as e:
                           return render_template('error.html',e=e)     

                        else:
                           flash("User Loggedin")
                           return redirect(url_for('index'))  
                        
               else:
                  flash("Incorrect Email/Password")
                  return render_template('login.html') 
                        
            except:
                flash("No accounts exist, please create a new account")
                return render_template('register.html') 
    elif 'name' in session:
        return render_template('index.html')  


    return render_template('login.html',title = 'login')

@app.route('/register',methods = ['POST','GET'])
def register():
   if request.method == 'POST':
       name = request.form.get('name') 
       email = request.form.get('email') 
       password = request.form.get('password')
       confpass = request.form.get('confirmpass')
       
       try:
        cursor = mysql.connection.cursor()
       except Exception as e:
        flash(f"Database Error: {e}") 
        return render_template('register.html',title = 'Database Error')  

       else: 
       
         try:
               cursor.execute("CREATE TABLE IF NOT EXISTS login (user_id INT AUTO_INCREMENT PRIMARY KEY ,name VARCHAR(255), email VARCHAR(255), password VARCHAR(255))")
         finally:
            cursor.execute('SELECT * FROM login WHERE email = %s',(email,))
            account = cursor.fetchone()
            if account:
                flash("Email already used! Please use different email address")
                return render_template('register.html')

            # check if name is valid
            elif not re.match(r'[A-Za-z0-9]+', name):
                flash('Enter Valid Name')
                return render_template('register.html',title = 'Enter Valid Name')        

            # check if email is valid
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('Enter Valid Email')
                return render_template('register.html',title = 'Enter Valid Email')

            #check if no data is provided
            elif not name or not email or not password or not confpass:  
                flash('Please fill all the details!')
                return render_template('register.html')

            #check if password and confirm password is correct
            elif (password != confpass):
                flash("password and confirmpassword field should match!")
                return render_template('register.html',title = 'pass should match')

            else:
                sql = "INSERT INTO login(name,email,password) VALUES(%s,%s,%s)"
                value = (name,email,password)
                cursor.execute(sql,value)
                mysql.connection.commit()
                cursor.close()
                flash("User Registration Successful !")
                return redirect(url_for('login'))     

   else:
      return render_template('register.html',title = 'Register')  
        

@app.route('/logout',methods = ['POST','GET'])
def logout():
    # Remove session data, this will log the user out
   session.pop('name', None)
   session.pop('email', None)
   session.pop('ecart',None)
   session.pop('tQuantityFmt',None)
   flash("User Successfully logged out")
   return redirect(url_for('index')) 

####################################################################################

@app.route('/stripe',methods=['POST','GET'])
def stripekeys():
   if request.method == 'POST':
      api_key = request.form['stripeApiKey']
      pub_key = request.form['stripepubKey']

      try:
         cursor = mysql.connection.cursor()
         cursor.execute("CREATE TABLE IF NOT EXISTS stripekeys (id INT AUTO_INCREMENT PRIMARY KEY, apikey VARCHAR(255), pubkey VARCHAR(255))")
      except Exception as e:
        flash("Database Error")
        return render_template('error.html',title = 'Database Error',e=e)  
       
      else: 
         cursor.execute('select * from stripekeys')
         keysfound = cursor.fetchone()
         if keysfound is not None:
            
            if api_key != "":
               sql = "UPDATE stripekeys SET apikey = %s"
               value = (api_key,)
               cursor.execute(sql,value)
               mysql.connection.commit()
            
            elif pub_key != "":
               sql = "UPDATE stripekeys SET pubkey = %s"
               value = (pub_key,)
               cursor.execute(sql,value)
               mysql.connection.commit()
 
            if api_key != "":
               try:
                  stripe.api_key = api_key
                  stripe.Account.retrieve()
               except stripe.error.AuthenticationError as e:
                  flash("STRIPE API KEY IS INVALID")
               
               cursor.close() 
               flash("Stripe keys Updated!")
               return redirect(request.referrer)
         
         else:
            if api_key != "":
               sql = "INSERT INTO stripekeys(apikey) VALUES(%s)"
               value = (api_key,)
               cursor.execute(sql,value)
               mysql.connection.commit()
            
            elif pub_key != "":
               sql = "INSERT INTO stripekeys(pubkey) VALUES(%s)"
               value = (pub_key,)
               cursor.execute(sql,value)
               mysql.connection.commit()
            
         if api_key != "":
            try:
               stripe.api_key = api_key
               stripe.Account.retrieve()
            except stripe.error.AuthenticationError as e:
               flash("STRIPE API KEY IS INVALID")
                  
         cursor.close() 
         flash("Stripe keys added successfully!")
         return redirect(request.referrer)
   else:
      return redirect(url_for('index'))


@app.route('/pay',methods=['POST'])
def create_checkout_session():
   try:
      global tableno
      global additionalNote
      tableno = request.form['tableno']
      additionalNote = request.form['additionalNote']
      cursor = mysql.connection.cursor()
      cursor.execute("SELECT apikey FROM stripekeys")
      
      apikey = cursor.fetchone()
      apikey_formatted = apikey[-1]

      stripe.api_key = apikey_formatted
      
      cartvalue = request.form['totalcartvalue']

      cartvalstripe = (int(cartvalue)*100)
      
      # Create a Stripe checkout session
      session = stripe.checkout.Session.create(
         payment_method_types=["card"],
         mode="payment",
         line_items=[
            {
                  "price_data":{
                     'unit_amount': cartvalstripe,
                     'currency': 'INR',
                     'product_data':{
                        'name': 'Vintage Cafe Order',
                        'description': f'Table No: {tableno}',
                     }
                  },
                  "quantity": 1,
            }
            
         ],
         success_url="http://localhost:80/success?session_id={CHECKOUT_SESSION_ID}",
         cancel_url="http://localhost:80/",
      )

      # Return the checkout session ID
      return session.id    
   
   except Exception as e:
      flash(str(e))
      return redirect(url_for('cart'))

@app.route("/success")
def success():

    # Get the checkout session ID from the query string
    checkout_session_id = request.args.get("session_id")

    # If the checkout session ID is None, redirect to the homepage
    if checkout_session_id is None:
        return redirect("/")

    # Retrieve the checkout session from Stripe
    try:
        session_stripe = stripe.checkout.Session.retrieve(checkout_session_id)
    except stripe.error.InvalidRequestError:
        return render_template("index.html", message="Invalid checkout session ID")    

    # Check the payment status of the checkout session
    if session_stripe.payment_status == "paid":

       try:
        cursor = mysql.connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS orders (id INT AUTO_INCREMENT PRIMARY KEY, item VARCHAR(255), price INT(255), email VARCHAR(255), stripeid VARCHAR(255))")

       except Exception as e:
        flash(f"Database Error: {e}")
        return render_template('login.html',title = 'Database Error')  
       
       else: 
            email = session.get('email')

            cursor.execute('SELECT email,stripeid FROM orders WHERE stripeid IS NOT NULL AND stripeid  = %s',(checkout_session_id,))
            stripeid_exists = cursor.fetchone()

            if stripeid_exists is not None:
                print(f".................. {stripeid_exists}")
                dbemail = stripeid_exists[0]
                stripeid = stripeid_exists[1]
                print("****",dbemail,stripeid)

                if email == dbemail and stripeid == checkout_session_id:
                    flash("Payment Already completed")

                    return redirect(url_for('index'))
    
                elif dbemail != email and stripeid == checkout_session_id:
                    print("database_mail is not equal to email and stripeid is equal to checkout_session_id")
                    return redirect(url_for('index'))

                
            else:    
               cursor.execute('SELECT item FROM cart WHERE email = %s',(email,))
               totalItems = cursor.fetchall()
               itemList = [i[0] for i in totalItems]
               itemList_fmt = f'{itemList}'

               cursor.execute('SELECT SUM(total) FROM cart WHERE email = %s',(email,))
               totalCartVal = cursor.fetchone()
               if totalCartVal is not None:
                  totalCartVal_formatted = totalCartVal[-1]

               elif totalCartVal_formatted is None:
                  cursor.execute('SELECT total FROM cart WHERE email = %s',(email,))
                  totalVal = cursor.fetchone()
                  print(f'total cart val is........ {totalVal}')
                  totalCartVal_formatted = totalVal[-1]
                  

         
               sql = "INSERT INTO orders(item,price,email,stripeid) VALUES(%s,%s,%s,%s)"
               value = (itemList_fmt,totalCartVal_formatted,email,checkout_session_id)
               cursor.execute(sql,value)
               mysql.connection.commit()
               
               flash("Payment Successful")
               name = session.get("name")

               global additionalNote
               global tableno

               if additionalNote == '' or None:
                  additionalNote = 'None'
               
               elif tableno == '' or None:
                  tableno == 'None'

               body=f''' Hello {name},
               Your order has been placed successfully!
               
               Items purchased: {itemList_fmt}
               
               Table No: {tableno}
               Additional Note: {additionalNote}
               
               Amount Paid: {totalCartVal_formatted} Rupees
         
               
               Payment Id: {checkout_session_id}
               Thank You!
               '''
               
               try:
                  msg = Message('Order Placed', recipients=[email], body=body)
                  
                  mail.send(msg)
                  print('Order Email Sent')

               except Exception as e:
                  flash(str(f'Email Error: {e}'))
                  return render_template('error.html',e=e)    
               
               else:
                  empty()
                  cursor.close()
                  return render_template('success.html')


        # Payment was successful, render the success template        
    else:
        # Payment was not successful, redirect to the homepage
        return redirect(url_for('index')) 

####################################################################################

@app.route('/eauth',methods=['POST','GET'])
def emailauthentication():
   if request.method == 'POST':
      mail_default_sender = request.form['mailDefaultSender']
      mail_server = request.form['mailServer']
      mail_port = request.form['mailPort']
      mail_tls = request.form['mailUseTls']
      mail_ssl = request.form['mailUseSsl']
      mail_username = request.form['mailUsername']
      mail_password = request.form['mailPassword']

      try:
         cursor = mysql.connection.cursor()
         # cursor.execute("CREATE TABLE IF NOT EXISTS stripekeys (id INT AUTO_INCREMENT PRIMARY KEY, apikey VARCHAR(255), pubkey VARCHAR(255))")
      except Exception as e:
        flash("Database Error")
        return render_template('error.html',title = 'Database Error',e=e)  
       
      else: 
         cursor.execute('select * from emailauth')
         eauthfound = cursor.fetchone()
         if eauthfound is not None:
            sql = "UPDATE emailauth SET mail_default_sender = %s, mail_server = %s, mail_port = %s, mail_tls = %s, mail_ssl = %s, mail_username = %s, mail_password = %s"
            value = (mail_default_sender,mail_server,mail_port,mail_tls,mail_ssl,mail_username,mail_password)
            cursor.execute(sql,value)
            mysql.connection.commit()
            cursor.close() 
            flash("Email Auth details Updated!")
            return redirect(request.referrer)
         else:
            sql = "INSERT INTO emailauth(mail_default_sender, mail_server, mail_port, mail_tls, mail_ssl, mail_username, mail_password) VALUES(%s,%s,%s,%s,%s,%s,%s)"
            value = (mail_default_sender,mail_server,mail_port,mail_tls,mail_ssl,mail_username,mail_password)
            cursor.execute(sql,value)
            mysql.connection.commit()
            cursor.close() 
            flash("Email Auth details added successfully!")
            return redirect(request.referrer)
   else:
      return redirect(url_for('index'))

if __name__ == '__main__':
   app.run(debug=True, port=80)