from flask import Flask, render_template, url_for, redirect, request, session, flash
from flask_mysqldb import MySQL
from flask_mail import Mail,Message
from forms import SignupForm, LoginForm, MenuForm, PaymentForm, AddFoodForm, DeleteFoodForm
import re
import stripe
import datetime
import random
import threading
import secrets
import os
from dotenv import load_dotenv

load_dotenv()

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

app = Flask(__name__)

tableno = None
additionalNote = None
otp = None

app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')

app.config["MYSQL_HOST"] = os.getenv('MYSQL_HOST')
app.config["MYSQL_DB"] = os.getenv('MYSQL_DB')
app.config["MYSQL_USER"] = os.getenv('MYSQL_USER')
app.config["MYSQL_PASSWORD"] = os.getenv('MYSQL_PASSWORD')

app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

domain = os.getenv('domain')
port = os.getenv('port')

mysql = MySQL(app)
mail = Mail(app)

def createMissingTables():            
   try:
      cursor = mysql.connection.cursor()
      cursor.execute("CREATE TABLE IF NOT EXISTS orders (id INT AUTO_INCREMENT PRIMARY KEY, item VARCHAR(255), price INT(255), name VARCHAR(255), email VARCHAR(255), stripeid VARCHAR(255), date VARCHAR(255), note VARCHAR(255), tableno INT(255), served INT(255))")
      cursor.execute("CREATE TABLE IF NOT EXISTS cart (id INT AUTO_INCREMENT PRIMARY KEY ,item VARCHAR(255), quantity int(255), price INT(255) ,total INT(255), email VARCHAR(255))")
      cursor.execute("CREATE TABLE IF NOT EXISTS allitems (item VARCHAR(225), quantity INT(225))")
      cursor.execute("CREATE TABLE IF NOT EXISTS beverages (user_id INT AUTO_INCREMENT PRIMARY KEY ,title VARCHAR(255), description VARCHAR(255), imagelink VARCHAR(255),price INT(255));")
      cursor.execute("CREATE TABLE IF NOT EXISTS breakfast (user_id INT AUTO_INCREMENT PRIMARY KEY ,title VARCHAR(255), description VARCHAR(255), imagelink VARCHAR(255),price INT(255));")
      cursor.execute("CREATE TABLE IF NOT EXISTS lunch (user_id INT AUTO_INCREMENT PRIMARY KEY ,title VARCHAR(255), description VARCHAR(255), imagelink VARCHAR(255),price INT(255));")
      cursor.execute("CREATE TABLE IF NOT EXISTS stripekeys (id INT AUTO_INCREMENT PRIMARY KEY, apikey VARCHAR(255), pubkey VARCHAR(255))")
      cursor.execute("CREATE TABLE IF NOT EXISTS login (user_id INT AUTO_INCREMENT PRIMARY KEY ,name VARCHAR(255), email VARCHAR(255), password VARCHAR(255))")
      cursor.execute("CREATE TABLE IF NOT EXISTS emailauth (id INT AUTO_INCREMENT PRIMARY KEY, mail_default_sender VARCHAR(255), mail_server VARCHAR(255), mail_port INT(100), mail_tls VARCHAR(255), mail_ssl VARCHAR(255), mail_username VARCHAR(255), mail_password VARCHAR(255))")
      cursor.execute("CREATE TABLE IF NOT EXISTS adminusers (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), adminmail VARCHAR(255), password VARCHAR(255), verified VARCHAR(255), owner VARCHAR(255))")
   except Exception as e:
      flash(f"Error creating tables: {e}")

# def sendemail(email,body,subject):
#    with app.app_context():
#       msg = Message(subject, recipients=[email], body=body)
#       mail.send(msg)
#       if mail.send(msg):
#          print(f'{subject} | Email Sent')
#       else:
#          flash('AN ERROR OCCURRED')

def sendemail(email, body, subject):
    with app.app_context():
        msg = Message(subject, recipients=[email], body=body)
        try:
            mail.connect()
            mail.send(msg)
            print(f'{subject} | Email Sent')
        
        except Exception as e:
            with app.test_request_context():
               print(f'An error occurred while sending email to {email}. Error message: {str(e)}')



