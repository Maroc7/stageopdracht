from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user,UserMixin, current_user,logout_user,login_required
from werkzeug.security import check_password_hash
from .models import Profile
from website import login_manager

auth = Blueprint('auth', __name__)


from .models import Profile

@login_manager.user_loader
def load_user(proifile_id):
    return Profile.query.get(int(proifile_id))



@auth.route('/login', methods=['GET', 'POST'])
def login():
    name = ''
    password = ''
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        profile = Profile.query.filter_by(name=name).first()
        if profile:
            if check_password_hash(profile.password, password):
                flash('Logged in successfully!', category='success')
                login_user(profile, remember=True)
                return redirect(url_for('views.index'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('name does not exist.', category='error')

    return render_template("login.html",profile = current_user)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))
