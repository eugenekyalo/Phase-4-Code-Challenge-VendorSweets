# server/testing/conftest.py
import pytest
from app import app, db

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create all tables in the in-memory database
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()  # Clean up the database after tests
