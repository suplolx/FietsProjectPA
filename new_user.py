from werkzeug.security import generate_password_hash
from flask_app import db
from models import User

username = input('username: ')
email = input('email: ')
password = input('password: ')

new_user = User(username=username, email=email, password=generate_password_hash(password, method='sha256'))

db.session.add(new_user)
db.session.commit()

print("Nieuwe gebruiker sucessvol toegevoegd.\nGebruikersnaam: {}\nWachtwoord: {}\nEmail: {}".format(username, password, email))
