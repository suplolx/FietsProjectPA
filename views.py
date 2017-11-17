from flask import render_template, request, redirect, url_for, flash
from flask_app import app, db
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from flask_weasyprint import HTML, render_pdf
from models import Fiets, User, Verwijderd
from forms import RegistratieForm, UserLogin, SearchForm, DeletedSearchForm
from dateutil.relativedelta import relativedelta
from PIL import Image
from base64 import b64decode
from io import BytesIO
import os, re, datetime, time, json


# Constants voor foto verwerking
IMG_SIZE = (500, 500)
IMG_PATH = "mysite/static/img/fietsen/"


# Login manager (docs: http://flask-login.readthedocs.io/en/latest/#configuring-your-application)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = u"Je moet ingelogd zijn om deze pagina te bekijken."


@login_manager.user_loader
def load_user(user_id):
    '''user loading function voor login manager

    Docs:
        http://flask-login.readthedocs.io/en/latest/#how-it-works

    Returns:
        User: User object

    Args:
        user_id (int): het id van de user om de goede user in te loggen

    '''

    return User.query.get(int(user_id))


@app.route('/')
def index():
    '''Index route met grafiek data en pagina navigatie

    Returns:
        Jinja-template: index.html
        vandaag (list): list van laatste vijf fietsen die zijn toegevoegd vandaag
        overschreden (list): list van alle fietsen die langer dan 3 maanden in db staan
        graph_merk (json): grafiek data van aantallen fietsen per merk

    '''

    # List comprehension met SQL-Alchemy query's om lists te vullen met vandaag toegevoegde en datum overschreden fietsen.
    vandaag = [d for d in Fiets.query.order_by(desc(Fiets.Id)).limit(5).all() if datetime.date.today() == d.Datum]
    overschreden = [d for d in Fiets.query.all() if datetime.date.today() >= d.Datum + relativedelta(months=3)]

    # Dict met aantal fietsen per merk
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
    '''Registratie formulier route om fietsen in te schrijven.

    Returns (GET):
        Jinja-template: forumulier.html
        form (object): het formulier dat meegegeven wordt in het template

    Returns (POST):
        Jinja-template: redirect naar formulier.html na het versturen van fiets data naar db en server

    '''

    form = RegistratieForm()
    # check of er al een fiets in db staat voor auto increment van "form.fietsnummer" field
    n = Fiets.query.order_by(desc(Fiets.Nummer)).first()
    n_2 = Verwijderd.query.order_by(desc(Verwijderd.Nummer)).first()

    if n.Nummer < n_2.Nummer:
        form.fietsnummer.data = n_2.Nummer + 1
    elif n:
        form.fietsnummer.data = n.Nummer + 1
    else:
        form.fietsnummer.data = 1

    if form.validate_on_submit():
        if request.method == 'POST' and 'photo' in request.files:
            # Error handler voor duplicate fiets nummers
            try:
                # Error handler voor als er fietsen worden toegevoegd zonder foto
                try:
                    # Unieke filenaam gebaseerd op timestamp
                    filename = IMG_PATH + str(time.time()).replace('.', '') + ".jpeg"
                    file = request.files['photo']
                    # check welke manier gebruiker heeft gekozen om foto te uploaden
                    if len(file.filename) > 0:
                        raw_pic = request.files['photo']
                        im = Image.open(raw_pic)
                        im.thumbnail(IMG_SIZE)
                        im.save(filename, "JPEG")

                    else:
                        # Base64 encoded string representatie van canvas data
                        raw_pic = request.form['imgdata']
                        # Omzetten van Base64 string naar Image
                        proc_pic = BytesIO(b64decode(re.sub("data:image/png;base64,", "", raw_pic)))
                        im = Image.open(proc_pic)
                        im.thumbnail(IMG_SIZE)
                        im.save(filename, "JPEG")

                    # Instance van Fiets class met alle fiets data van form (met foto)
                    fiets = Fiets(Nummer=request.form['fietsnummer'], Merk=request.form['merk'],
                                  FrameType=request.form['frametype'],  Kleur=request.form['kleur'],
                                  auteur=current_user, Framenummer=request.form['framenummer'], Gegraveerde_postcode=request.form['gravpostcode'],
                                  Opmerkingen=request.form['opmerkingen'], Foto=filename.split('/')[4],
                                  Datum=datetime.datetime.now().strftime("%Y-%m-%d"),)

                    # Fiets instance toevoegen aan db
                    db.session.add(fiets)
                    db.session.commit()

                except OSError:
                    # Instance van Fiets class met alle fiets data van form (zonder foto)
                    fiets = Fiets(Nummer=request.form['fietsnummer'], Merk=request.form['merk'],
                                  FrameType=request.form['frametype'],  Kleur=request.form['kleur'],
                                  auteur=current_user, Framenummer=request.form['framenummer'], Gegraveerde_postcode=request.form['gravpostcode'],
                                  Opmerkingen=request.form['opmerkingen'],
                                  Datum=datetime.datetime.now().strftime("%Y-%m-%d"),)

                    # Fiets instance toevoegen aan db
                    db.session.add(fiets)
                    db.session.commit()

                flash("Fiets Nummer {} is toegevoegd!".format(form.fietsnummer.data), "succes")
                return redirect(url_for('formulier'))

            except IntegrityError:
                db.session.rollback()
                flash('Er is al een fiets met dat nummer!', 'error')
                return redirect(url_for('formulier'))

    return render_template('formulier.html', form=form, title="Registratie")


