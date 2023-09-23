from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from FTApp.config import configurations

login_manager = LoginManager()
db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(configurations[config_name])
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    from FTApp.main.routes import main_router
    app.register_blueprint(main_router)
    from FTApp.auth.routes import auth
    app.register_blueprint(auth)
    return app
