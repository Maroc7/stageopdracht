from flask import Blueprint, render_template, redirect, url_for,request,flash
from .models import  Profile
from .form_profile import AddProfileForm
from .form_profile import hash_password
from website.database import db
views_pf = Blueprint("views_pf", __name__)

@views_pf.route('/add_profile', methods=['GET', 'POST'])
def add_profile():
    form = AddProfileForm()
    if form.validate_on_submit():
        hashed_password = hash_password(form.password.data)
        profile = Profile(name=form.name.data, role=form.role.data, password=hashed_password)
        db.session.add(profile)
        db.session.commit()
        flash('Profile added successfully.', 'success')
        return redirect(url_for('views_pf.add_profile'))
    return render_template('add_profile.html', form=form)
 
@views_pf.route("/show_profiles")
def show_profiles():
    profiles = Profile.query.all()
    return render_template("show_profiles.html",profiles=profiles)


