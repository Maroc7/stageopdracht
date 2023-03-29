from flask import Blueprint, render_template, redirect, url_for,request
from .models import  Profile, User
from .forms import AddProfileForm
import pandas as pd
import csv
views = Blueprint('views', __name__)

@views.route('/')
def index():
    df = pd.read_csv('website/feestdag.csv')
    data = df.to_dict('records')
    return render_template('index.html', data=data)

@views.route('/toevoegen', methods=['GET','POST'])
def toevoegen():
    # haal de gegevens uit het formulier
    
    datum = request.form['datum']
    naam_nl = request.form['naam_nl']
    naam_en = request.form['naam_en']
    naam_fr = request.form['naam_fr']
    is_officieel = request.form['is_officieel']
    is_officieel = False
    if 'is_officieel' in request.form:
        is_officieel = True

    # sla de gegevens op in de CSV
    with open('feestdagen.csv', 'a', newline='') as csvfile:
        fieldnames = ['datum', 'naam_nl', 'naam_en', 'naam_fr', 'is_officieel']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'datum': datum, 'naam_nl': naam_nl, 'naam_en': naam_en, 'naam_fr': naam_fr, 'is_officieel': is_officieel})

    # stuur de gebruiker terug naar de pagina met de feestdagen
    return redirect(url_for('/'))




@views.route('/add_profile', methods=['GET', 'POST'])
def add_profile():
    form = AddProfileForm()
    if form.validate_on_submit():
        from .database import db
        profile = Profile(name=form.name.data, role=form.role.data)
        db.session.add(profile)
        db.session.commit()

        if profile.role == "beheerder":
            new_user = User(username=profile.name.lower,id_profile=profile.id, password=profile.name,is_admin=True)
            db.session.add(new_user)
            db.session.commit()
            profile.user = new_user
            db.session.commit()
            return redirect(url_for('views.index'))
    return render_template('add_profile.html', form=form)

@views.route("/show_profiles")
def show_profiles():
    profiles = Profile.query.all()
    return render_template("show_profiles.html",profiles=profiles)




""""
from website.models import db, Profile, User

@auth.route('/add_profile', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        new_profile = Profile(name=name, username=username, password=password, role=role)
        db.session.add(new_profile)
        db.session.commit()

        # Check if the new user is a 'beheerder' and create a new user if true
        if role == 'beheerder':
            new_user = User(username=username, password=password, is_admin=True)
            db.session.add(new_user)
            db.session.commit()

        return redirect(url_for('auth.login'))
    return render_template('add_profile.html')

"""