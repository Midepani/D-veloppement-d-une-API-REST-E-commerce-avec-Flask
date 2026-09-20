import requests

url = "http://127.0.0.1:5000/api/auth/login"

donnees = {
    "email": "midepanichrist@gmail.com",
     "mot_de_passe": "AZ"
}

response = requests.post(url, json=donnees)

print("Status :", response.status_code)
print("Réponse :", response.json())
