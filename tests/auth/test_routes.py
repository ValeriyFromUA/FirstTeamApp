from http import HTTPStatus

from tests.conftest import client


def test_registration_page(client):
    response = client.get('/registration')
    assert response.status_code == HTTPStatus.OK


def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == HTTPStatus.OK


def test_logout_page(client):
    response = client.get('/logout')
    assert response.status_code == HTTPStatus.FOUND
