import jwt
from flask import request, jsonify,Blueprint
from models import db, Commande,Produit,LigneCommande
from functools import wraps

JWT_SECRET = "d3fb12750c2eff92120742e1b334479e"


#db.init_app(app)

#Blue print pour les routes Commande
commandes_bp = Blueprint("commandes", __name__)

def check_fields(body, fields):
    # On récupère les champs requis au format 'ensemble'
    required_parameters_set = set(fields)
    # On récupère les champs du corps de la requête au format 'ensemble'
    fields_set = set(body.keys())
    # Si l'ensemble des champs requis n'est pas inclut dans l'ensemble des champs du corps de la requête
    # Alors s'il manque des paramètres et la valeur False sera renvoyée
    return required_parameters_set <= fields_set
    
    
# decorateur pour les requette admin et client la codition client ou admin est gérer dans la fonction décoré. 
def token_exigé(f):
    @wraps(f)
    def wrapper(**kwargs):
        token = request.headers.get("Authorization", "0")

        try:
            decoded = jwt.decode(
                token,
                JWT_SECRET,
                algorithms="HS256"
            )


            return f(decoded, **kwargs)

        except Exception:
            return jsonify({
                "error": "Jeton d'accès invalide."
            }), 401

    return wrapper
    
         
@commandes_bp.route('/api/commandes', methods=['GET'])
@token_exigé
def recuplist_Commande(decoded):
  

    if decoded.get("role") == "admin":
        listecoma = Commande.query.all()
    else:
        listecoma = Commande.query.filter_by(
            utilisateur_id=decoded.get("id_utilisateur")
        ).all()

    result = []

    for commande in listecoma:

        lignes = LigneCommande.query.filter_by(
            commande_id=commande.id
        ).all()

        produits = []

        for ligne in lignes:

            produit = Produit.query.filter_by(
                id=ligne.produit_id
            ).first()

            produits.append({
                "produit_id": ligne.produit_id,
                "nom_produit": produit.nom if produit else None,
                "quantite": ligne.quantite,
                "prix_unitaire": ligne.prix_unitaire
            })

        result.append({
            "id": commande.id,
            "utilisateur_id": commande.utilisateur_id,
            "date_commande": (
                commande.date_commande.isoformat()
                if commande.date_commande else None
            ),
            "adresse_livraison": commande.adresse_livraison,
            "statut": commande.statut,
            "produits": produits
        })

    return jsonify(result), 200

@commandes_bp.route('/api/commandes/<id>', methods=['GET'])
@token_exigé
def recup_Commandeid(decoded,id):
    comaID = Commande.query.filter_by(id=id).first()
    
    if not comaID:
        
         return jsonify({
            "message": "Pas de Commande ayan cet ID"
        }), 404
        
    if decoded.get("role") != "admin" and comaID.utilisateur_id != decoded.get("id_utilisateur"):
        #if comaID.utilisateur_id != decoded.get("id_utilisateur"):
            return jsonify({
                "error": "Accès interdit à cette commande."
            }), 403
    
    resultID = {
        "id": comaID.id,
        "utilisateur_id": comaID.utilisateur_id,
        "date_commande": comaID.date_commande.isoformat() if comaID.date_commande else None,
        "adresse_livraison": comaID.adresse_livraison,
        "statut": comaID.statut
        
    }

    return jsonify(resultID), 200
       
@commandes_bp.route('/api/commandes', methods=['POST'])
@token_exigé
def creation_commande(decoded):
    try:
        body = request.get_json()

        # Vérifier les champs obligatoires
        if not body or not check_fields(
            body,
            {'utilisateur_id', 'adresse_livraison'}
        ):
            return jsonify({
                "error": "Champs manquants, l'adresse de livraison est obligatoire"
            }), 400

        # Le client ne peut créer une commande que pour lui-même
        if decoded.get("role") != "admin":
            if body['utilisateur_id'] != decoded.get("id_utilisateur"):
                return jsonify({
                    "error": "Vous ne pouvez pas cree une commande pour qu'elq1 d'autre."
                }), 403

        # Création de la commande
        new_commande = Commande(
            utilisateur_id=body['utilisateur_id'],
            adresse_livraison=body['adresse_livraison']
            
        )

        db.session.add(new_commande)
        db.session.commit()

        return jsonify({
            'message': 'Commande créée avec succès.',
            'id': new_commande.id,
            'utilisateur_id': new_commande.utilisateur_id,
            'date_commande': new_commande.date_commande.isoformat()
                if new_commande.date_commande else None,
            'adresse_livraison': new_commande.adresse_livraison,
            'statut': new_commande.statut
        }), 201

    except Exception as e:
        db.session.rollback()

        return jsonify({
            'error': str(e)
        }), 500
        
