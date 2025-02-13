# Hello!, This is a **Restaurant Management System** I created in my second year of engineering. 

# ---------------------------------------------------------------

### Installation:

- git clone this repo
- `pip install -r requirements.txt`
- Create a file called `.env` and copy contents of `.env.example` in it. `(website wont run without this file)`
- Fill mysql database details in your `.env` file
- Fill up email authentication details in `.env` (optional but might get error)
- Import the demo sql file provided

# ---------------------------------------------------------------


### Note: <span style="color:red">You must create an account at stripe.com and get your api keys! </span>
### <span style="color:red"> Also Note: Admin account needs to be verified before accessing the dashboard **(therefore you will need to setup smtp!)** </span>


### Usage:
- To create all the mysql tables you need to visit `127.0.0.1/admin/login` or `localhost/admin/login` or `yourdomain.com/admin/login`
- User Panel `127.0.0.1` or `localhost` or `yourdomain.com`
- Admin Panel: `127.0.0.1/admin` or `localhost/admin` or `yourdomain.com/admin`

# ---------------------------------------------------------------

Issues:
  
  - ~No implementation of csrf tokens~
  - ~Form fields are not secured~
  - ~Item prices can be modified using inspect element~
  - Admin page is not responsive
  - Passwords are not hashed
  - Public_key of payment gateway is exposed ⚠️
  - Only 3 categories are available in menu
  - Only stripe payment gateway is supported

# ---------------------------------------------------------------

Images:

## Home Page
![Home Page](static/sample/home.png)
## Menu Page
![Menu Page](static/sample/menu.png)
## Cart Page
![Cart Page](static/sample/cart.png)
## Admin Home Page
![Admin Home Page](static/sample/admin.png)
## Admin Manage Orders Page
![Manage Orders Page](static/sample/orders.png)


# ---------------------------------------------------------------

## I would appreciate any contribution to this project. Just Fork this repository and try to fix the above issues.
## Once you are done, submit a pull request

# ---------------------------------------------------------------

## License:
[Custom License](LICENSE)
# ---------------------------------------------------------------
### <span style="color:green"> My Discord: itsadi22 </span>
Ask me if you need any help `:wink:`

[Contact me](mailto:itsadi22.zil@ud.me)
