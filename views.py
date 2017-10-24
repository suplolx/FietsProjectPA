from flask import render_template, request, redirect, url_for, flash
from flask_app import app, db
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
#from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.security import check_password_hash
from models import Fiets, User
from forms import RegistratieForm, UserLogin, SearchForm
from dateutil.relativedelta import relativedelta
from PIL import Image
from base64 import b64decode
from io import BytesIO
import re
import datetime
import time
import json


#photos = UploadSet('photos', IMAGES) # https://auth0.com/blog/image-processing-in-python-with-pillow/
#configure_uploads(app, photos)
DATE_THRESHOLD = 7
IMG_SIZE = (500, 500)
IMG_PATH = "mysite/static/img/fietsen/"


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = u"Je moet ingelogd zijn om deze pagina te bekijken."


@login_manager.user_loader
def load_user(user_id):
    '''
    login func voor flask_login. Zie docs: https://flask-login.readthedocs.io/en/latest/
    '''
    return User.query.get(int(user_id))


@app.route('/')
def index():
    '''
    returns
    index.html: Jinja template

    vandaag: sqlalchemy query voor fietsen die vandaag zijn toegevoegd. Python
             object datatype

    overschreden: sqlalchemy query voor fietsen die langer dan 3 maanden in db
                  staan. Python object datatype

    grap_merk: Python dictionary met sqlquery per merk voor grafiek dashboard.
               Json dump
    '''
    vandaag = [d for d in Fiets.query.order_by(desc(Fiets.Id)).limit(5).all() if datetime.date.today() == d.Datum]
    overschreden = [d for d in Fiets.query.all() if datetime.date.today() >= d.Datum + relativedelta(months=3)]

    merk_dict = {"Gazelle":len(Fiets.query.filter_by(Merk="Gazelle").all()),
                  "Batavus":len(Fiets.query.filter_by(Merk="Batavus").all()),
                  "Sparta":len(Fiets.query.filter_by(Merk="Sparta").all()),
                  "Giant":len(Fiets.query.filter_by(Merk="Giant").all()),
                  "Overige":len(Fiets.query.filter(Fiets.Merk != "Gazelle").\
                         filter(Fiets.Merk != "Batavus").\
                         filter(Fiets.Merk != "Giant").\
                         filter(Fiets.Merk != "Sparta").all())
    }

    return render_template('index.html', vandaag=vandaag,
    overschreden=overschreden, graph_merk=json.dumps(merk_dict, sort_keys=True))


@app.route('/formulier', methods=['GET', 'POST'])
@login_required
def formulier():
    form = RegistratieForm()
    recent_nummer = Fiets.query.order_by(desc(Fiets.Nummer)).first()
    if recent_nummer:
        form.fietsnummer.data = recent_nummer.Nummer + 1
    else:
        form.fietsnummer.data = 1
    if form.validate_on_submit():
        if request.method == 'POST' and 'photo' in request.files:
            try:

                try:
                    filename = IMG_PATH + str(time.time()).replace('.', '') + ".jpeg"
                    raw_pic = request.form['imgdata']
                    proc_pic = BytesIO(b64decode(re.sub("data:image/png;base64,", "", raw_pic)))
                    im = Image.open(proc_pic)
                    im.thumbnail(IMG_SIZE)
                    im.save(filename, "JPEG")
                    fiets = Fiets(Nummer=request.form['fietsnummer'], Merk=request.form['merk'],
                                  FrameType=request.form['frametype'],  Kleur=request.form['kleur'],
                                  auteur=current_user, Framenummer=request.form['framenummer'], Gegraveerde_postcode=request.form['gravpostcode'],
                                  Opmerkingen=request.form['opmerkingen'], Foto=filename.split('/')[4],
                                  Datum=datetime.datetime.now().strftime("%Y-%m-%d"),)
                    db.session.add(fiets)
                    db.session.commit()

                except OSError:
                    fiets = Fiets(Nummer=request.form['fietsnummer'], Merk=request.form['merk'],
                                  FrameType=request.form['frametype'],  Kleur=request.form['kleur'],
                                  auteur=current_user, Framenummer=request.form['framenummer'], Gegraveerde_postcode=request.form['gravpostcode'],
                                  Opmerkingen=request.form['opmerkingen'],
                                  Datum=datetime.datetime.now().strftime("%Y-%m-%d"),)

                    db.session.add(fiets)
                    db.session.commit()



                flash("Fiets Nummer {} is toegevoegd!".format(form.fietsnummer.data))
                return redirect(url_for('formulier'))

            except IntegrityError:
                db.session.rollback()
                flash('Er is al een fiets met dat nummer!')
                return redirect(url_for('formulier'))

    return render_template('formulier.html', form=form, title="Registratie")


