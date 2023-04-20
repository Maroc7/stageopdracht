from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path
from website.bp_feestdag import views_fd
from website.bp_profile import views_pf
from website.bp_general import views_gn
from website.database import db
from website.config import DB_NAME
from flask_login import LoginManager
from .bp_feestdag import bp_feestdag

app = Flask(__name__)
login_manager = LoginManager()
#blueprints registreren


def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:root@localhost:3306/{DB_NAME}'

    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    app.register_blueprint(views_fd, url_prefix='/')
    app.register_blueprint(views_gn, url_prefix='/')
    app.register_blueprint(views_pf , url_prefix='/')
    from .bp_profile.auth import auth
    app.register_blueprint(auth, url_prefix='/')

    return app


    