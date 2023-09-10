from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from FTApp.config import configurations

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(configurations[config_name])
    db.init_app(app)

    return app


app = create_app(config_name='development')
with app.app_context():
    db.create_all()