@app.route('/')
def index():
   return render_template('index.html',title='Cafe')


@app.route('/beverages',methods=['GET','POST'])
def beverages():
   
   if request.method=='POST':
      form = AddFoodForm()
      if form.validate_on_submit():
         coffeetitle = request.form.get('foodtitle')
         coffeedescription = request.form.get('fooddescription')
         coffeeurlimage = request.form.get('foodurlimage')
         coffeprice = request.form.get('foodprice')

         try:
            cursor = mysql.connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS beverages (user_id INT AUTO_INCREMENT PRIMARY KEY ,title VARCHAR(255), description VARCHAR(255), imagelink VARCHAR(255),price INT(255));")
         except Exception as e:
            return render_template("error.html",e=e)   
            
         else:
            sql = "INSERT INTO beverages(title,description,imagelink,price) VALUES(%s,%s,%s,%s)"
            value = (coffeetitle,coffeedescription,coffeeurlimage,coffeprice)
            cursor.execute(sql,value)
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('beverages'))
      else:
         for x in form.errors:
            if x == 'foodurlimage':
               flash("Enter valid URL!")
            
            elif x == 'foodtitle':
               flash("Enter valid title")
            
            elif x == 'fooddescription':
               flash("Enter valid description")

            elif x == 'foodprice':
               flash("Enter valid amount!")

            else:
               flash("Contact Admin: ",x)

            return redirect(request.referrer)
   else:

      try:
         form = MenuForm()
         cursor = mysql.connection.cursor()

         cursor.execute("SELECT title,description,imagelink,price FROM beverages")
         value = cursor.fetchall()
         cursor.close()
         
      except Exception as e:
         return render_template("error.html",e=e)

      else:
         if not value:
            flash("No Items In The Menu!")
            return redirect(request.referrer)
         
         
         return render_template('beverages.html', value=value, form=form)





@app.route('/breakfast',methods=['GET','POST'])
def breakfast():
   form = MenuForm()
   if request.method=='POST':
      breaktitle = request.form.get('foodtitle')
      breakdescription = request.form.get('fooddescription')
      breakurlimage = request.form.get('foodurlimage')
      breakfastprice = request.form.get('foodprice')

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
            return render_template('breakfast.html', value=value, form=form)

      except Exception as e:
         return render_template("error.html",e=e)


@app.route('/lunch',methods=['GET','POST'])
def lunch():
   form = MenuForm()
   if request.method=='POST':
      lunchtitle = request.form.get('foodtitle')
      lunchdescription = request.form.get('fooddescription')
      lunchurlimage = request.form.get('foodurlimage')
      lunchprice = request.form.get('foodprice')
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
            return render_template('lunch.html', value=value, form=form)

      except Exception as e:
         return render_template("error.html",e=e)


