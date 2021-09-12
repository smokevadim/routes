import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_PORT = '8500'
DB_USER = 'dbuser'
DB_PASSWORD = 'dbpassword'
DB_HOST = os.environ.get('DB_HOST', 'localhost')
SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5450/route'
