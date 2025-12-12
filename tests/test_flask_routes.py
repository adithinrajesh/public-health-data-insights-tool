import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Filter Patients" in response.data

def test_age_filter_route(client):
    response = client.get("/filter/age?min_age=20&max_age=40")
    assert response.status_code == 200
    assert b"<table" in response.data

def test_summary_hospital_route(client):
    response = client.get("/summary/hospital")
    assert response.status_code == 200
    assert b"<table" in response.data
