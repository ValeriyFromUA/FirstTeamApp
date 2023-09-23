from http import HTTPStatus


def test_main_page(client):
    response = client.get('/')
    response_main = client.get('/main')
    assert response.status_code == HTTPStatus.OK
    assert response_main.status_code == HTTPStatus.OK


def test_candidates_page(client):
    response = client.get('/candidates')
    assert response.status_code == HTTPStatus.FOUND


def test_candidate_profile_page(client):
    response = client.get('/candidates/1')
    assert response.status_code == HTTPStatus.FOUND


def test_team_profile_page(client):
    response = client.get('/teams/1')
    assert response.status_code == HTTPStatus.FOUND


def test_opportunities_page(client):
    response = client.get('/opportunities')
    assert response.status_code == HTTPStatus.FOUND


def test_opportunity_page(client):
    response = client.get('/opportunities/1')
    assert response.status_code == HTTPStatus.FOUND