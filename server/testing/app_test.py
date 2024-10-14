# server/testing/app_test.py
import pytest
from models import Vendor, Sweet, VendorSweet

def test_add_vendor_sweet(test_client):
    # Create a vendor and sweet first
    vendor = Vendor(name='Test Vendor')
    sweet = Sweet(name='Test Sweet')
    db.session.add(vendor)
    db.session.add(sweet)
    db.session.commit()

    # Valid request
    response = test_client.post('/add_vendor_sweet', json={'vendor_id': vendor.id, 'sweet_id': sweet.id, 'price': 5.0})
    assert response.status_code == 201

    # Invalid request (negative price)
    response = test_client.post('/add_vendor_sweet', json={'vendor_id': vendor.id, 'sweet_id': sweet.id, 'price': -1.0})
    assert response.status_code == 400
    assert response.get_json()["error"] == "Price must be greater than zero."

def test_get_vendors(test_client):
    vendor = Vendor(name='Another Vendor')
    db.session.add(vendor)
    db.session.commit()

    response = test_client.get('/vendors')
    assert response.status_code == 200
    assert len(response.get_json()) > 0

def test_get_sweets(test_client):
    sweet = Sweet(name='Another Sweet')
    db.session.add(sweet)
    db.session.commit()

    response = test_client.get('/sweets')
    assert response.status_code == 200
    assert len(response.get_json()) > 0