@app.route('/addtocart',methods=["GET","POST"])
def addtocart():
      if request.method == 'POST':
         item = request.form['item']
         # price = request.form['price']
         
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
         # Select price based on the item name
            query = (
        "SELECT price FROM beverages WHERE title = %s "
        "UNION "
        "SELECT price FROM breakfast WHERE title = %s "
        "UNION "
        "SELECT price FROM lunch WHERE title = %s"
         )

            cursor.execute(query, (item, item, item))
            results = cursor.fetchall()

            #print(f'the item is: -------> {results} ----> {results[0]} ----> {results[0][0]}')
            
            if results:
                  price = results[0][0]

            else:
               price = 100000
               flash("Please Contact An Administrator")
               print("Please Contact An Administrator")


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
      form = PaymentForm()    
      try:
         email = session['email']
         cursor = mysql.connection.cursor()
         
         #stripe publishable key
         cursor.execute("SELECT pubkey FROM stripekeys")
         pubkey = cursor.fetchone()

         if pubkey is None:
            flash("Please setup Payment Gateway")
            pubkey = 'None'
            pubkey_formatted = 'None'
         else:
            pubkey_formatted = pubkey[-1]

            # this is required to eliminated empty spaces in string
            pubkey_formatted = pubkey_formatted.strip()


         if pubkey_formatted == '' or pubkey_formatted is None:
            flash("Payment Gateway is not configured!")
            pubkey_formatted = 'None'
            
         else: 
            pubkey_formatted = pubkey[0]
           
            print("payment gateway is configured: ",pubkey_formatted)

         
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

         cursor.close()
         return render_template("cart.html",item=item,quantity=quantity,price=price,total=total,total_column=total_column,pubkey_formatted=pubkey_formatted,form=form)

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
                cursor.close()
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
   createMissingTables()
   if 'admin' not in session:
      if request.method == 'POST':
         adminUsername = request.form['adminUsername']
         adminPassword = request.form['adminPassword']
         
         try:
            cursor = mysql.connection.cursor()
            #create missing tables
            cursor.execute('SELECT adminmail FROM adminusers')
            
         except Exception as e:
            flash("Database Error: " + str(e))
            return redirect(request.referrer)
         else:
            adminfound = cursor.fetchall()
            if adminfound is not None and adminfound != tuple(''):
               print(type(adminfound))
               cursor.execute('SELECT adminmail FROM adminusers WHERE username = %s AND password IS NOT NULL AND password = %s', (adminUsername, adminPassword,))
               adminlogged = cursor.fetchone()
               if adminlogged:
                  adminMail = adminlogged[0]
                  session['admin'] = adminMail
                  cursor.close()
                  print(f"Admin session started as: {adminMail}")
               else:
                  flash("Incorrect Username/Password")
               
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
         sql = "INSERT INTO adminusers(username,adminmail,password,verified,owner) VALUES(%s,%s,%s,%s,%s)"
         value = (adminUsername,adminEmail,adminPassword,0,1)
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
            int(formotp)
         except:
               flash("Enter Integer Value")
               return redirect(url_for('verifyadmin'))
         else:
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
               return redirect(request.referrer)

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
                  subject = 'Vintage Cafe OTP'
                  threading.Thread(target=lambda: sendemail(adminMail, body, subject)).start()
                  print('OTP SENT!')

               except Exception as e:
                  flash(str(e))
                  return redirect(url_for('admin'))
               else:
                  flash(f"OTP has been sent to the following email: {adminMail}")
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
               subject = 'Vintage Cafe OTP | Forget Password'
               threading.Thread(target=lambda: sendemail(adminforgetMail, body, subject)).start()

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
            subject = 'Vintage Cafe | Admin Password Updated'
            threading.Thread(target=lambda: sendemail(sessionForgetMail, body, subject)).start()
            session.pop('forgetmail',None)
            session.pop('admin',None)

            flash("Admin Password updated Successfully!")

            return redirect(url_for('admin'))

      else:
         flash("Password doesn't match with confirm password field !")
         return redirect(url_for('forgetpass'))
   
   else:
      return redirect(url_for('admin'))


