from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash


def hash_password(password):
 return generate_password_hash(password)

class FeestdagForm(FlaskForm):
    datum = StringField('Datum', validators=[DataRequired()], render_kw={"type": "date"})
    naam_nl = StringField('Naam NL', validators=[DataRequired()])
    naam_en = StringField('Naam EN', validators=[DataRequired()])
    naam_fr = StringField('Naam FR', validators=[DataRequired()])
    is_officieel = BooleanField('Officiële feestdag', default=False)
    submit = SubmitField('Opslaan')
