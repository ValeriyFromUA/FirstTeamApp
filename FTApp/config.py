import os

from FTApp.constants import SECRET

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = SECRET

    # Turn off Flask-SQLAlchemy event system
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'prod.db')


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')


configurations = {
    'base': Config,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
