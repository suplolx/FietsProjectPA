from flask_wtf import Form
from wtforms.fields import TextField, TextAreaField, SubmitField, IntegerField, PasswordField, BooleanField, HiddenField, DateField
from wtforms.validators import DataRequired, Length


class RegistratieForm(Form):
    fietsnummer = IntegerField("Fiets Nummer", validators=[DataRequired()])
    merk = TextField("Merk")
    frametype = TextField("Frametype")
    kleur = TextField("Kleur")
    framenummer = TextField("Framenummer")
    gravpostcode = TextField("Graveer code")
    opmerkingen = TextAreaField("Opmerkingen", validators=[Length(min=0, max=200)])
    imgdata = HiddenField("Foto")
    datum = DateField("Datum")
    formBtn = SubmitField("VOEG TOE")



class UserLogin(Form):
    gebruikersnaam = TextField("Gebruikersnaam")
    wachtwoord = PasswordField("Wachtwoord")
    onthoudme = BooleanField("Onthoud mij")
    loginBtn = SubmitField("Log in")



class SearchForm(Form):
    Merk = TextField("Merk")
    FrameType = TextField("FrameType")
    Kleur = TextField("Kleur")
    Datum = TextField("Datum")



class TestForm(Form):
    pdf_formulier = BooleanField("Pdf Formulier")
    submitBtn = SubmitField("Submit")



class DeleteForm(Form):
    pdf_formulier = BooleanField("Opgehaald?")
    delete_btn = SubmitField("Verwijder")