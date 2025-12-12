import pytest
import sqlite3
import os
import pandas as pd

TEST_DB = "db/test_health.db"

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    # Ensure db folder exists
    os.makedirs("db", exist_ok=True)

    # Create test database
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            Age INTEGER,
            Gender TEXT,
            Hospital TEXT,
            Doctor TEXT,
            AdmissionType TEXT,
            MedicalCondition TEXT,
            DateOfAdmission TEXT,
            DischargeDate TEXT,
            BillingAmount REAL,
            InsuranceProvider TEXT,
            TestResults TEXT,
            BloodType TEXT,
            Medication TEXT
        )
    """)

    sample_data = [
        (25, "Male", "General Hospital", "Dr. A", "Emergency", "Flu", "2023-01-05", "2023-01-10", 200.0, "AIA", "Positive", "O+", "Med1"),
        (35, "Female", "City Hospital", "Dr. B", "Routine", "Covid", "2023-03-01", "2023-03-05", 500.0, "AXA", "Negative", "A+", "Med2"),
    ]

    cursor.executemany("""
        INSERT INTO patients VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, sample_data)

    conn.commit()
    conn.close()

    # Modify environment variable so analysis.py uses test DB
    os.environ["TEST_DB_PATH"] = os.path.abspath(TEST_DB)
