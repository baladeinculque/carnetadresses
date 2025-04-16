from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import os

app = Flask(__name__)
migrate = Migrate(app, db)
CORS(app)  # Active CORS pour toutes les routes

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://carnetadresses_db_user:nsaHfy3PAXIYdKhQ2Nq9bssP3u0rTUwK@dpg-cvvsnn24d50c739n4b50-a/carnetadresses_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modèle de données pour les contacts
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(100), nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    email_etu = db.Column(db.String(100), nullable=False, unique=True)
    email_perso = db.Column(db.String(100), nullable=False, unique=True)
    date_naissance = db.Column(db.String(100), nullable=True)
    tel = db.Column(db.String(20), nullable=True, unique=True)
    discord_id = db.Column(db.String(100), nullable=True, unique=True)  
    groupe = db.Column(db.String(100), nullable=True)
    sous_groupe = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Contact {self.nom}>'

# Créer la base de données au démarrage (si elle n'existe pas)
with app.app_context():
    db.create_all()

# Routes API CRUD

# 1. Récupérer tous les contacts
@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.order_by(Contact.nom).all()
    return jsonify([{
        'id': c.id,
        'prenom': c.prenom,
        'nom': c.nom,
        'email': c.email,
        'groupe': c.groupe,
        'sous_groupe': c.sous_groupe  # ✅ Ajouté
    } for c in contacts])

# 2. Ajouter un contact
@app.route('/api/contacts', methods=['POST'])
def add_contact():
    data = request.json
    contact = Contact(
        prenom=data['prenom'],
        nom=data['nom'],
        email=data['email'],
        groupe=data.get('groupe', ''),
        sous_groupe=data.get('sous_groupe', '')  # ✅ Ajouté
    )
    db.session.add(contact)
    db.session.commit()
    return jsonify({'message': 'Contact ajouté avec succès'}), 201

# 3. Mettre à jour un contact
@app.route('/api/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    contact = Contact.query.get_or_404(id)
    data = request.json
    contact.nom = data.get('nom', contact.nom)
    contact.prenom = data.get('prenom', contact.prenom)
    contact.email = data.get('email', contact.email)
    contact.groupe = data.get('groupe', contact.groupe)
    contact.sous_groupe = data.get('sous_groupe', contact.sous_groupe)  # ✅ Ajouté
    db.session.commit()
    return jsonify({'message': 'Contact mis à jour'})

# 4. Supprimer un contact
@app.route('/api/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    return jsonify({'message': 'Contact supprimé'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
