import jwt
from flask import Flask, request, jsonify
from models import db, Utilisateur
from routes.auth import authenti_bp


JWT_SECRET = "d3fb12750c2eff92120742e1b334479e"

app = Flask(__name__)

app.register_blueprint(authenti_bp)

def decode_token(token):
    try:
        return jwt.decode(
            token,
            JWT_SECRET,
            algorithms="HS256"
        )
    except Exception:
        print("Jeton JWT invalide.")
        return
    
def require_authentication(f):
    def wrapper(**kwargs):
        token = request.headers.get("Authorization", "0")
        if not decode_token(token):
            return {"error": "Jeton d'accès invalide."}, 401
        return f(**kwargs)
    return wrapper
    

@app.route('/predict', methods=["GET"])
@require_authentication
def predict():
    return {"message": "Ok !"}, 200

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cart.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de l'extension SQLAlchemy avec notre application
db.init_app(app)

# Création des tables au démarrage de l'application
@app.before_request
def create_tables():
    app.before_request_funcs[None].remove(create_tables)
    
    db.create_all()

# Ajout de quelques produits pour tester
#@app.before_request
def add_sample_data():
   # app.before_request_funcs[None].remove(add_sample_data)
    
    # Vérifier si des produits existent déjà
    if Utilisateur.query.count() == 0:
        utilisateurs = [
            Utilisateur(nom='MIDEPANI', prenom='Sedrick', email= 'midepanichrist@gmail.com',age=33,matricule='0001', mot_de_passe= generate_password_hash('AZ') ),
            Utilisateur(nom='NGOUANDA', prenom='Christ', email='midchrist@rocketmail.com',age= 44,matricule='0002', mot_de_passe = generate_password_hash('BZ')),
            Utilisateur(nom='MAYER', prenom='HPO', email='admin@gmail.com', age=100,matricule='0003',mot_de_passe = generate_password_hash('TE'),role='admin'),
            Utilisateur(nom='MIDEPANI2', prenom='SM', email='admin2@gmail.com', age=100,matricule='0004',mot_de_passe =generate_password_hash('TE'),role='admin')
        ]
        db.session.add_all(utilisateurs)
        db.session.commit()
        
        
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        add_sample_data()

    app.run(debug=True)