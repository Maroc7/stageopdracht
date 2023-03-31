from flask_wtf import FlaskForm
from wtforms import StringField, SelectField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length
from werkzeug.security import generate_password_hash

class AddProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField("password",validators=[DataRequired()])
    role = SelectField('Role', choices=[('beheerder', 'Beheerder'), ('personeel', 'Personeel')], validators=[DataRequired()])


def hash_password(password):
 return generate_password_hash(password)

class LoginForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=60)])
    submit = SubmitField('Inloggen')