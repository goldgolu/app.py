import pytest
from paws_running.app import app, db  

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_homepage(client):
    """Check if homepage (/) is working."""
    response = client.get("/")
    assert response.status_code == 200

def test_health_route(client):
    """Check if health route is working."""
    response = client.get("/health")
    assert response.status_code == 200

def test_database():
    """Check if database initializes properly."""
    try:
        db.create_all()
        assert True
    except Exception:
        assert False
