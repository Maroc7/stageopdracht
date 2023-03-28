from flask import Blueprint, render_template, redirect, url_for
from .models import  Profile
from .forms import AddProfileForm

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/add_profile', methods=['GET', 'POST'])
def add_profile():
    form = AddProfileForm()
    if form.validate_on_submit():
        from .database import db
        profile = Profile(name=form.name.data, role=form.role.data)
        db.session.add(profile)
        db.session.commit()
        return redirect(url_for('views.index'))
    return render_template('add_profile.html', form=form)

@views.route("/show_profiles")
def show_profiles():
    profiles = Profile.query.all()
    return render_template("show_profiles.html",profiles=profiles)