@app.route('/admin',methods=['POST','GET'])
@app.route('/admin/',methods=['POST','GET'])
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

         if request.method == 'POST':
            form = AddFoodForm()
            form1 = DeleteFoodForm()
            
            if request.form.get('form_type') == 'payment_gateway':
               paymentactive = True
               return render_template('adminpay.html', apikey=apikey,pubkey=pubkey,paymentactive=paymentactive)   
            
            elif request.form.get('form_type') == 'admin_email':
               emailactive = True
               return render_template('adminemail.html', title='Email Auth',mail_default_sender=mail_default_sender,mail_server=mail_server,mail_port=mail_port,mail_tls=mail_tls,mail_ssl=mail_ssl,mail_username=mail_username,mail_password=mail_password,emailactive=emailactive)
         
            elif request.form.get('form_type') == 'admin_food':
               foodactive = True
               return render_template('adminfood.html',title='Manage Food Menu',foodactive=foodactive, form=form, form1=form1)
            
            elif request.form.get('form_type') == 'admin_delfood':
               
               if form1.validate_on_submit() == True:
                  foodName = request.form.get('foodName')
                  foodCategory = request.form.get('foodCategory')
               
                  cursor.execute(f"SELECT title FROM {foodCategory} WHERE title = %s", (foodName,))
                  delFoodFound = cursor.fetchone()
               
                  if delFoodFound is not None:
                     cursor.execute(f"DELETE FROM {foodCategory} WHERE title = %s", (delFoodFound,))
                     mysql.connection.commit()
                     flash(f'{foodName} deleted from the menu!')
                  
                  else:
                     flash(f'{foodName} not found!')

               else:
                  for x in form1.errors:
                     flash(f'Enter valid {x} !')
               cursor.close()      
               foodactive = True
               
               return render_template('adminfood.html',title='Manage Food Menu',foodactive=foodactive, form1=form1, form=form)
            
            elif request.form.get('form_type') == 'admin_marketingNav':
               marketingMail = True
               return render_template("adminmarketing.html",title='Marketing Mails',marketingMail=marketingMail)
            
            elif request.form.get('form_type') == 'admin_marketing':
               marketingMail = True
               emailSubject = request.form.get("subject")
               emailMessage = request.form.get('message')

               cursor.execute('SELECT email from login')
               result = cursor.fetchall()
               totalMails = len(result)
               for x in result:
                  userMail = x[0]
                  threading.Thread(target=lambda: sendemail(userMail, emailMessage, emailSubject)).start()
               flash("Marketing Emails Sent!")

               cursor.execute('SELECT adminmail from adminusers')
               result1 = cursor.fetchall()
               totalAdminMails = len(result1)
               
               marketingSubjectAdmin = 'Admin Notice | Marketing email Sent!'
               marketingMessageAdmin = f'Marketing email has been sent to {totalMails} users and {totalAdminMails} admin users'
               for x in result1:
                  adminMail = x[0]
                  threading.Thread(target=lambda: sendemail(adminMail, marketingMessageAdmin, marketingSubjectAdmin)).start()

               return render_template("adminmarketing.html",title='Marketing Mails',marketingMail=marketingMail)
            
            elif request.form.get('form_type') == 'admin_manageaccounts':
               adminManageAccounts = True
               cursor.execute("SELECT name,email from login")
               registeredUsers = cursor.fetchall()
               
               cursor.execute('SELECT username,adminmail,verified,owner from adminusers')
               adminusers = cursor.fetchall()
               cursor.close()
               return render_template('adminmanageaccounts.html',title='Manage Accounts',adminManageAccounts=adminManageAccounts,registeredUsers=registeredUsers,adminusers=adminusers)
            
            elif request.form.get('form_type') == 'admin_loginas':
               userName = request.form.get("loginas_name")
               userEmail = request.form.get("loginas_email")

               session.pop('ecart',None)
               session.pop('tQuantityFmt',None)
               session['email'] = userEmail
               session['name'] = userName
               
               flash(f"Logged in as {userName}!")
               return redirect(url_for('index'))

            elif request.form.get('form_type') == 'admin_deluseracc':
               adminManageAccounts = True

               deluserMail = request.form.get("deluserMail")
               cursor.execute('DELETE FROM login WHERE email = %s',(deluserMail,))
               mysql.connection.commit()
               flash(f"User {deluserMail} Deleted!")
               
               cursor.execute("SELECT name,email from login")
               registeredUsers = cursor.fetchall()
               
               cursor.execute('SELECT username,adminmail,verified,owner from adminusers')
               adminusers = cursor.fetchall()
               cursor.close()
               return render_template('adminmanageaccounts.html',title='Manage Accounts',adminManageAccounts=adminManageAccounts,registeredUsers=registeredUsers,adminusers=adminusers)

            elif request.form.get('form_type') == 'admin_delAddacc':
               adminManageAccounts = True
               delAddMail = request.form.get('delAddMail')
               
               cursor.execute("DELETE FROM adminusers WHERE adminmail = %s",(delAddMail,))
               mysql.connection.commit()
               flash(f"Admin User {delAddMail} Deleted!")
               
               cursor.execute("SELECT name,email from login")
               registeredUsers = cursor.fetchall()

               cursor.execute('SELECT username,adminmail,verified,owner from adminusers')
               adminusers = cursor.fetchall()
               cursor.close()
               
               if delAddMail == adminMail:
                  session.pop('admin',None)
                  return redirect(url_for('index'))
               else:
                  return render_template('adminmanageaccounts.html',title='Manage Accounts',adminManageAccounts=adminManageAccounts,registeredUsers=registeredUsers,adminusers=adminusers)
               
            elif request.form.get('form_type') == 'admin_manageOrders':
               adminManageOrders = True

               cursor.execute('SELECT name,item,price,date,note,tableno,served,stripeid from orders WHERE served = %s',(0,))
               pendingorders = cursor.fetchall()

               cursor.execute('SELECT name,item,price,date,served from orders ORDER BY id DESC')
               allOrders = cursor.fetchall()

               return render_template('adminmanageorders.html',adminManageOrders=adminManageOrders,pendingorders=pendingorders,allOrders=allOrders)

            elif request.form.get('form_type') == 'admin_completeOrder':
               adminManageOrders = True

               stripeid = request.form.get('stripeid')
               cursor.execute('UPDATE orders SET served = 1 WHERE stripeid = %s;',(stripeid,))
               mysql.connection.commit()

               cursor.execute('SELECT name,item,price,date,note,tableno,served,stripeid from ORDERS WHERE served = %s',(0,))
               pendingorders = cursor.fetchall()
               
               cursor.execute('SELECT name,item,price,date,served from ORDERS ORDER BY id DESC')
               allOrders = cursor.fetchall()
               return render_template('adminmanageorders.html',adminManageOrders=adminManageOrders,pendingorders=pendingorders,allOrders=allOrders)

            elif request.form.get('form_type') == 'admin_deleteOrder':
               adminManageOrders = True

               stripeid = request.form.get('stripeid')
               cursor.execute('UPDATE orders SET served = 2 WHERE stripeid = %s;',(stripeid,))
               mysql.connection.commit()

               cursor.execute('SELECT name,item,price,date,note,tableno,served,stripeid from ORDERS WHERE served = %s',(0,))
               pendingorders = cursor.fetchall()
               
               cursor.execute('SELECT name,item,price,date,served from ORDERS')
               allOrders = cursor.fetchall()
               return render_template('adminmanageorders.html',adminManageOrders=adminManageOrders,pendingorders=pendingorders,allOrders=allOrders)

            
            elif request.form.get('form_type') == 'admin_AddAddAcc':
               adminManageAccounts = True
               newAdminName = request.form.get('newAdminName')
               newAdminEmail = request.form.get('newAdminEmail')
               NewAdminpass = secrets.token_hex(6)
               
               sql = "INSERT INTO adminusers(username,adminmail,password,verified,owner) VALUES(%s,%s,%s,%s,%s)"
               value = (newAdminName,newAdminEmail,NewAdminpass,0,0)
               cursor.execute(sql,value)
               mysql.connection.commit()
               
               subject = 'Your admin account credentials!'
               body = f'''New Admin account created!

               username: {newAdminName}
               password: {NewAdminpass}
               '''
               threading.Thread(target=lambda: sendemail(newAdminEmail, body, subject)).start()
               flash("New admin account created!")

               cursor.execute("SELECT name,email from login")
               registeredUsers = cursor.fetchall()

               cursor.execute('SELECT username,adminmail,verified,owner from adminusers')
               adminusers = cursor.fetchall()
               cursor.close()
               return render_template('adminmanageaccounts.html',title='Manage Accounts',adminManageAccounts=adminManageAccounts,registeredUsers=registeredUsers,adminusers=adminusers)

            else:
               #today sales
               now = datetime.datetime.now()
               current_date = now.strftime("%Y-%m-%d")
               cursor.execute('Select SUM(price) from orders Where date = %s',(current_date,))
               todaySales = cursor.fetchone()

               cursor.execute("SELECT SUM(price) FROM orders")
               totalSales = cursor.fetchone()
               
               cursor.execute('SELECT SUM(total) FROM cart')
               pendingSales = cursor.fetchone()

               cursor.execute('SELECT id from orders')
               totalids = cursor.fetchall()
               totalOrders = len(totalids)
               
               # To display data on chart
               cursor.execute('SELECT date, SUM(price) as total_price FROM orders GROUP BY date LIMIT 7;')
               sales = cursor.fetchall()

               #For pie chart data
               cursor.execute("SELECT item, SUM(quantity) FROM allitems GROUP BY item")
               allitems = cursor.fetchall()
               
               cursor.close()
               homeactive = True
               return render_template('admin.html', title = "Admin",totalSales=totalSales,sales=sales,homeactive=homeactive,pendingSales=pendingSales,totalOrders=totalOrders,todaySales=todaySales,allitems=allitems)

         else:
            try:

               #today sales
               now = datetime.datetime.now()
               current_date = now.strftime("%Y-%m-%d")
               cursor.execute('Select SUM(price) from orders Where date = %s',(current_date,))
               todaySales = cursor.fetchone()
               
               #total sales
               cursor.execute("SELECT SUM(price) FROM orders")
               totalSales = cursor.fetchone()
               
               #pending sales
               cursor.execute('SELECT SUM(total) FROM cart')
               pendingSales = cursor.fetchone()

               #total orders
               cursor.execute('SELECT id from orders')
               totalids = cursor.fetchall()
               totalOrders = len(totalids)
               
               # To display data on chart
               cursor.execute('SELECT date, SUM(price) as total_price FROM orders GROUP BY date LIMIT 7;')
               sales = cursor.fetchall()

               #For pie chart data
               cursor.execute("SELECT item, SUM(quantity) FROM allitems GROUP BY item")
               allitems = cursor.fetchall()
               
               cursor.close()
               homeactive = True
               return render_template('admin.html', title = "Admin",totalSales=totalSales,sales=sales,homeactive=homeactive,pendingSales=pendingSales,totalOrders=totalOrders,todaySales=todaySales,allitems=allitems)
            
            except Exception as e:
               return render_template('error.html',e=e)
      
   else:
      if request.method == 'POST':
         if request.form.get('form_type') == 'admin_forgetOTP':
            formotp = request.form.get('formotp')
            global otp
            try:
               int(formotp)

            except:
               flash("Enter Valid Integer")
               return redirect(url_for('admin'))

            else:
               if otp == int(formotp):
                  print("OTP VERIFIED SUCCESSFULLY!!!")
                  return render_template('adminsetnewpass.html')
               
               else:
                  flash("Invalid OTP")
                  return redirect(url_for('forgetpass'))
         else:
            flash("AN ERROR OCCURRED! --> Try clearing cookies!")
            return redirect(request.referrer)
      else:
         return redirect(url_for('adminlogin'))  


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',e=e)
 
