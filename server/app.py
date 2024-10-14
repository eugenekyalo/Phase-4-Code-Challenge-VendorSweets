# server/app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db) 

# Import your models here
from models import Vendor, Sweet, VendorSweet

# Ensure tables are created when the app starts
with app.app_context():
    db.create_all()

# Route to add a new VendorSweet with price validation
@app.route('/add_vendor_sweet', methods=['POST'])
def add_vendor_sweet():
    data = request.json
    price = data.get('price', 0)

    # Validate price
    if price <= 0:
        return jsonify({"error": "Price must be greater than zero."}), 400

    new_vendor_sweet = VendorSweet(
        vendor_id=data.get('vendor_id'),
        sweet_id=data.get('sweet_id'),
        price=price
    )

    try:
        db.session.add(new_vendor_sweet)
        db.session.commit()
        return jsonify({"message": "VendorSweet created successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Route to get all vendors
@app.route('/vendors', methods=['GET'])
def get_vendors():
    vendors = Vendor.query.all()
    return jsonify([{"id": v.id, "name": v.name} for v in vendors]), 200

# Route to get all sweets
@app.route('/sweets', methods=['GET'])
def get_sweets():
    sweets = Sweet.query.all()
    return jsonify([{"id": s.id, "name": s.name} for s in sweets]), 200

@app.route('/test_db', methods=['GET'])
def test_db():
    try:
        db.create_all()  # Ensure all tables are created
        test_vendor = Vendor(name='Test Vendor')
        db.session.add(test_vendor)
        db.session.commit()
        return jsonify({"message": "Test entry added!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
