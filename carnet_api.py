from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Active CORS pour toutes les routes

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modèle de données pour les contacts
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(100), nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    groupe = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Contact {self.nom}>'

# Créer la base de données au démarrage (si elle n'existe pas)
with app.app_context():
    db.create_all()

# Routes API CRUD

# 1. Récupérer tous les contacts
@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    return jsonify([{
        'id': c.id,
        'prenom': c.prenom,
        'nom': c.nom,
        'email': c.email,
        'groupe': c.groupe
    } for c in contacts])

# 2. Ajouter un contact
@app.route('/api/contacts', methods=['POST'])
def add_contact():
    data = request.json
    contact = Contact(
        prenom=data['prenom'],
        nom=data['nom'],
        email=data['email'],
        groupe=data.get('groupe', '')
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
