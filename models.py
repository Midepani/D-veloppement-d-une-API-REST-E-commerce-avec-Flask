from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialisation de l'extension SQLAlchemy
db = SQLAlchemy()

# Définition des modèles
class Utilisateur(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120),unique=True, nullable=False)
    password_hash = db.Column(db.String(255),nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20),nullable=False,default='client')
    date_creation = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Utilisateur {self.nom}>'
        
        
class Produit(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    categorie = db.Column(db.String(50), nullable=False)
    prix = db.Column(db.Float, nullable=False)
    quantite_stock = db.Column(db.Integer, nullable=True)
    date_creation = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Produit {self.nom}>'
        
class Commande(db.Model):
    __tablename__ = 'order'
    
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_commande = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    adresse_livraison=db.Column(db.String(250), nullable=False)
    statut=db.Column(db.String(50), nullable=False, default='en attente')
    # Relation avec les éléments du panier
    items = db.relationship('LigneCommande', backref='commande', lazy=True, cascade='all, delete-orphan')
    utilisateur = db.relationship('Utilisateur', backref='commandes')
    
    def __repr__(self):
        return f'<Commande {self.id}>'

class LigneCommande(db.Model):
    __tablename__ = 'order_item'
    
    id = db.Column(db.Integer, primary_key=True)
    commande_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantite = db.Column(db.Integer, default=1)
    prix_unitaire = db.Column(db.Float, default=1)
    
    # Relation avec le produit
    produit = db.relationship('Produit', backref='order_item')
    
    def __repr__(self):
        return f'<LigneCommande {self.id}, Produit: {self.produit_id}, Qty: {self.quantite}>'

