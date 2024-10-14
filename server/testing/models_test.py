import pytest
from app import app
from models import db, Sweet, Vendor, VendorSweet
from faker import Faker

@pytest.fixture(scope='module')
def test_client():
    # Create a test client
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create the database schema
        yield client
        with app.app_context():
            db.drop_all()  # Clean up after tests

class TestVendorSweet:
    '''Class VendorSweet in models.py'''

    def test_price_0_or_greater(self, test_client):
        '''requires price >= 0.'''

        with app.app_context():
            sweet = Sweet(name=Faker().name())
            vendor = Vendor(name=Faker().name())
            db.session.add_all([sweet, vendor])
            db.session.commit()

            vendor_sweet = VendorSweet(
                vendor_id=vendor.id, sweet_id=sweet.id, price=0)
            db.session.add(vendor_sweet)
            db.session.commit()

            # Ensure the vendor_sweet was created
            assert vendor_sweet.id is not None

    def test_price_too_low(self, test_client):
        '''requires non negative price .'''

        with app.app_context():
            sweet = Sweet(name=Faker().name())
            vendor = Vendor(name=Faker().name())
            db.session.add_all([sweet, vendor])
            db.session.commit()

            with pytest.raises(ValueError):
                vendor_sweet = VendorSweet(
                    vendor_id=vendor.id, sweet_id=sweet.id, price=-1)
                db.session.add(vendor_sweet)
                db.session.commit()

    def test_price_none(self, test_client):
        '''requires non negative price .'''

        with app.app_context():
            sweet = Sweet(name=Faker().name())
            vendor = Vendor(name=Faker().name())
            db.session.add_all([sweet, vendor])
            db.session.commit()

            with pytest.raises(ValueError):
                vendor_sweet = VendorSweet(
                    vendor_id=vendor.id, sweet_id=sweet.id, price=None)
                db.session.add(vendor_sweet)
                db.session.commit()
