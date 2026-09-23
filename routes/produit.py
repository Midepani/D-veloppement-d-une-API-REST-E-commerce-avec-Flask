import jwt
from flask import request, jsonify,Blueprint
from models import db, Produit
from functools import wraps

JWT_SECRET = "d3fb12750c2eff92120742e1b334479e"


#db.init_app(app)

#Blue print pour les routes Produit
produits_bp = Blueprint("produits", __name__)

def check_fields(body, fields):
    # On récupère les champs requis au format 'ensemble'
    required_parameters_set = set(fields)
    # On récupère les champs du corps de la requête au format 'ensemble'
    fields_set = set(body.keys())
    # Si l'ensemble des champs requis n'est pas inclut dans l'ensemble des champs du corps de la requête
    # Alors s'il manque des paramètres et la valeur False sera renvoyée
    return required_parameters_set <= fields_set
    
    
# decorateur pour les requette admin 
def require_admin(f):
    @wraps(f)
    def wrapper(**kwargs):
        token = request.headers.get("Authorization", "0")

        try:
            decoded = jwt.decode(
                token,
                JWT_SECRET,
                algorithms="HS256"
            )

            if decoded.get("role") != "admin":
                return jsonify({
                    "error": "Accès réservé aux administrateurs."
                }), 403

            return f(**kwargs)

        except Exception:
            return jsonify({
                "error": "Jeton d'accès invalide."
            }), 401

    return wrapper
         
@produits_bp.route('/api/produits', methods=['GET'])
def recuplist_produit():
    listeprod = Produit.query.all()
    result = []
    for x in listeprod:
        result.append({
            "id": x.id,
            "nom": x.nom,
            "description": x.description,
            "categorie": x.categorie,
            "prix": x.prix,
            "quantite_stock": x.quantite_stock,
            "date_creation": x.date_creation.isoformat()
        })
    return jsonify(result), 200         
     
   
@produits_bp.route('/api/produits/<id>', methods=['GET'])
def recup_produitid(id):
    prodID = Produit.query.filter_by(id=id).first()
    
    if not prodID:
        
         return jsonify({
            "message": "Pas de produit ayan cet ID"
        }), 404
    
    resultID = {
        "id": prodID.id,
        "nom": prodID.nom,
        "description": prodID.description,
        "categorie": prodID.categorie,
        "prix": prodID.prix,
        "quantite_stock": prodID.quantite_stock,
        "date_creation": prodID.date_creation.isoformat()
    }

    return jsonify(resultID), 200
    
    
@produits_bp.route('/api/produits', methods=['POST'])
@require_admin
def add_prod():
    try:
        body = request.get_json()
        if not check_fields(body, {'id','nom','description','categorie','prix','quantite_stock'}):
            # S'il manque un paramètre on retourne une erreur 400
            return jsonify({'error': "Missing fields."}), 400
            
            
        produit_existant = Produit.query.filter_by(
            id=body['id']
        ).first()
        if  produit_existant:
            return jsonify({'error': 'Ce mail existe deja'}), 404
            
            #creation nouvelle Produit
        new_produit = Produit(
            id= body['id'],
            nom=body['nom'],
            description =body['description'],
            categorie =body['categorie'],
            prix =body['prix'],
            quantite_stock= body['quantite_stock']
            
            
        )
        db.session.add(new_produit)

        db.session.commit()
    
        return jsonify({
            'message': 'Produit créé avec succès',
            'id': new_produit.id,
            'nom': new_produit.nom,
            'description': new_produit.description,
            'categorie': new_produit.categorie,
            'prix': new_produit.prix,
            'quantite_stock':new_produit.quantite_stock,
            'date_creation': new_produit.date_creation
            
             }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': str(e)
        }), 500

@produits_bp.route('/api/produits/<id>', methods=['PATCH'])
@require_admin
def edit_modifiprod(id):
    try:
        body = request.get_json()

        if not check_fields(body, {'quantite_stock'}):
            # S'il manque un paramètre on retourne une erreur 400
            return jsonify({
                'error': "Missing fields."
            }), 400

        modifiprod = Produit.query.filter_by(id=id).first()

        if not modifiprod:
            return jsonify({
                'error': "Product not found."
            }), 404

        modifiprod.quantite_stock = int(body['quantite_stock'])

        db.session.commit()

        return jsonify({
            'message': 'Quantité du produit modifiée avec succès',
            'id': modifiprod.id,
            'quantite_stock': modifiprod.quantite_stock
        }), 200

    except Exception as e:
        db.session.rollback()

        return jsonify({
            'error': str(e)
        }), 500
        
@produits_bp.route('/api/produits/<id>', methods=['DELETE'])
@require_admin
def supp_produit(id):
    try:

        supproduit = Produit.query.filter_by(id=id).first()

        if not supproduit:
            return jsonify({
                'error': 'Product not found.'
            }), 404

        db.session.delete(supproduit)
        db.session.commit()

        return jsonify({
            'message': 'Produit supprimé avec succès'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': str(e)
        }), 500