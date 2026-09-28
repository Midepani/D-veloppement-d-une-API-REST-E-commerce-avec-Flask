import requests

BASE_URL = "http://127.0.0.1:5000"


# ==================================================
# LOGIN CLIENT
# ==================================================

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

if response.status_code != 200:
    print("Le login client a échoué.")
    exit()

client_token = response.json()["token"]

headers_client = {
    "Authorization": client_token
}


# ==================================================
# HISTORIQUE DES COMMANDES
# ==================================================

response = requests.get(
    f"{BASE_URL}/api/commandes",
    headers=headers_client
)

print("\n===== HISTORIQUE DES COMMANDES =====")
print("Status :", response.status_code)
print("Réponse :", response.json())