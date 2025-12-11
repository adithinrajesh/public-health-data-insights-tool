import pandas as pd
import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "health_data.db")
DB_PATH = os.path.abspath(DB_PATH)

def create_connection():
    return sqlite3.connect(DB_PATH)

def load_data_from_db():
    conn = create_connection()
    df = pd.read_sql_query("SELECT * FROM patients", conn)
    conn.close()
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Strip strings and normalize
    str_cols = ["Name", "Gender", "BloodType", "MedicalCondition", 
                "Doctor", "Hospital", "InsuranceProvider", 
                "AdmissionType", "Medication", "TestResults"]
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()

    # Handle missing numerical values
    if "Age" in df.columns:
        df["Age"] = pd.to_numeric(df["Age"], errors='coerce').fillna(0).astype(int)
    if "BillingAmount" in df.columns:
        df["BillingAmount"] = pd.to_numeric(df["BillingAmount"], errors='coerce').fillna(0.0).astype(float)

    # Dates
    for col in ["DateOfAdmission", "DischargeDate"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Room Number
    if "RoomNumber" in df.columns:
        df["RoomNumber"] = df["RoomNumber"].fillna("Unknown").astype(str)

    return df

def save_cleaned_data(df: pd.DataFrame):
    conn = create_connection()
    df.to_sql("patients", conn, if_exists="replace", index=False)
    conn.close()
    print("✔ Cleaned data saved to database")