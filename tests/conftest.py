import pytest
from app import create_app, db

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "test-secret-key"

@pytest.fixture
def client():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()
