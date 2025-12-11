import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "health_data.db")
DB_PATH = os.path.abspath(DB_PATH)

def create_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS health_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Age INTEGER,
            Gender TEXT,
            BloodType TEXT,
            MedicalCondition TEXT,
            DateOfAdmission TEXT,
            Doctor TEXT,
            Hospital TEXT,
            InsuranceProvider TEXT,
            BillingAmount REAL,
            RoomNumber TEXT,
            AdmissionType TEXT,
            DischargeDate TEXT,
            Medication TEXT,
            TestResults TEXT
        )
    """)
    
    conn.commit()
    conn.close()
    print("Table created successfully.")

def load_csv_to_db(csv_path):
    """Load Kaggle CSV dataset into SQLite database."""
    conn = create_connection()
    df = pd.read_csv(csv_path)

    # Rename columns to match SQLite table
    df.rename(columns={
        "Blood Type": "BloodType",
        "Date of Admission": "DateOfAdmission",
        "Insurance Provider": "InsuranceProvider",
        "Test Results": "TestResults",
    }, inplace=True)

    df.to_sql("patients", conn, if_exists="append", index=False)
    conn.close()
    print("✔ Data loaded into database!")
