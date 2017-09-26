from flask_app import db
from flask_login import UserMixin


class Fiets(db.Model):

    Id = db.Column(db.Integer, primary_key=True)
    Nummer = db.Column(db.Integer, unique=True)
    Merk = db.Column(db.String(15))
    FrameType = db.Column(db.String(15))
    Kleur = db.Column(db.String(15))
    Framenummer = db.Column(db.String(50), unique=True)
    Gegraveerde_postcode = db.Column(db.String(30))
    Opmerkingen = db.Column(db.String(200))
    Datum = db.Column(db.Date())


    def __init__(self, Nummer, Merk, FrameType, Kleur, Framenummer=None,
                 Gegraveerde_postcode=None, Opmerkingen=None, Datum=None):

        self.Nummer = Nummer
        self.Merk = Merk
        self.FrameType = FrameType
        self.Kleur = Kleur
        self.Framenummer = Framenummer
        self.Gegraveerde_postcode = Gegraveerde_postcode
        self.Opmerkingen = Opmerkingen
        self.Datum = Datum



class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False
