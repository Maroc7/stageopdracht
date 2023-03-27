from flask import Blueprint, render_template,redirect,url_for
from .models import Profile
from .forms import AddProfileForm


views = Blueprint('views', __name__)

@views.route("/")
def do_index():
    return render_template("index.html")

@views.route('/add_profile', methods=['GET', 'POST'])
def add_profile():
    form = AddProfileForm()
    if form.validate_on_submit():
        profile = Profile(name=form.name.data, role=form.role.data)

        # Sla het profiel op in de database of voeg het toe aan een lijst met profielen
        return redirect(url_for('/'))
    return render_template('add_profile.html', form=form)
