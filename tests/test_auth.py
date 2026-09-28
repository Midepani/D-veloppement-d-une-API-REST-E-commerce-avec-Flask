import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


def test_login_client(client):
    response = client.post(
        '/api/auth/login',
        json={
            'email': 'midepanichrist@gmail.com',
            'mot_de_passe': 'Client1234'
        }
    )

    assert response.status_code == 200
    assert 'token' in response.json


def test_login_admin(client):
    response = client.post(
        '/api/auth/login',
        json={
            'email': 'admin@gmail.com',
            'mot_de_passe': 'Admin1234'
        }
    )

    assert response.status_code == 200
    assert 'token' in response.json


def test_mauvais_mot_de_passe(client):
    response = client.post(
        '/api/auth/login',
        json={
            'email': 'admin@gmail.com',
            'mot_de_passe': 'mauvais_mot_de_passe'
        }
    )

    assert response.status_code == 401


def test_utilisateur_inexistant(client):
    response = client.post(
        '/api/auth/login',
        json={
            'email': 'utilisateur_inexistant@gmail.com',
            'mot_de_passe': 'Test1234'
        }
    )

    assert response.status_code == 401