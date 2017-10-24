from secret import USERNAME, PASSWORD, DB_NAME, secret_key
import os


basedir = os.path.abspath(os.path.dirname(__file__))


DEBUG = False
SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@FietsFoetsie.mysql.pythonanywhere-services.com/{}'.format(USERNAME, PASSWORD, DB_NAME)
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_SIZE = 100
SQLALCHEMY_POOL_RECYCLE = 280
SECRET_KEY = secret_key
UPLOADED_PHOTOS_DEST = "mysite/static/img/fietsen"