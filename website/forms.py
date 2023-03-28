from flask_wtf import FlaskForm
from wtforms import StringField, SelectField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length

class AddProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    role = SelectField('Role', choices=[('beheerder', 'Beheerder'), ('personeel', 'Personeel')], validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = StringField('Gebruikersnaam', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Wachtwoord', validators=[DataRequired(), Length(min=6, max=60)])
    submit = SubmitField('Inloggen')