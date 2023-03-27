from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired

class AddProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    role = SelectField('Role', choices=[('beheerder', 'Beheerder'), ('personeel', 'Personeel')], validators=[DataRequired()])
