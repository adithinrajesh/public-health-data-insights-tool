import pytest
from app import create_app
import sys, os
sys.path.append(os.path.abspath("."))

from src.analysis import (
    filter_by_age_range, filter_by_gender, summary_by_hospital
)
from src.logging_setup import logger

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
