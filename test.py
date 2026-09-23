import requests

# 1. Connexion administrateur
login = requests.post(
    "http://127.0.0.1:5000/api/auth/login",
    json={
        "email": "admin@gmail.com",
        "mot_de_passe": "Admin123!"
    }
)

print("Login :", login.status_code)
print("Réponse login :", login.json())

# 2. Récupération du token
token = login.json()["token"]

# 3. Création d'un produit
response = requests.post(
    "http://127.0.0.1:5000/api/produits",
    headers={
        "Authorization": token
    },
    json={
        "id": 4,
        "nom": "iPhone",
        "description": "Smartphone Apple",
        "categorie": "Telephone",
        "prix": 999.99,
        "quantite_stock": 10
        
    }
)

print("POST produit :", response.status_code)
print("Réponse produit :", response.json())