@app.route('/overzicht/<int:pagina_num>')
def overzicht(pagina_num):
    '''Overzicht route met een tabel van alle fietsen in db

    Returns:
        Jinja-template: overzicht.html
        result (object): object met alle fietsen in db

    '''
    result = Fiets.query.order_by(desc(Fiets.Nummer)).paginate(per_page=15, page=pagina_num, error_out=True)

    # result = Fiets.query.order_by(desc(Fiets.Nummer)).all()
    deleted = [d for d in Verwijderd.query.order_by(desc(Verwijderd.Nummer)).limit(5).all() if datetime.date.today() == d.Datum_verwijderd]
    return render_template('overzicht.html', result=result, deleted=deleted, title="Overzicht")


@app.route('/zoeken', methods=['GET', 'POST'])
def zoeken():
    '''Zoeken route naar zoek pagina om specifieke zoek query's uit te voeren

    Returns (GET):
        Jinja-template: zoeken.html
        form (object): zoek velden om query's in te voeren

    Returns (POST):
        Jinja-template: zoeken.html
        form (object): zoek velden om query's in te voeren
        result (object): SQL-alchemy query samengesteld door zoek velden

    '''

    form = SearchForm()
    if request.method == 'POST':
        kwargs = dict()
        # query constructor met onbekend aantal args/kwargs
        for field in form:
            if len(field.data) >= 2:
                 kwargs.update({field.name:field.data})
        query_ = Fiets.query.filter_by(**kwargs).all()
        return render_template('zoeken.html', title="Zoeken", form=form, result=query_)
    return render_template('zoeken.html', title="Zoeken", form=form)


