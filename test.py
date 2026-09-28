import requests

BASE_URL = "http://127.0.0.1:5000"


# ==================================================
# 1. LOGIN CLIENT
# ==================================================

client_data = {
    "email": "midepanichrist@gmail.com",
    "mot_de_passe": "Client1234"
}

response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json=client_data
)

print("\n===== 1. LOGIN CLIENT =====")
print("Status :", response.status_code)
print("Réponse :", response.json())

if response.status_code != 200:
    print("Le login client a échoué.")
    exit()

client_token = response.json()["token"]

headers_client = {
    "Authorization": client_token
}


# ==================================================
# 2. CREATION DE LA COMMANDE 1
# ==================================================

commande_data = {
    "utilisateur_id": 1,
    "adresse_livraison": "10 rue de Paris"
}

response = requests.post(
    f"{BASE_URL}/api/commandes",
    json=commande_data,
    headers=headers_client
)

print("\n===== 2. CREATION COMMANDE =====")
print("Status :", response.status_code)
print("Réponse :", response.json())

if response.status_code != 201:
    print("La création de la commande a échoué.")
    exit()

commande_id = response.json()["id"]


# ==================================================
# 3. AJOUT DE 2 RED-MI DANS LA COMMANDE
# ==================================================

produit_data = {
    "produit_id": 1,
    "quantite": 2
}

response = requests.post(
    f"{BASE_URL}/api/commandes/{commande_id}/produits",
    json=produit_data,
    headers=headers_client
)

print("\n===== 3. AJOUT PRODUIT COMMANDE =====")
print("Status :", response.status_code)
print("Réponse :", response.json())

if response.status_code != 201:
    print("L'ajout du produit a échoué.")
    exit()


# ==================================================
# 4. LOGIN ADMIN
# ==================================================

admin_data = {
    "email": "admin@gmail.com",
    "mot_de_passe": "Admin1234"
}

response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json=admin_data
)

print("\n===== 4. LOGIN ADMIN =====")
print("Status :", response.status_code)
print("Réponse :", response.json())

if response.status_code != 200:
    print("Le login admin a échoué.")
    exit()

admin_token = response.json()["token"]

headers_admin = {
    "Authorization": admin_token
}


# ==================================================
# 5. VALIDATION DE LA COMMANDE
# ==================================================

response = requests.patch(
    f"{BASE_URL}/api/commandes/{commande_id}",
    json={
        "statut": "validée"
    },
    headers=headers_admin
)

print("\n===== 5. VALIDATION COMMANDE =====")
print("Status :", response.status_code)
print("Réponse :", response.json())

if response.status_code != 200:
    print("La validation de la commande a échoué.")
    exit()


# ==================================================
# 6. VERIFICATION DU STOCK APRES VALIDATION
# ==================================================

response = requests.get(
    f"{BASE_URL}/api/produits/1"
)

print("\n===== 6. VERIFICATION STOCK APRES VALIDATION =====")
print("Status :", response.status_code)
print("Réponse :", response.json())


# ==================================================
# 7. NOUVELLE COMMANDE POUR TESTER LE STOCK
# ==================================================

commande_test = {
    "utilisateur_id": 1,
    "adresse_livraison": "20 rue de Rouen"
}

response = requests.post(
    f"{BASE_URL}/api/commandes",
    json=commande_test,
    headers=headers_client
)

print("\n===== 7. NOUVELLE COMMANDE TEST =====")
print("Status :", response.status_code)
print("Réponse :", response.json())

if response.status_code != 201:
    print("La nouvelle commande n'a pas pu être créée.")
    exit()

commande_test_id = response.json()["id"]


# ==================================================
# 8. AJOUT DE 1000 RED-MI
# ==================================================

produit_test = {
    "produit_id": 1,
    "quantite": 1000
}

response = requests.post(
    f"{BASE_URL}/api/commandes/{commande_test_id}/produits",
    json=produit_test,
    headers=headers_client
)

print("\n===== 8. AJOUT DE 1000 RED-MI =====")
print("Status :", response.status_code)
print("Réponse :", response.json())

if response.status_code != 201:
    print("L'ajout du produit a échoué.")
    exit()


# ==================================================
# 9. VALIDATION AVEC STOCK INSUFFISANT
# ==================================================

response = requests.patch(
    f"{BASE_URL}/api/commandes/{commande_test_id}",
    json={
        "statut": "validée"
    },
    headers=headers_admin
)

print("\n===== 9. VALIDATION AVEC STOCK INSUFFISANT =====")
print("Status :", response.status_code)
print("Réponse :", response.json())


# ==================================================
# 10. VERIFICATION DU STOCK APRES REFUS
# ==================================================

response = requests.get(
    f"{BASE_URL}/api/produits/1"
)

print("\n===== 10. STOCK APRES REFUS DE VALIDATION =====")
print("Status :", response.status_code)
print("Réponse :", response.json())