@commandes_bp.route('/api/commandes/<id>/produits', methods=['POST'])
@token_exigé
def ajouter_produit_commande(decoded, id):
    try:
        body = request.get_json()

        # Vérifier les champs obligatoires
        if not body or 'produit_id' not in body or 'quantite' not in body:
            return jsonify({
                'error': 'Les champs produit_id et quantite sont obligatoires.'
            }), 400

        # Vérifier que la commande existe
        commande = Commande.query.filter_by(id=id).first()

        if not commande:
            return jsonify({
                'error': 'Commande non trouvée.'
            }), 404

        # Vérifier que le client est bien propriétaire de la commande
        if decoded.get("role") != "admin":
            if commande.utilisateur_id != decoded.get("id_utilisateur"):
                return jsonify({
                    'error': 'Vous ne pouvez pas modifier cette commande.'
                }), 403

        # Vérifier que le produit existe
        produit = Produit.query.filter_by(
            id=body['produit_id']
        ).first()

        if not produit:
            return jsonify({
                'error': 'Produit non trouvé.'
            }), 404

        # Vérifier que la quantité est valide
        if int(body['quantite']) <= 0:
            return jsonify({
                'error': 'La quantité doit être supérieure à 0.'
            }), 400

        # Vérifier si le produit est déjà dans la commande
        ligne_commande = LigneCommande.query.filter_by(
            commande_id=commande.id,
            produit_id=produit.id
        ).first()

        if ligne_commande:
            # Le produit existe déjà : on augmente la quantité
            ligne_commande.quantite += int(body['quantite'])

        else:
            # Ajouter une nouvelle ligne
            ligne_commande = LigneCommande(
                commande_id=commande.id,
                produit_id=produit.id,
                quantite=int(body['quantite']),
                prix_unitaire=produit.prix
            )

            db.session.add(ligne_commande)

        db.session.commit()

        return jsonify({
            'message': 'Produit ajouté à la commande avec succès.',
            'commande_id': commande.id,
            'produit_id': produit.id,
            'nom_produit': produit.nom,
            'quantite': ligne_commande.quantite,
            'prix_unitaire': ligne_commande.prix_unitaire
        }), 201

    except Exception as e:
        db.session.rollback()

        return jsonify({
            'error': str(e)
        }), 500


@commandes_bp.route('/api/commandes/<id>', methods=['PATCH'])
@token_exigé
def modifier_statut_commande(decoded, id):
    try:
        # Seul un administrateur peut modifier le statut
        if decoded.get("role") != "admin":
            return jsonify({
                'error': 'Accès interdit. Administrateur requis.'
            }), 403

        body = request.get_json()

        if not body or 'statut' not in body:
            return jsonify({
                'error': 'Le champ statut est obligatoire.'
            }), 400

        nouveau_statut = body['statut']

        statuts_autorises = {
            'en attente',
            'validée',
            'expédiée',
            'annulée'
        }

        if nouveau_statut not in statuts_autorises:
            return jsonify({
                'error': 'Statut invalide.'
            }), 400

        # Recherche de la commande
        commande = Commande.query.filter_by(id=id).first()

        if not commande:
            return jsonify({
                'error': 'Commande non trouvée.'
            }), 404

        # Traitement particulier lors de la validation
        if nouveau_statut == 'validée':

            # Évite de retirer le stock une deuxième fois
            if commande.statut != 'en attente':
                return jsonify({
                    'error': 'Seule une commande en attente peut être validée.'
                }), 400

            # Récupération des produits de la commande
            lignes = LigneCommande.query.filter_by(
                commande_id=commande.id
            ).all()

            if not lignes:
                return jsonify({
                    'error': 'Impossible de valider une commande sans produit.'
                }), 400

            # Vérification de TOUT le stock avant modification
            for ligne in lignes:

                produit = Produit.query.filter_by(
                    id=ligne.produit_id
                ).first()

                if not produit:
                    return jsonify({
                        'error': f'Produit {ligne.produit_id} non trouvé.'
                    }), 404

                if produit.quantite_stock is None:
                    return jsonify({
                        'error': f'Stock non défini pour le produit {produit.nom}.'
                    }), 400

                if produit.quantite_stock < ligne.quantite:
                    return jsonify({
                        'error': f'Stock insuffisant pour le produit {produit.nom}.',
                        'stock_disponible': produit.quantite_stock,
                        'quantite_demandee': ligne.quantite
                    }), 400

            # Si tous les produits sont disponibles,
            # on diminue le stock
            for ligne in lignes:

                produit = Produit.query.filter_by(
                    id=ligne.produit_id
                ).first()

                produit.quantite_stock -= ligne.quantite

        # Modification du statut
        commande.statut = nouveau_statut

        db.session.commit()

        return jsonify({
            'message': 'Statut de la commande modifié avec succès.',
            'id': commande.id,
            'statut': commande.statut
        }), 200

    except Exception as e:
        db.session.rollback()

        return jsonify({
            'error': str(e)
        }), 500