@app.route('/verwijderd', methods=['GET', 'POST'])
def verwijderd():
    '''Verwijderd route naar zoek pagina om specifieke zoek query's uit te voeren
    naar alle verwijderde fietsen.

    Returns (GET):
        Jinja-template: zoeken.html
        form (object): zoek velden om query's in te voeren

    Returns (POST):
        Jinja-template: zoeken.html
        form (object): zoek velden om query's in te voeren
        result (object): SQL-alchemy query samengesteld door zoek velden

    '''

    form = DeletedSearchForm()
    if request.method == 'POST':
        kwargs = dict()
        # query constructor met onbekend aantal args/kwargs
        for field in form:
            if len(field.data) >= 2:
                 kwargs.update({field.name:field.data})
        query_ = Verwijderd.query.filter_by(**kwargs).all()
        return render_template('verwijderd.html', title="Verwijderd", form=form, result=query_)
    return render_template('verwijderd.html', title="Verwijderd", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Login route voor de login pagina

    Returns (GET):
        Jinja-template: login.html
        form (object): formulier met login velden

    Returns (POST):
        Jinja-template: redirect naar index.html

    '''

    form = UserLogin()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.gebruikersnaam.data).first()
        if user:
            # check password hash in db met gehashte password van password form field
            if check_password_hash(user.password, form.wachtwoord.data):
                login_user(user, remember=form.onthoudme.data)
                flash('Welkom {}!'.format(user.username.capitalize()), 'informatie')
                return redirect(url_for('index'))
        flash('gebruikersnaam of wachtwoord onjuist!', 'error')
        return redirect(url_for('login'))

    return render_template('login.html', form=form, title="Login")


@app.route('/delete_fiets/<int:id>', methods=['POST'])
@login_required
def delete_fiets(id):
    '''Verwijder fiets route. Voegt verwijderde fiets toe aan "Verwijderd" table
    in db.

    Returns:
        Jinja-template: redirect naar index.html

    Args:
        id (int): id van de fiets verkregen door form action
    '''

    fiets = Fiets.query.filter_by(Nummer=id).first()
    verwijderd = Verwijderd(Nummer=fiets.Nummer, Merk=fiets.Merk, FrameType=fiets.FrameType,
                            Kleur=fiets.Kleur, Framenummer=fiets.Framenummer, Gegraveerde_postcode=fiets.Gegraveerde_postcode,
                            Opmerkingen=fiets.Opmerkingen, Datum_aangemeld=fiets.Datum, Datum_aangepast=fiets.Datum_aangepast,
                            Datum_verwijderd=datetime.datetime.now().strftime("%Y-%m-%d"), auteur=current_user, Foto=fiets.Foto)

    db.session.add(verwijderd)
    db.session.delete(fiets)
    db.session.commit()
    # Foto verwijderen van server
    # if fiets.Foto:
    #   os.remove(IMG_PATH + fiets.Foto)
    flash('Fiets nummer {} is succesvol verwijderd!'.format(id), 'succes')
    return redirect(url_for('overzicht', pagina_num=1))


@app.route('/undo/<int:id>', methods=['GET', 'POST'])
@login_required
def ongedaan_maken(id):
    vandaag = datetime.date.today()
    deleted = Verwijderd.query.filter_by(Nummer=id).first()
    if deleted.Datum_verwijderd == vandaag:
        try:
            fiets = Fiets(Nummer=deleted.Nummer, Merk=deleted.Merk, FrameType=deleted.FrameType,
                          Kleur=deleted.Kleur, auteur=current_user, Framenummer=deleted.Framenummer,
                          Gegraveerde_postcode=deleted.Gegraveerde_postcode, Opmerkingen=deleted.Opmerkingen,
                          Datum=deleted.Datum_aangemeld, Datum_aangepast=deleted.Datum_aangepast, Foto=deleted.Foto)

            db.session.add(fiets)
            db.session.delete(deleted)
            db.session.commit()
            flash("Actie succesvol ongedaan gemaakt!", "succes")
            return redirect(url_for('overzicht', pagina_num=1))

        except IntegrityError:
            db.session.rollback()
            flash('Er is al een fiets met dat nummer!', 'error')
            return redirect(url_for('formulier'))

    else:
        flash("Deze fiets is al langer dan een dag verwijderd.", "error")
        return redirect(url_for('overzicht', pagina_num=1))


@app.route('/edit_fiets/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_fiets(id):
    '''Edit fiets route met formulier om bestaande fietsen aan te passen

    Returns (GET):
        Jinja-template: edit.html
        form (object): ingevuld formulier met data van opgevraagde fiets.

    Returns (POST):
        Jinja-template: redirect naar overzicht.html

    Args:
        id (int): id van de fiets verkregen door form action

    '''

    form = RegistratieForm()
    fiets = Fiets.query.filter_by(Nummer=id).first()

    # Invullen van fiets data in form fields
    form.fietsnummer.data = fiets.Nummer
    form.merk.data = fiets.Merk
    form.frametype.data = fiets.FrameType
    form.kleur.data = fiets.Kleur
    form.framenummer.data = fiets.Framenummer
    form.gravpostcode.data = fiets.Gegraveerde_postcode
    form.datum.data = fiets.Datum
    form.opmerkingen.data = fiets.Opmerkingen
    if request.method == 'POST':
        if form.validate_on_submit():
            # Error handler voor als er geen foto is toegevoegd
            try:
                # Unieke filenaam gebaseerd op timestamp
                filename = IMG_PATH + str(time.time()).replace('.', '') + ".jpeg"
                raw_pic = request.files['photo']
                im = Image.open(raw_pic)
                im.thumbnail(IMG_SIZE)
                im.save(filename, "JPEG")
                # Dict met de nieuwe form data
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

            flash('Fiets nummer {} aangepast!'.format(id), 'succes')
            return redirect(url_for('overzicht', pagina_num=1))

    return render_template('edit.html', form=form)


@app.route('/fiets/<int:id>', methods=['GET', 'POST'])
def fiets(id):
    '''Fiets route met gedetaileerde informatie over opgevraagde fiets

    Returns:
        Jinja-template: fiets.html
        result (object): query met opgevraagde fiets

    Args:
        id (int): id van de fiets verkregen door form action

    '''
    f = Fiets.query.filter_by(Nummer=id).first()
    query = f if f is not None else Verwijderd.query.filter_by(Nummer=id).first()
    return render_template('fiets.html', result=query)


@app.route('/test', methods=["GET", "POST"])
def test_page():
    '''Test pagina route voor return value tests

    Returns:
        Jinja-template: testpage.html
        gevarieerde data: -

    '''

    # form = TestForm()
    if request.method == "POST":
        result = request.form['pdf-formulier']
        return "<p> {} </p>".format(result)

    return render_template('testpage.html')


@app.route('/to_pdf/<int:id>', methods=["POST", "GET"])
@login_required
def generate_pdf(id):
    '''Pdf generatie route. Genereert een pdf met de gegevens van de fiets.

    Returns:
        pdf: opent een pdf in de browser die geprint kan worden

    '''

    f = Fiets.query.filter_by(Nummer=id).first()
    # Datum van nu
    t = datetime.datetime.now().strftime("%Y-%m-%d")
    html = render_template('pdf_formulier.html', r=f, t=t)
    return render_pdf(HTML(string=html))


@app.route('/logout')
@login_required
def logout():
    '''Loguit route om de ingelogde gebruiker uit te loggen

    Returns:
        Jinja-template: redirect naar login.html

    '''

    # logout method van flask-login
    # https://github.com/maxcountryman/flask-login/blob/master/flask_login/utils.py (regel 164)
    logout_user()
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    '''Error handler voor HTTP 404 error

    Returns:
        Jinja-template: 404.html custom error pagina

    '''
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    '''Error handler voor HTTP 500 error

    Returns:
        Jinja-template: 500.html custom error pagina
        error (object): error object met informatie over de error

    '''

    # Veranderingen ongedaan maken in db
    db.session.rollback()
    return render_template('500.html', error=e), 500
