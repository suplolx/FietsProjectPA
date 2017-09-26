from secret import USERNAME, PASSWORD, DB_NAME, secret_key


DEBUG = False
SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@Suplolx.mysql.pythonanywhere-services.com/{}'.format(USERNAME, PASSWORD, DB_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_SIZE = 100
SQLALCHEMY_POOL_RECYCLE = 280
SECRET_KEY = secret_key