####################################################################

@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
   
    if 'name' in session:
      return render_template('index.html') 
    
    elif form.is_submitted() == True:
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
                           subject = 'New Login Detected!'
                           threading.Thread(target=lambda: sendemail(email, body, subject)).start()
                           #sendemail(email,body,subject)

                        except Exception as e:
                           return render_template('error.html',e=e)     

                        else:
                           flash("You have logged in!")
                           return redirect(url_for('index'))  
                        
               else:
                  flash("Incorrect Email/Password")
                  return render_template('login.html',form=form) 
                        
            except:
                flash("No accounts exist, please create a new account")
                return render_template('register.html') 
 

    else:
      return render_template('login.html',title = 'login',form=form)

@app.route('/register',methods = ['POST','GET'])
@app.route('/signup',methods = ['POST','GET'])
def register():
   form = SignupForm()
   if request.method == 'POST':
      if form.validate_on_submit() == True:
         name = request.form.get('name') 
         email = request.form.get('email') 
         password = request.form.get('password')

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
                  return render_template('register.html',form=form)

               else:
                  sql = "INSERT INTO login(name,email,password) VALUES(%s,%s,%s)"
                  value = (name,email,password)
                  cursor.execute(sql,value)
                  mysql.connection.commit()
                  cursor.close()
                  flash("User Registration Successful !")
                  return redirect(url_for('login'))     
      else:
         for x in form.errors:
            if 'confpass' in x:
               flash("password and confirm password fields should match!")
            else:
               flash(f"Enter a valid {x}")
            return redirect(url_for('register'))

   else:
      return render_template('register.html',title = 'Register',form=form)  
        

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
      api_key = request.form.get('stripeApiKey')
      pub_key = request.form.get('stripePubKey')

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
            
            if api_key != "" and pub_key != "":
               sql = "UPDATE stripekeys SET apikey = %s, pubkey = %s"
               value = (api_key, pub_key)
               cursor.execute(sql,value)
               mysql.connection.commit()
            
            elif api_key != "":
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
            if api_key != "" and pub_key != "":
               sql = "INSERT INTO stripekeys (apikey, pubkey) VALUES (%s, %s)"
               value = (api_key,pub_key)
               cursor.execute(sql,value)
               mysql.connection.commit()
            
            elif api_key != "":
               sql = "INSERT INTO stripekeys(apikey) VALUES(%s)"
               value = (api_key,)
               cursor.execute(sql,value)
               mysql.connection.commit()
            
            elif pub_key != "":
               sql = "INSERT INTO stripekeys(pubkey) VALUES(%s)"
               value = (pub_key,)
               cursor.execute(sql,value)
               mysql.connection.commit()
            
            cursor.close() 
         if api_key != "":
            try:
               stripe.api_key = api_key
               stripe.Account.retrieve()
            except stripe.error.AuthenticationError as e:
               flash("STRIPE API KEY IS INVALID")
                  
         
         flash("Stripe keys added successfully!")
         return redirect(request.referrer)
   else:
      return redirect(url_for('index'))


