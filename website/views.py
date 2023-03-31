from flask import Blueprint, render_template, redirect, url_for,request,flash
from .models import  Profile
from flask_login import current_user
from .forms import AddProfileForm
import pandas as pd
import csv
from .forms import hash_password
from .database import db

views = Blueprint('views', __name__)


@views.route('/')
def index():
    return render_template('index.html', profile = current_user)



@views.route("/feestdag")
def feestdag():
    df = pd.read_csv('feestdag.csv',encoding="utf-8")
    data = df.to_dict('records')
    return render_template('feestdag.html', data=data)
    


@views.route('/toevoegen', methods=['GET','POST'])
def toevoegen():
    # haal de gegevens uit het formulier
    datum = request.form['datum']
    naam_nl = request.form['naam_nl']
    naam_en = request.form['naam_en']
    naam_fr = request.form['naam_fr']
    is_officieel = request.form.get('is_officieel')
    bevestigd = "in behandeling"
    if is_officieel is not None:
        is_officieel = True
    else:
        is_officieel = False
    # sla de gegevens op in de CSV
    with open('feestdag_aanvraag.csv', 'a', newline='', encoding="utf-8")as csvfile:
        fieldnames = ['datum', 'naam_nl', 'naam_en', 'naam_fr', 'is_officieel','bevestigd']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'datum': datum, 'naam_nl': naam_nl, 'naam_en': naam_en, 'naam_fr': naam_fr, 'is_officieel': is_officieel, 'bevestigd' : bevestigd})
        flash("Aanvraag feestdag is verstuurd!, succes")
    return redirect(url_for('views.feestdag'))




@views.route('/add_profile', methods=['GET', 'POST'])
def add_profile():
    form = AddProfileForm()
    if form.validate_on_submit():
        hashed_password = hash_password(form.password.data)
        profile = Profile(name=form.name.data, role=form.role.data, password=hashed_password)
        db.session.add(profile)
        db.session.commit()
        flash('Profile added successfully.', 'success')
        return redirect(url_for('views.add_profile'))
    return render_template('add_profile.html', form=form)
 
@views.route("/show_profiles")
def show_profiles():
    profiles = Profile.query.all()
    return render_template("show_profiles.html",profiles=profiles)


# route om de feestdagen te bewerken
@views.route('/feestdag/edit', methods=['GET', 'POST'])
def edit_feestdagen():
    # lees de feestdagen uit het CSV-bestand
    with open('feestdag.csv', 'r', newline='', encoding='utf-8') as csvfile:
        feestdagen_reader = csv.DictReader(csvfile)
        feestdagen = list(feestdagen_reader)

    if request.method == 'POST':
        # haal de gegevens op uit het formulier
        datum = request.form['datum']
        naam_nl = request.form['naam_nl']
        naam_en = request.form['naam_en']
        naam_fr = request.form['naam_fr']
        is_officieel = request.form.get('is_officieel')

        # bewerk de feestdag in de lijst
        for feestdag in feestdagen:
                feestdag['Name NL'] = naam_nl
                feestdag['Name EN'] = naam_en
                feestdag['Name FR'] = naam_fr
                feestdag['Datum'] = datum
                feestdag['Officiële feestdag'] = is_officieel

        # schrijf de aangepaste feestdagen terug naar het CSV-bestand
        with open('feestdag.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name_nl', 'name_en', 'name_fr', 'date', 'official']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for feestdag in feestdagen:
                writer.writerow(feestdag)

        return redirect(url_for('views.index'))

    # render het formulier om feestdagen te bewerken
    return render_template('beheerder_editcsv.html', feestdagen=feestdagen)



@views.route('/bevestigen', methods=['GET', 'POST'])
def bevestigen():
    df = pd.read_csv('feestdag_aanvraag.csv',encoding="utf-8")
    data = df.to_dict('records')
    return render_template('bevestigen.html', data=data)


@views.route('/bevestig-feestdag/<datum>', methods=['POST'])
def bevestig_feestdag(datum):
       # controleer of de gebruiker een beheerder is
    if not current_user.is_authenticated or current_user.role != 'beheerder':
        return redirect(url_for('auth.login'))
    
    # haal de gegevens van de bevestigde feestdag op
    with open('feestdag_aanvraag.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        feestdagen = [row for row in reader]
        feestdag = next((row for row in feestdagen if row['Datum'] == datum), None)

    # voeg de feestdag toe aan het andere CSV-bestand
    with open('feestdag.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Datum', 'Naam NL', 'Naam EN', 'Naam FR', 'Officiële feestdag']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for row in feestdagen:
            if row['Datum'] == datum:
                row.pop('bevestigd', None)
                writer.writerow(row)
                verwijder_feestdag(datum)
    flash("Feestdag is bevestigd", "succes")
    return render_template("feestdag.html")


def verwijder_feestdag(datum):
    with open('feestdag_aanvraag.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        feestdagen = [row for row in reader if row['Datum'] != datum]
    with open('feestdag_aanvraag.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Datum', 'Naam NL', 'Naam EN', 'Naam FR', 'Officiële feestdag', 'bevestigd']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in feestdagen:
            writer.writerow(row)