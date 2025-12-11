import sqlite3
import pandas as pd
import os

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "health_data.db")
DB_PATH = os.path.abspath(DB_PATH)

def get_connection():
    """Create a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)

# -------------------------------
# Filtering functions
# -------------------------------

def filter_by_hospital(hospital_name):
    """Return all records for a given hospital."""
    conn = get_connection()
    query = "SELECT * FROM patients WHERE Hospital = ?"
    df = pd.read_sql_query(query, conn, params=(hospital_name,))
    conn.close()
    return df

def filter_by_gender(gender):
    """Return all records for a given gender."""
    conn = get_connection()
    query = "SELECT * FROM patients WHERE Gender = ?"
    df = pd.read_sql_query(query, conn, params=(gender,))
    conn.close()
    return df

def filter_by_age_range(min_age, max_age):
    """Return all records within a given age range."""
    conn = get_connection()
    query = "SELECT * FROM patients WHERE Age BETWEEN ? AND ?"
    df = pd.read_sql_query(query, conn, params=(min_age, max_age))
    conn.close()
    return df

def filter_by_admission_date(start_date, end_date):
    """Return all records within a date range. Format: 'YYYY-MM-DD'."""
    conn = get_connection()
    query = "SELECT * FROM patients WHERE DateOfAdmission BETWEEN ? AND ?"
    df = pd.read_sql_query(query, conn, params=(start_date, end_date))
    conn.close()
    return df

# -------------------------------
# Summary functions
# -------------------------------

def summary_by_hospital():
    """Return count of patients and average billing by hospital."""
    conn = get_connection()
    query = """
    SELECT Hospital, COUNT(*) AS PatientCount, AVG(BillingAmount) AS AvgBilling
    FROM patients
    GROUP BY Hospital
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def summary_by_medical_condition():
    """Return count of patients per medical condition."""
    conn = get_connection()
    query = """
    SELECT MedicalCondition, COUNT(*) AS PatientCount
    FROM patients
    GROUP BY MedicalCondition
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def trend_admissions_over_time():
    """Return number of admissions per month."""
    conn = get_connection()
    query = """
    SELECT strftime('%Y-%m', DateOfAdmission) AS Month, COUNT(*) AS Admissions
    FROM patients
    GROUP BY Month
    ORDER BY Month
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def billing_stats():
    """Return min, max, and average billing amount."""
    conn = get_connection()
    query = "SELECT MIN(BillingAmount) AS MinBill, MAX(BillingAmount) AS MaxBill, AVG(BillingAmount) AS AvgBill FROM patients"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
