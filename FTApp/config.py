import os
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
CV_DIR = os.path.join(STATIC_DIR, 'cv')
TEAM_LOGO_DIR = os.path.join(STATIC_DIR, 'team_logo')
CANDIDATE_PIC_DIR = os.path.join(STATIC_DIR, 'candidate_pic')
CURRENT_DATATIME = datetime.now()
FILENAME_PREFIX = CURRENT_DATATIME.strftime('%Y%m%d%H%M%S')


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fsfhshsughusgh323fdfgdg'

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
    TESTING = True


configurations = {
    'base': Config,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
