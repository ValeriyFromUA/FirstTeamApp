import pytest

from FTApp import create_app, db
from FTApp.auth.models import Team


@pytest.fixture
def client():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
    with app.test_client() as client:
        yield client
    with app.app_context():
        db.drop_all()
