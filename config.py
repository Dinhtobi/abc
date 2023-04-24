import os 

SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))


# Connect to the database
SQLALCHEMY_DATABASE_URI = 'mysql://root:''@localhost/pbl5_ndkm'

# Turn off the Flask-SQLAlchemy event system and warning
SQLALCHEMY_TRACK_MODIFICATIONS = False

MAIL_SERVER='smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'dinhnguyen2002asd@gmail.com'
MAIL_PASSWORD = ''
MAIL_USE_TLS= False
MAIL_USE_SSL= True