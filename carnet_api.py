from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Modèle de données ---
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    groupe = db.Column(db.String(100))

# --- Créer la base de données ---
with app.app_context():
    db.create_all()

# --- Routes API CRUD ---
@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    return jsonify([{
    'id': c.id,
    'nom': c.nom,
    'prenom': c.prenom,
    'email': c.email,
    'groupe': c.groupe
} for c in contacts])

@app.route('/api/contacts', methods=['POST'])
def add_contact():
    data = request.json
    contact = Contact(
        nom=data['nom'],
        prenom=data['prenom'],
        email=data['email'],
        groupe=data.get('groupe', '')
    )
    db.session.add(contact)
    db.session.commit()
    return jsonify({'message': 'Contact ajouté avec succès'}), 201

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

@app.route('/api/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    return jsonify({'message': 'Contact supprimé'})

if __name__ == '__main__':
    app.run(debug=True)
