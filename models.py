from flask_app import db, app
from flask_login import UserMixin
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)



class User(UserMixin, db.Model):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    authenticated = db.Column(db.SmallInteger, default=False)
    fiets_aangemeld = db.relationship('Fiets', backref='auteur', lazy='dynamic')


    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False



class Fiets(db.Model):
    __tablname__ = "fiets"
    __table_args__ = {'extend_existing': True}
    Id = db.Column(db.Integer, primary_key=True)
    Nummer = db.Column(db.Integer, unique=True)
    Merk = db.Column(db.String(15))
    FrameType = db.Column(db.String(15))
    Kleur = db.Column(db.String(15))
    Framenummer = db.Column(db.String(50), unique=True)
    Gegraveerde_postcode = db.Column(db.String(30))
    Opmerkingen = db.Column(db.String(200))
    Datum = db.Column(db.Date())
    Datum_aangepast = db.Column(db.Date())
    Datum_verwijderd = db.Column(db.Date())
    Foto = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



if __name__ == '__main__':
    manager.run()


