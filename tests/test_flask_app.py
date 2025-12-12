# tests/test_flask_app.py
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    rv = client.get("/")
    assert b"Welcome to the Public Health Data Insights Tool" in rv.data

def test_filter_age(client):
    rv = client.get("/filter/age?min_age=20&max_age=40")
    assert rv.status_code == 200
    assert b"<table" in rv.data  # HTML table returned

def test_hospital_summary(client):
    rv = client.get("/summary/hospital")
    assert rv.status_code == 200
    assert b"<table" in rv.data
