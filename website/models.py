from. import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Profile(db.model,UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.Text, unique=True)
        role = db.Column(db.Text)
