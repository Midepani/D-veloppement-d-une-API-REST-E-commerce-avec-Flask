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

