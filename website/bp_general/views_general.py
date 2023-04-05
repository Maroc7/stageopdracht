from flask import Blueprint,render_template
from flask_login import current_user
import csv

views_gn = Blueprint("views_general", __name__)

@views_gn.route('/')
def index():
    with open('feestdag_aanvraag.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        niet_bevestigd = sum(1 for row in reader if row['bevestigd'] == 'in behandeling')
        return render_template('index.html', current_user = current_user,niet_bevestigd = niet_bevestigd)
