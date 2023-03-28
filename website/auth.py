from flask import Blueprint, render_template, request, redirect, url_for, session
from website.models import User
from website.database import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the user exists and the password is correct
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            # Check if the user has the role of "beheerder"
            if user.role == "beheerder":
                session['user_id'] = user.id
                session['is_admin'] = user.is_admin
                return redirect(url_for('beheerderspagina'))
            else:
                # User does not have the "beheerder" role
                error_msg = "Access denied. Only users with the role of beheerder are allowed to access the beheerderspagina."
                return render_template('login.html', error=error_msg)
        else:
            # Invalid login credentials
            error_msg = "Invalid username or password."
            return render_template('login.html', error=error_msg)

    # Render the login page
    return render_template('login.html')
