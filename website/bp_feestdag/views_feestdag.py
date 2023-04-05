from flask import Blueprint, render_template, redirect, url_for,request,flash
from flask_login import current_user
import pandas as pd
import csv
from website.bp_feestdag.forms import hash_password,FeestdagForm

views_fd = Blueprint('views', __name__)




@views_fd.route("/feestdag")
def feestdag():
    df = pd.read_csv('feestdag.csv',encoding="utf-8")
    data = df.to_dict('records')
    return render_template('feestdag.html', data=data)
    


@views_fd.route('/toevoegen', methods=['GET','POST'])
def toevoegen():
    # haal de gegevens uit het formulier
    ingediend_door = current_user.name
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
        fieldnames = ['datum', 'naam_nl', 'naam_en', 'naam_fr', 'is_officieel','bevestigd','ingediend_door']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'datum': datum, 'naam_nl': naam_nl, 'naam_en': naam_en, 'naam_fr': naam_fr, 'is_officieel': is_officieel, 'bevestigd' : bevestigd,"ingediend_door" : ingediend_door})
        flash("Aanvraag feestdag is verstuurd!")
    return redirect(url_for('views.feestdag'))


 


@views_fd.route('/feestdag/edit', methods=['GET', 'POST'])
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

        return redirect(url_for('views_general.index'))

    # render het formulier om feestdagen te bewerken
    return render_template('beheerder_editcsv.html', feestdagen=feestdagen)



@views_fd.route('/bevestigen', methods=['GET', 'POST'])
def bevestigen():
    df = pd.read_csv('feestdag_aanvraag.csv',encoding="utf-8")
    data = df.to_dict('records')
    return render_template('bevestigen.html', data=data)


@views_fd.route('/bevestig-feestdag/<datum>', methods=['POST'])
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
        fieldnames = ['Datum', 'Naam NL', 'Naam EN', 'Naam FR', 'Officiële feestdag',"ingediend_door"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for row in feestdagen:
            if row['Datum'] == datum:
                row.pop('bevestigd', None)
                writer.writerow(row)
                verwijder_feestdag_aanvraag(datum)
    flash("Feestdag is bevestigd")
    return render_template("feestdag.html")


def verwijder_feestdag_aanvraag(datum):
    with open('feestdag_aanvraag.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        feestdagen = [row for row in reader if row['Datum'] != datum]
    with open('feestdag_aanvraag.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Datum', 'Naam NL', 'Naam EN', 'Naam FR', 'Officiële feestdag', 'bevestigd','ingediend_door']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in feestdagen:
            writer.writerow(row)


    # haal de feestdag op die je wilt bewerken
    with open('feestdag.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        feestdagen = [row for row in reader]
        feestdag = next((row for row in feestdagen if row['Datum'] == datum), None)

        # als de feestdag niet gevonden is, toon dan een foutmelding
        if not feestdag:
            flash('Feestdag niet gevonden.', 'error')
            return redirect(url_for('views_general.index'))

    # vul een formulier met de huidige waarden van de feestdag
    form = FeestdagForm(data=feestdag)

    # als het formulier is ingediend en geldig is, sla dan de bewerkte feestdag op
    if form.validate_on_submit():
        # bewerk de feestdag met de waarden uit het formulier
        feestdag['Naam NL'] = form.naam_nl.data
        feestdag['Naam EN'] = form.naam_en.data
        feestdag['Naam FR'] = form.naam_fr.data
        feestdag['Officiële feestdag'] = form.is_officieel.data

        # sla de bewerkte feestdag op in het CSV-bestand
        with open('feestdag.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Datum', 'Naam NL', 'Naam EN', 'Naam FR', 'Officiële feestdag']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(feestdagen)

        flash('Feestdag bewerkt!', 'success')
        return redirect(url_for('views_pf.index'))

    # toon het bewerkingsformulier
    return render_template('bewerk_feestdag.html', form=form)




@views_fd.route('/feestdag/<datum>', methods=['GET', 'POST'])
def bewerk_feestdag(datum):
    with open('feestdag.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        feestdagen = [row for row in reader]
        feestdag = next((row for row in feestdagen if row['Datum'] == datum), None)

        if not feestdag:
            flash('Feestdag niet gevonden.', 'error')
            return redirect(url_for('views_general.index'))

    form = FeestdagForm(data=feestdag)

    if form.validate_on_submit():
        feestdag['Naam NL'] = form.naam_nl.data
        feestdag['Naam EN'] = form.naam_en.data
        feestdag['Naam FR'] = form.naam_fr.data
        feestdag['Officiële feestdag'] = form.is_officieel.data

        with open('feestdag.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Datum', 'Naam NL', 'Naam EN', 'Naam FR', 'Officiële feestdag',"ingediend_door"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(feestdagen)

        flash('Feestdag bewerkt!', 'success')
        return redirect(url_for('views.edit_feestdagen'))

    return render_template('bewerk_feestdag.html', form=form, feestdag=feestdag)


@views_fd.route('/verwijder-feestdag/<datum>', methods=['POST'])
def verwijder_feestdag(datum):


    # controleer of de gebruiker een beheerder is
    if not current_user.is_authenticated or current_user.role != 'beheerder':
        return redirect(url_for('auth.login'))
    
    # verwijder de feestdag uit het CSV-bestand
    with open('feestdag.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        feestdagen = [row for row in reader]
    with open('feestdag.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Datum', 'Naam NL', 'Naam EN', 'Naam FR', 'Officiële feestdag',"ingediend_door"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in feestdagen:
            if row['Datum'] != datum:
                writer.writerow(row)
    
    # verwijder de feestdag uit het aanvraag CSV-bestand als deze daar ook staat
    with open('feestdag_aanvraag.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        feestdagen = [row for row in reader]
    with open('feestdag_aanvraag.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Datum', 'Naam NL', 'Naam EN', 'Naam FR', 'Officiële feestdag', 'bevestigd',"ingediend_door"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in feestdagen:
            if row['Datum'] != datum:
                writer.writerow(row)
    flash("Feestdag is verwijderd")
    return redirect(url_for('views.edit_feestdagen'))