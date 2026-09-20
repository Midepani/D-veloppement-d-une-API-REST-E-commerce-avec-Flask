from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialisation de l'extension SQLAlchemy
db = SQLAlchemy()

# Définition des modèles
class Utilisateur(db.Model):
    __tablename__ = 'Utilisateurs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    matricule = db.Column(db.String(10),unique=True,nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100),unique=True, nullable=False)
    age = db.Column(db.Integer,nullable=False)
    mot_de_passe = db.Column(db.String(255),nullable=False)
    role = db.Column(db.String(20),nullable=False,default='client')
    
def __repr__(self):
        return f'<Utilisateur {self.nom}>'

