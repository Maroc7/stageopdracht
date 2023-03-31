from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from os import path
from website.views import views
from website.database import db
from website.config import DB_NAME
from flask_login import LoginManager

app = Flask(__name__)
login_manager = LoginManager()

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:root@localhost:3306/{DB_NAME}'

    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    app.register_blueprint(views, url_prefix='/')
    app.cli.add_command('db',MigrateCommand)

    # Import auth here to avoid circular import issues
    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')

    return app
