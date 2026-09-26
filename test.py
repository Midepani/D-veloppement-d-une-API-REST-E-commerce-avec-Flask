import requests

BASE_URL = "http://127.0.0.1:5000"


# ==============================
# LOGIN CLIENT
# ==============================

client_data = {
    "email": "midepanichrist@gmail.com",
    "mot_de_passe": "Client1234"
}

response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json=client_data
)

print("\n===== LOGIN CLIENT =====")
print("Status :", response.status_code)
print("Réponse :", response.json())

client_token = response.json()["token"]

headers_client = {
    "Authorization": client_token
}


# ==============================
# 1 - CREATION D'UNE COMMANDE
# ==============================

commande_data = {
    "utilisateur_id": 1,
    "adresse_livraison": "10 rue de Paris"
}

response = requests.post(
    f"{BASE_URL}/api/commandes",
    json=commande_data,
    headers=headers_client
)

print("\n===== CREATION COMMANDE =====")
print("Status :", response.status_code)
print("Réponse :", response.json())


# Récupérer automatiquement l'ID de la commande créée
commande_id = response.json()["id"]


# ==============================
# 2 - AJOUTER UN PRODUIT
# ==============================

produit_data = {
    "produit_id": 1,
    "quantite": 2
}

response = requests.post(
    f"{BASE_URL}/api/commandes/{commande_id}/produits",
    json=produit_data,
    headers=headers_client
)

print("\n===== AJOUT PRODUIT COMMANDE =====")
print("Status :", response.status_code)
print("Réponse :", response.json())