@app.route('/overzicht')
@login_required
def search():
    result = Fiets.query.order_by(desc(Fiets.Nummer)).all()
    return render_template('overzicht.html', result=result, title="Overzicht")


@app.route('/zoeken', methods=['GET', 'POST'])
@login_required
def zoeken():
    form = SearchForm()
    if request.method == 'POST':
        kwargs = dict()
        for field in form:
            if len(field.data) >= 2:
                 kwargs.update({field.name:field.data})
        query_ = Fiets.query.filter_by(**kwargs).all()
        return render_template('zoeken.html', title="Zoeken", form=form, result=query_)
    return render_template('zoeken.html', title="Zoeken", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLogin()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.gebruikersnaam.data).first()
        if user:
            if check_password_hash(user.password, form.wachtwoord.data):
                login_user(user, remember=form.onthoudme.data)
                flash('Welkom {}!'.format(user.username.capitalize()))
                return redirect(url_for('index'))
        flash('gebruikersnaam of wachtwoord onjuist!')
        return redirect(url_for('login'))

    return render_template('login.html', form=form, title="Login")


@app.route('/delete_fiets/<int:id>', methods=['POST'])
@login_required
def delete_fiets(id):
    fiets = Fiets.query.filter_by(Nummer=id).first()
    db.session.delete(fiets)
    db.session.commit()
    flash('Fiets nummer {} is succesvol verwijderd!'.format(id))
    return redirect(url_for('index'))


@app.route('/edit_fiets/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_fiets(id):
    form = RegistratieForm()
    fiets = Fiets.query.filter_by(Nummer=id).first()
    form.fietsnummer.data = fiets.Nummer
    form.merk.data = fiets.Merk
    form.frametype.data = fiets.FrameType
    form.kleur.data = fiets.Kleur
    form.framenummer.data = fiets.Framenummer
    form.gravpostcode.data = fiets.Gegraveerde_postcode
    form.opmerkingen.data = fiets.Opmerkingen
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                filename = IMG_PATH + str(time.time()).replace('.', '') + ".jpeg"
                raw_pic = request.files['photo']
                im = Image.open(raw_pic)
                im.thumbnail(IMG_SIZE)
                im.save(filename, "JPEG")
                update_dict = {
                    "Nummer": request.form['fietsnummer'],
                    "Merk": request.form['merk'],
                    "FrameType": request.form['frametype'],
                    "Kleur": request.form['kleur'],
                    "Framenummer": request.form['framenummer'],
                    "Gegraveerde_postcode": request.form['gravpostcode'],
                    "Opmerkingen": request.form['opmerkingen'],
                    "Datum_aangepast": datetime.date.today(),
                    "Foto": filename.split('/')[4]
                }
                new_fiets = Fiets.query.filter_by(Nummer=id).update(update_dict)
                db.session.commit()

            except OSError:
                update_dict = {
                    "Nummer": request.form['fietsnummer'],
                    "Merk": request.form['merk'],
                    "FrameType": request.form['frametype'],
                    "Kleur": request.form['kleur'],
                    "Framenummer": request.form['framenummer'],
                    "Gegraveerde_postcode": request.form['gravpostcode'],
                    "Opmerkingen": request.form['opmerkingen'],
                    "Datum_aangepast": datetime.date.today(),
                }
                new_fiets = Fiets.query.filter_by(Nummer=id).update(update_dict)
                db.session.commit()



            flash('Fiets nummer {} aangepast!'.format(id))
            return redirect(url_for('search'))

    return render_template('edit.html', form=form)


@app.route('/fiets/<int:id>', methods=['GET', 'POST'])
@login_required
def fiets(id):
    f = Fiets.query.filter_by(Nummer=id).first()
    return render_template('fiets.html', result=f)


@app.route('/test')
@login_required
def test_page():
    return render_template('testpage.html')


@app.route('/offline')
def offline():
    return render_template('offline.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    db.session.rollback()
    return render_template('500.html', error=e), 500
