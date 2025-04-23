from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError

import os
 
app = Flask(__name__)
CORS(app)  # Active CORS pour toutes les routes

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://carnetadresses_db_user:nsaHfy3PAXIYdKhQ2Nq9bssP3u0rTUwK@dpg-cvvsnn24d50c739n4b50-a/carnetadresses_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

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

    def to_dict(self):
        return {
            'id': self.id,
            'prenom': self.prenom,
            'nom': self.nom,
            'email_etu': self.email_etu,
            'email_perso': self.email_perso,
            'tel': self.tel,
            'discord_id': self.discord_id,
            'date_naissance': self.date_naissance,
            'groupe': self.groupe,
            'sous_groupe': self.sous_groupe
        }

# Créer la base de données au démarrage (si elle n'existe pas)
with app.app_context():
    db.create_all()

# Routes API CRUD

# 1. Récupérer tous les contacts
@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.order_by(Contact.nom).all()
    return jsonify([c.to_dict() for c in contacts])

# 2. Ajouter un contact
@app.route('/api/contacts', methods=['POST'])
def add_contact():
    data = request.json
    contact = Contact(
        prenom=data['prenom'],
        nom=data['nom'],
        email_etu=data['email_etu'],
        email_perso=data['email_perso'],
        tel=data.get('tel'),
        discord_id=data.get('discord_id'),
        date_naissance=data.get('date_naissance'),
        groupe=data.get('groupe', ''),
        sous_groupe=data.get('sous_groupe', '')
    )
    try:
        db.session.add(contact)
        db.session.commit()
        return jsonify({'message': 'Contact ajouté avec succès'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Doublon détecté (email, téléphone ou Discord ID)'}), 400

# 3. Mettre à jour un contact
@app.route('/api/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    contact = Contact.query.get_or_404(id)
    data = request.json
    contact.nom = data.get('nom', contact.nom)
    contact.prenom = data.get('prenom', contact.prenom)
    contact.email_etu = data.get('email_etu', contact.email_etu)
    contact.email_perso = data.get('email_perso', contact.email_perso)
    contact.tel = data.get('tel', contact.tel)
    contact.discord_id = data.get('discord_id', contact.discord_id)
    contact.date_naissance = data.get('date_naissance', contact.date_naissance)
    contact.groupe = data.get('groupe', contact.groupe)
    contact.sous_groupe = data.get('sous_groupe', contact.sous_groupe)
    try:
        db.session.commit()
        return jsonify({'message': 'Contact mis à jour'})
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Conflit de doublon lors de la mise à jour'}), 400

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
