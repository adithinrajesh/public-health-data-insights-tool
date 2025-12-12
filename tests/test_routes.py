import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    return app.test_client()

def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"html" in response.data.lower()  # crude check

def test_filter_age_route(client):
    response = client.get("/filter/age?min_age=20&max_age=30")
    assert response.status_code == 200
    assert b"<table" in response.data  # should return HTML table

def test_hospital_summary_route(client):
    response = client.get("/summary/hospital")
    assert response.status_code == 200
    assert b"<table" in response.data
