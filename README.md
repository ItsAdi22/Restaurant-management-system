# Hello! This is the first project I created using Flask framework in my second year of engineering.

# ---------------------------------------------------------------

### Installation:

- git clone this repo
- `pip install -r requirements.txt`
- Create a file called `.env` and copy contents of `.env.example` in it. `(website wont run without this file)`
- fill mysql database details in your `.env` file
- fill up email authentication details in `.env` (optional but might get error)
- import the demo sql file provided

# ---------------------------------------------------------------


### Note: <span style="color:red">You must create an account at stripe.com and get your api keys! </span>
### <span style="color:red"> Also Note: Admin account needs to be verified before accessing the dashboard **(therefore you will need to setup smpt!)** </span>


### Usage:
- go to this address `127.0.0.1` or `localhost` or `yourdomain.com`
- Admin panel: `127.0.0.1/admin` or `localhost/admin` or `yourcomain.com/admin`

# ---------------------------------------------------------------

Issues:
  - No implementation of csrf tokens
  - Form fields are not secured
  - Passwords are not hashed
  - Public_key of payment gateway is exposed ⚠️
  - ~Item prices can be modified using inspect element~

# ---------------------------------------------------------------

## I would appreciate any contribution to this project. Just Fork this repository and try to fix the above issues.
## Once you are done, create a pull request


# ---------------------------------------------------------------
### <span style="color:green"> My Discord: itsadi22 </span>
Ask me if you need any help `:wink:`

[Contact me](mailto:itsadi22.zil@ud.me)
