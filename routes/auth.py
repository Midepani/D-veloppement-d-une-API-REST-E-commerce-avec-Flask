import jwt
from flask import request, jsonify,Blueprint
from models import db, Utilisateur
from datetime import datetime, timedelta

# hashage du mot de passe 

from werkzeug.security import generate_password_hash, check_password_hash

JWT_SECRET = "d3fb12750c2eff92120742e1b334479e"

authenti_bp = Blueprint("authenti", __name__)

def check_fields(body, fields):
    # On récupère les champs requis au format 'ensemble'
    required_parameters_set = set(fields)
    # On récupère les champs du corps de la requête au format 'ensemble'
    fields_set = set(body.keys())
    # Si l'ensemble des champs requis n'est pas inclut dans l'ensemble des champs du corps de la requête
    # Alors s'il manque des paramètres et la valeur False sera renvoyée
    return required_parameters_set <= fields_set

@authenti_bp.route('/api/auth/login', methods=['POST'])
def generate_token():
    body = request.get_json()
    
    email = body.get('email')
    mot_de_passe = body.get('mot_de_passe')

    if not email or not mot_de_passe:
            return jsonify({
                'error': 'Email et mot de passe obligatoires.'
            }), 400

        # Recherche de l'utilisateur dans SQLite
    utilisateur = Utilisateur.query.filter_by(
            email=email
        ).first()

        # Utilisateur inexistant ou mot de passe incorrect
    if not utilisateur or  not check_password_hash(
    utilisateur.mot_de_passe,
    mot_de_passe):
            return jsonify({
                'error': 'Email ou mot de passe invalide.'
            }), 401
            
    token = jwt.encode(
            {
            
                "id_utilisateur": utilisateur.id,
                "email": utilisateur.email,
                "role": utilisateur.role,                
                "exp": datetime.utcnow() + timedelta(hours=1),
                
                
            },
            JWT_SECRET,
            algorithm="HS256"
        )
    return jsonify({"token": token}), 200
@authenti_bp.route('/api/auth/register', methods=['POST'])
def add_users():
    try:
        body = request.get_json()
        if not check_fields(body, {'email','nom', 'prenom', 'age','mot_de_passe','matricule'}):
            # S'il manque un paramètre on retourne une erreur 400
            return jsonify({'error': "Missing fields."}), 400
            
            
        utilisateur = Utilisateur.query.filter_by(
            matricule=body['matricule']
        ).first()
        if  utilisateur:
            return jsonify({'error': 'Ce matricule existe deja'}), 404
            
            #creation nouvelle utilisateur
        nouvel_utilisateur = Utilisateur(

            matricule=body['matricule'],
            nom=body['nom'],
            prenom=body['prenom'],
            email=body['email'],
            age=body['age'],
            mot_de_passe=generate_password_hash(body['mot_de_passe'])

        )


       
        db.session.add(nouvel_utilisateur)

        db.session.commit()
    
        return jsonify({
            'message': 'Utilisateur créé avec succès',
            'matricule': nouvel_utilisateur.matricule
             }), 201


    except Exception as e:

        db.session.rollback()

        return jsonify({
            'error': str(e)
        }), 500