from flask import Blueprint, render_template, redirect, url_for,request,flash
from .models import  Profile
from .forms import AddProfileForm
import pandas as pd
import csv
from .forms import hash_password
from .database import db

views = Blueprint('views', __name__)


@views.route('/')
def index():
    df = pd.read_csv('feestdag.csv',encoding="utf-8")
    data = df.to_dict('records')
    return render_template('index.html', data=data)


@views.route('/toevoegen', methods=['GET','POST'])
def toevoegen():
    # haal de gegevens uit het formulier
    datum = request.form['datum']
    naam_nl = request.form['naam_nl']
    naam_en = request.form['naam_en']
    naam_fr = request.form['naam_fr']
    is_officieel = request.form.get('is_officieel')
    if is_officieel is not None:
        is_officieel = True
    else:
        is_officieel = False
    # sla de gegevens op in de CSV
    with open('feestdag.csv', 'a', newline='', encoding="utf-8")as csvfile:
        fieldnames = ['datum', 'naam_nl', 'naam_en', 'naam_fr', 'is_officieel']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'datum': datum, 'naam_nl': naam_nl, 'naam_en': naam_en, 'naam_fr': naam_fr, 'is_officieel': is_officieel})
    return redirect(url_for('views.index'))






@views.route('/add_profile', methods=['GET', 'POST'])
def add_profile():
    form = AddProfileForm()
    if form.validate_on_submit():
        hashed_password = hash_password(form.password.data)
        profile = Profile(name=form.name.data, role=form.role.data, password=hashed_password)
        db.session.add(profile)
        db.session.commit()
        flash('Profile added successfully.', 'success')
        return redirect(url_for('views.show_profiles'))
    return render_template('add_profile.html', form=form)
 
@views.route("/show_profiles")
def show_profiles():
    profiles = Profile.query.all()
    return render_template("show_profiles.html",profiles=profiles)

