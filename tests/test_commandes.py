from app import app


def obtenir_token_client(client):
    response = client.post(
        '/api/auth/login',
        json={
            'email': 'midepanichrist@gmail.com',
            'mot_de_passe': 'Client1234'
        }
    )

    assert response.status_code == 200

    return response.json['token']

def obtenir_token_admin(client):
    response = client.post(
        '/api/auth/login',
        json={
            'email': 'admin@gmail.com',
            'mot_de_passe': 'Admin1234'
        }
    )

    assert response.status_code == 200

    return response.json['token']


def test_client_peut_voir_ses_commandes():
    app.config['TESTING'] = True

    with app.test_client() as client:

        token = obtenir_token_client(client)

        response = client.get(
            '/api/commandes',
            headers={
                'Authorization': token
            }
        )


        assert response.status_code == 200

def test_client_recoit_une_liste_de_commandes():
    app.config['TESTING'] = True

    with app.test_client() as client:

        token = obtenir_token_client(client)

        response = client.get(
            '/api/commandes',
            headers={
                'Authorization': token
            }
        )

        assert response.status_code == 200
        assert isinstance(response.json, list)

def test_client_peut_voir_une_commande():
    app.config['TESTING'] = True

    with app.test_client() as client:

        token = obtenir_token_client(client)

        response = client.get(
            '/api/commandes/1',
            headers={
                'Authorization': token
            }
        )

        assert response.status_code == 200
        assert response.json['id'] == 1
def test_commande_inexistante():
    app.config['TESTING'] = True

    with app.test_client() as client:

        token = obtenir_token_client(client)

        response = client.get(
            '/api/commandes/99999',
            headers={
                'Authorization': token
            }
        )

        assert response.status_code == 404

def test_client_peut_creer_une_commande():
    app.config['TESTING'] = True

    with app.test_client() as client:

        token = obtenir_token_client(client)

        response = client.post(
            '/api/commandes',
            headers={
                'Authorization': token
            },
            json={
                'utilisateur_id': 1,
                'adresse_livraison': '10 rue de Test, 76000 Rouen'
            }
        )

        assert response.status_code == 201
        assert 'id' in response.json

def test_client_ne_peut_pas_creer_commande_pour_un_autre_utilisateur():
    app.config['TESTING'] = True

    with app.test_client() as client:

        token = obtenir_token_client(client)

        response = client.post(
            '/api/commandes',
            headers={
                'Authorization': token
            },
            json={
                'utilisateur_id': 2,
                'adresse_livraison': '10 rue de Test, 76000 Rouen'
            }
        )

        assert response.status_code == 403

def test_client_peut_ajouter_produit_commande():
    app.config['TESTING'] = True

    with app.test_client() as client:

        token = obtenir_token_client(client)

        # Création d'une commande
        response_commande = client.post(
            '/api/commandes',
            headers={
                'Authorization': token
            },
            json={
                'utilisateur_id': 1,
                'adresse_livraison': '10 rue de Test, 76000 Rouen'
            }
        )

        assert response_commande.status_code == 201

        id_commande = response_commande.json['id']

        # Ajout d'un produit
        response_produit = client.post(
            f'/api/commandes/{id_commande}/produits',
            headers={
                'Authorization': token
            },
            json={
                'produit_id': 1,
                'quantite': 2
            }
        )

        assert response_produit.status_code == 201

def test_ajout_produit_avec_quantite_invalide():
    app.config['TESTING'] = True

    with app.test_client() as client:

        token = obtenir_token_client(client)

        # Création d'une commande
        response_commande = client.post(
            '/api/commandes',
            headers={
                'Authorization': token
            },
            json={
                'utilisateur_id': 1,
                'adresse_livraison': '10 rue de Test, 76000 Rouen'
            }
        )

        assert response_commande.status_code == 201

        id_commande = response_commande.json['id']

        # Tentative d'ajout avec une quantité de 0
        response_produit = client.post(
            f'/api/commandes/{id_commande}/produits',
            headers={
                'Authorization': token
            },
            json={
                'produit_id': 1,
                'quantite': 0
            }
        )

        assert response_produit.status_code == 400

def test_ajout_produit_inexistant():
    app.config['TESTING'] = True

    with app.test_client() as client:

        token = obtenir_token_client(client)

        # Création d'une commande
        response_commande = client.post(
            '/api/commandes',
            headers={
                'Authorization': token
            },
            json={
                'utilisateur_id': 1,
                'adresse_livraison': '10 rue de Test, 76000 Rouen'
            }
        )

        assert response_commande.status_code == 201

        id_commande = response_commande.json['id']

        # Tentative d'ajout d'un produit inexistant
        response_produit = client.post(
            f'/api/commandes/{id_commande}/produits',
            headers={
                'Authorization': token
            },
            json={
                'produit_id': 99999,
                'quantite': 2
            }
        )

        assert response_produit.status_code == 404
