import jwt
from flask import Flask, request, jsonify
from models import db, Utilisateur,Produit
from routes.auth import authenti_bp
from routes.produit import produits_bp


JWT_SECRET = "d3fb12750c2eff92120742e1b334479e"

app = Flask(__name__)

# Configuration de la base de données
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///digimarket.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/blent/D-veloppement-d-une-API-REST-E-commerce-avec-Flask/digimarket.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de l'extension SQLAlchemy avec notre application
db.init_app(app)

app.register_blueprint(authenti_bp)
app.register_blueprint(produits_bp)


#Remplissage de la base digimarket.db avec quelques données de test. 

@app.before_request
def add_sample_data():
    app.before_request_funcs[None].remove(add_sample_data)
    
    # Vérifier si des produits existent déjà
    if Produit.query.count() == 0:
        produits = [
            Produit(id= 1, nom ='Red-mi', description='Smartphone pliable', categorie='Telephone', prix=799.99, quantite_stock=50),
            Produit(id= 2, nom ='Lenova', description='Thinkpad ix3', categorie='PC Portables', prix=900.99, quantite_stock=5),
            Produit(id= 3, nom ='Samsung', description='TV écrant plasma', categorie='AudioVision', prix=2000, quantite_stock=100)
        ]
        db.session.add_all(produits)
        db.session.commit()


# Gestion de l'hautntification GWT
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

       
if __name__ == "__main__":
   # with app.app_context():
       # db.create_all()
       # add_sample_data()

    app.run(debug=True)