@app.route('/pay',methods=['POST'])
def create_checkout_session():
   if 'name' in session:
      try:
         email = session['email']

         global tableno
         global additionalNote
         tableno = request.form['tableno']
         additionalNote = request.form['additionalNote']
         
         cursor = mysql.connection.cursor()
         cursor.execute("SELECT apikey FROM stripekeys")
         
         apikey = cursor.fetchone()
         apikey_formatted = apikey[-1]

         stripe.api_key = apikey_formatted
         
         cursor.execute('SELECT SUM(total) FROM cart WHERE email = %s',(email,))
         total_column = cursor.fetchone()
         cartvalue = total_column[0]

         cartvalstripe = (int(cartvalue)*100)
         
         # Create a Stripe checkout session
         stripe_session  = stripe.checkout.Session.create(
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
            success_url=f"http://{domain}:{port}/" + "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=f"http://{domain}:{port}/",
         )

         # Return the checkout session ID
         return stripe_session.id    
      
      except Exception as e:
         flash(str(e))
         return redirect(url_for('cart'))
   else:
      return redirect(url_for('home'))

@app.route("/success")
def success():

    # Get the checkout session ID from the query string
   checkout_session_id = request.args.get("session_id")

    # If the checkout session ID is None, redirect to the homepage
   if checkout_session_id is None:
      return redirect(url_for('index'))

    # Retrieve the checkout session from Stripe
   try:
      session_stripe = stripe.checkout.Session.retrieve(checkout_session_id)
   
   except stripe.error.InvalidRequestError:
      flash("Invalid checkout session id")
      return redirect(url_for('index')) 
   
   except stripe.error.AuthenticationError:
      flash('STRIPE ERROR OCCURED')
      return redirect(url_for('index')) 

   else:
    # Check the payment status of the checkout session
      if session_stripe.payment_status == "paid":

         try:
            cursor = mysql.connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS orders (id INT AUTO_INCREMENT PRIMARY KEY, item VARCHAR(255), price INT(255), name VARCHAR(255), email VARCHAR(255), stripeid VARCHAR(255), date DATE, note VARCHAR(255), tableno INT(255), served INT(255))")

         except Exception as e:
            flash(f"Database Error: {e}")
            return redirect(url_for('login')) 
         
         else: 
            email = session.get('email') 
            name = session.get('name') 

            cursor.execute('SELECT email,stripeid FROM orders WHERE stripeid IS NOT NULL AND stripeid  = %s',(checkout_session_id,))
            stripeid_exists = cursor.fetchone()

            if stripeid_exists is not None:
               print(f".................. {stripeid_exists}")
               dbemail = stripeid_exists[0]
               stripeid = stripeid_exists[1]
               print("****",dbemail,stripeid,"****")

               if email == dbemail and stripeid == checkout_session_id:
                  flash("Payment Already completed")
                  return redirect(url_for('index'))

               elif dbemail != email and stripeid == checkout_session_id:
                  flash("This order belongs to a different user!")
                  return redirect(url_for('index'))

            else:   
               cursor.execute('SELECT item,quantity FROM cart WHERE email = %s',(email,))
               itemQuantity = cursor.fetchall()

               # For the pie chart
               cursor.execute("CREATE TABLE IF NOT EXISTS allitems (item VARCHAR(225), quantity INT(225))")
               for x,y in itemQuantity:
                  cursor.execute("INSERT INTO allitems (item, quantity) VALUES (%s, %s)", (x, y))
                  mysql.connection.commit()

               cursor.execute('SELECT item FROM cart WHERE email = %s',(email,))
               totalItems = cursor.fetchall()
               itemList = [i[0] for i in totalItems]
               itemList_fmt = f'{itemList}'

               cursor.execute('SELECT SUM(total) FROM cart WHERE email = %s',(email,))
               totalCartVal = cursor.fetchone()
               print(totalCartVal,'gg?')

               if totalCartVal is None:
                  return render_template("error.html",e='Please complete the payment again!')
               
               #current date
               now = datetime.datetime.now()
               current_date = now.strftime("%Y-%m-%d")

               global additionalNote
               global tableno

               sql = "INSERT INTO orders(item,price,name,email,stripeid,date,tableno,note,served) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
               value = (itemList_fmt,totalCartVal[0],name,email,checkout_session_id,current_date,tableno,additionalNote,0)
               cursor.execute(sql,value)
               mysql.connection.commit()
               
               flash("Payment Successful")
               name = session.get("name")

               if additionalNote == '' or None:
                  additionalNote = 'None'
               
               elif tableno == '' or None:
                  tableno == 'None'

               body=f''' Hello {name},
               Your order has been placed successfully!
               
               Items purchased: {itemList_fmt}
               
               Table No: {tableno}
               Additional Note: {additionalNote}
               
               Amount Paid: {totalCartVal[0]} Rupees
         
               
               Payment Id: {checkout_session_id}
               Thank You!
               '''
               
               try:
                  subject = 'Order Placed'
                  threading.Thread(target=lambda: sendemail(email, body, subject)).start()

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
         print('payment was not successful')
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


@app.route('/test')
def test():

   currentAdmin = session.get('admin')
   if currentAdmin is not None:
      email = session.get("email")
      
      cursor = mysql.connection.cursor()
      cursor.execute('SELECT apikey from stripekeys')
      apikey = cursor.fetchone()
      
      cursor.execute('SELECT SUM(total) FROM cart WHERE email = %s',(email,))
      totalcartval = cursor.fetchone()

      return f'current-admin: {currentAdmin} <br> ---------- <br> stripe-api-key: {apikey} <br> ---------- <br>email: {email} <br> cart-value: {str(totalcartval[0])}'
   else:
      flash("ADMIN MUST BE LOGGED IN")
      return redirect(url_for('admin'))

if __name__ == '__main__':
   app.run(debug=True,host=domain, port=port)
