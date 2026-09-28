from app import app

# obtention des tocken
def obtenir_token_admin(client):
    login = client.post(
        '/api/auth/login',
        json={
            'email': 'admin@gmail.com',
            'mot_de_passe': 'Admin1234'
        }
    )

    assert login.status_code == 200

    return login.json['token']


def obtenir_token_client(client):
    login = client.post(
        '/api/auth/login',
        json={
            'email': 'midepanichrist@gmail.com',
            'mot_de_passe': 'Client1234'
        }
    )

    assert login.status_code == 200

    return login.json['token']

# consultation produits

def test_liste_produits():
    app.config['TESTING'] = True

    with app.test_client() as client:
        response = client.get('/api/produits')

        assert response.status_code == 200


def test_produit_existant():
    app.config['TESTING'] = True

    with app.test_client() as client:
        response = client.get('/api/produits/1')

        assert response.status_code == 200
        assert response.json['id'] == 1


def test_produit_inexistant():
    app.config['TESTING'] = True

    with app.test_client() as client:
        response = client.get('/api/produits/99999')

        assert response.status_code == 404

# droits d'accès 

def test_client_ne_peut_pas_ajouter_produit():
    app.config['TESTING'] = True

    with app.test_client() as client:

        token = obtenir_token_client(client)

        response = client.post(
            '/api/produits',
            headers={
                'Authorization': token
            },
            json={
                'nom': 'Produit test',
                'description': 'Produit créé pour le test',
                'categorie': 'Test',
                'prix': 10.00,
                'quantite_stock': 10
            }
        )

        assert response.status_code == 403


def test_admin_peut_ajouter_produit():
    app.config['TESTING'] = True

    with app.test_client() as client:

        token = obtenir_token_admin(client)

        response = client.post(
            '/api/produits',
            headers={
                'Authorization': token
            },
            json={
                'id': 102,
                'nom': 'Produit test pytest',
                'description': 'Produit créé pour les tests',
                'categorie': 'Test',
                'prix': 10.00,
                'quantite_stock': 10
            }
        )

        assert response.status_code == 201


def test_admin_peut_modifier_stock():
    app.config['TESTING'] = True

    with app.test_client() as client:

        token = obtenir_token_admin(client)

        response = client.patch(
            '/api/produits/1',
            headers={
                'Authorization': token
            },
            json={
                'quantite_stock': 20
            }
        )

        assert response.status_code == 200
        assert response.json['quantite_stock'] == 20

def test_client_ne_peut_pas_modifier_stock():
    app.config['TESTING'] = True

    with app.test_client() as client:

        token = obtenir_token_client(client)

        response = client.patch(
            '/api/produits/1',
            headers={
                'Authorization': token
            },
            json={
                'quantite_stock': 50
            }
        )

        assert response.status_code == 403

def test_admin_peut_supprimer_produit():
    app.config['TESTING'] = True

    with app.test_client() as client:

        token = obtenir_token_admin(client)

        response = client.delete(
            '/api/produits/102',
            headers={
                'Authorization': token
            }
        )

        assert response.status_code == 200