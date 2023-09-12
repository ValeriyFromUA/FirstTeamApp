from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager
from FTApp.config import configurations
from flask_bcrypt import Bcrypt

login_manager = LoginManager()
db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(configurations[config_name])
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    from .routes import core
    app.register_blueprint(core)
    return app
