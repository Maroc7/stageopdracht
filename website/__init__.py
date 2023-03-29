from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from os import path
from flask_login import LoginManager
from website.views import views
from website.auth import auth
from website.database import db

DB_NAME = "stage"
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/stage'

    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Add Flask-Migrate commands to the app's CLI
    app.cli.add_command('db',MigrateCommand)
    return app
