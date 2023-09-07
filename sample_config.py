# Set up the database connection

SQLALCHEMY_DATABASE_URI = 'mssql://username:password@server/database'
SECRET_KEY = 'secret'
DEBUG = True


SERVER = 'localhost'
DATABASE = 'DemoDB'
USERNAME = 'SA' 
PASSWORD = 'password'
DRIVER = '{ODBC Driver 17 for SQL SERVER}'
TIMEOUT = 1 # Setting Timeout to 1 second
TRUSTED_CONNECTION = 'YES'