def test_client_ne_peut_pas_valider_commande():
    app.config['TESTING'] = True

    with app.test_client() as client:

        token = obtenir_token_client(client)

        # Création d'une commande
        response_commande = client.post(
            '/api/commandes',
            headers={
                'Authorization': token
            },
            json={
                'utilisateur_id': 1,
                'adresse_livraison': '10 rue de Test, 76000 Rouen'
            }
        )

        assert response_commande.status_code == 201

        id_commande = response_commande.json['id']

        # Le client essaie de valider la commande
        response_validation = client.patch(
            f'/api/commandes/{id_commande}',
            headers={
                'Authorization': token
            },
            json={
                'statut': 'validée'
            }
        )

        assert response_validation.status_code == 403

def test_admin_peut_valider_commande_et_reduire_stock():
    app.config['TESTING'] = True

    with app.test_client() as client:

        # Token client
        token_client = obtenir_token_client(client)

        # Token admin
        token_admin = obtenir_token_admin(client)

        # Création de la commande
        response_commande = client.post(
            '/api/commandes',
            headers={
                'Authorization': token_client
            },
            json={
                'utilisateur_id': 1,
                'adresse_livraison': '10 rue de Test, 76000 Rouen'
            }
        )

        assert response_commande.status_code == 201

        id_commande = response_commande.json['id']

        # Récupération du produit avant la commande
        response_produit = client.get('/api/produits/1')

        assert response_produit.status_code == 200

        stock_avant = response_produit.json['quantite_stock']

        # Ajout de 2 produits à la commande
        response_ajout = client.post(
            f'/api/commandes/{id_commande}/produits',
            headers={
                'Authorization': token_client
            },
            json={
                'produit_id': 1,
                'quantite': 2
            }
        )

        assert response_ajout.status_code == 201

        # Validation par l'administrateur
        response_validation = client.patch(
            f'/api/commandes/{id_commande}',
            headers={
                'Authorization': token_admin
            },
            json={
                'statut': 'validée'
            }
        )

        assert response_validation.status_code == 200
        assert response_validation.json['statut'] == 'validée'

        # Vérification du stock après validation
        response_produit = client.get('/api/produits/1')

        stock_apres = response_produit.json['quantite_stock']

        assert stock_apres == stock_avant - 2

def test_admin_ne_peut_pas_valider_si_stock_insuffisant():
    app.config['TESTING'] = True

    with app.test_client() as client:

        # Token client
        token_client = obtenir_token_client(client)

        # Token admin
        token_admin = obtenir_token_admin(client)

        # Récupération du stock avant
        response_produit = client.get('/api/produits/1')

        assert response_produit.status_code == 200

        stock_avant = response_produit.json['quantite_stock']

        # Création de la commande
        response_commande = client.post(
            '/api/commandes',
            headers={
                'Authorization': token_client
            },
            json={
                'utilisateur_id': 1,
                'adresse_livraison': '10 rue de Test, 76000 Rouen'
            }
        )

        assert response_commande.status_code == 201

        id_commande = response_commande.json['id']

        # Ajout d'une quantité supérieure au stock disponible
        response_ajout = client.post(
            f'/api/commandes/{id_commande}/produits',
            headers={
                'Authorization': token_client
            },
            json={
                'produit_id': 1,
                'quantite': stock_avant + 100
            }
        )

        assert response_ajout.status_code == 201

        # L'administrateur essaye de valider la commande
        response_validation = client.patch(
            f'/api/commandes/{id_commande}',
            headers={
                'Authorization': token_admin
            },
            json={
                'statut': 'validée'
            }
        )

        # La validation doit être refusée
        assert response_validation.status_code == 400

        # Vérification de la commande
        response_commande = client.get(
            f'/api/commandes/{id_commande}',
            headers={
                'Authorization': token_client
            }
        )

        assert response_commande.status_code == 200
        assert response_commande.json['statut'] == 'en attente'

        # Vérification du stock
        response_produit = client.get('/api/produits/1')

        stock_apres = response_produit.json['quantite_stock']

        assert stock_apres == stock_avant


def test_client_peut_consulter_lignes_commande():
    app.config['TESTING'] = True

    with app.test_client() as client:

        # Connexion du client
        token_client = obtenir_token_client(client)

        # Création d'une commande
        response_commande = client.post(
            '/api/commandes',
            headers={
                'Authorization': token_client
            },
            json={
                'utilisateur_id': 1,
                'adresse_livraison': '10 rue de Test, 76000 Rouen'
            }
        )

        assert response_commande.status_code == 201

        id_commande = response_commande.json['id']

        # Ajout d'un produit à la commande
        response_ajout = client.post(
            f'/api/commandes/{id_commande}/produits',
            headers={
                'Authorization': token_client
            },
            json={
                'produit_id': 1,
                'quantite': 2
            }
        )

        assert response_ajout.status_code == 201

        # Consultation des lignes de la commande
        response_lignes = client.get(
            f'/api/commandes/{id_commande}/lignes',
            headers={
                'Authorization': token_client
            }
        )

        assert response_lignes.status_code == 200

        # Vérification de la ligne
        assert len(response_lignes.json) == 1
        assert response_lignes.json[0]['produit_id'] == 1
        assert response_lignes.json[0]['quantite'] == 2