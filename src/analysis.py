from socket import create_connection
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

# 1. Age Range
def filter_by_age_range(min_age, max_age):
    conn = get_connection()
    query = f"SELECT * FROM patients WHERE Age BETWEEN {min_age} AND {max_age}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# 2. Gender
def filter_by_gender(gender):
    conn = get_connection()
    query = f"SELECT * FROM patients WHERE Gender='{gender}'"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# 3. Hospital
def filter_by_hospital(hospitals):
    conn = get_connection()

    if isinstance(hospitals, str):
        hospitals = [hospitals]

    hospital_list = ",".join([f"'{h}'" for h in hospitals])
    query = f"SELECT * FROM patients WHERE Hospital IN ({hospital_list})"

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# 4. Doctor
def filter_by_doctor(doctors):
    conn = get_connection()
    doctor_list = ','.join([f"'{d}'" for d in doctors])
    query = f"SELECT * FROM patients WHERE Doctor IN ({doctor_list})"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# 5. Admission Type
def filter_by_admission_type(adm_types):
    conn = get_connection()
    type_list = ','.join([f"'{t}'" for t in adm_types])
    query = f"SELECT * FROM patients WHERE AdmissionType IN ({type_list})"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# 6. Medical Condition
def filter_by_condition(conditions):
    conn = get_connection()
    cond_list = ','.join([f"'{c}'" for c in conditions])
    query = f"SELECT * FROM patients WHERE MedicalCondition IN ({cond_list})"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# 7. Admission Date Range
def filter_by_admission_date(start_date, end_date):
    conn = get_connection()
    query = f"""
        SELECT * FROM patients
        WHERE DateOfAdmission BETWEEN '{start_date}' AND '{end_date}'
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# 8. Discharge Date Range
def filter_by_discharge_date(start_date, end_date):
    conn = get_connection()
    query = f"""
        SELECT * FROM patients
        WHERE DischargeDate BETWEEN '{start_date}' AND '{end_date}'
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# 9. Billing Amount Range
def filter_by_billing(min_amount, max_amount):
    conn = get_connection()
    query = f"SELECT * FROM patients WHERE BillingAmount BETWEEN {min_amount} AND {max_amount}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# 10. Insurance Provider
def filter_by_insurance(providers):
    conn = get_connection()
    prov_list = ','.join([f"'{p}'" for p in providers])
    query = f"SELECT * FROM patients WHERE InsuranceProvider IN ({prov_list})"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# 11. Test Results
def filter_by_test_results(results):
    conn = get_connection()
    res_list = ','.join([f"'{r}'" for r in results])
    query = f"SELECT * FROM patients WHERE TestResults IN ({res_list})"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# 12. Blood Type
def filter_by_blood_type(blood_types):
    conn = get_connection()
    bt_list = ','.join([f"'{b}'" for b in blood_types])
    query = f"SELECT * FROM patients WHERE BloodType IN ({bt_list})"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# 13. Medication
def filter_by_medication(meds):
    conn = get_connection()
    med_list = ','.join([f"'{m}'" for m in meds])
    query = f"SELECT * FROM patients WHERE Medication IN ({med_list})"
    df = pd.read_sql_query(query, conn)
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

def summary_by_doctor():
    conn = get_connection()
    query = """
    SELECT Doctor, COUNT(*) AS PatientCount
    FROM patients
    GROUP BY Doctor
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def summary_by_admission_type():
    conn = get_connection()
    query = """
    SELECT "Admission Type" AS AdmissionType, COUNT(*) AS PatientCount
    FROM patients
    GROUP BY "Admission Type"
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def summary_by_test_results():
    conn = get_connection()
    query = """
    SELECT "TestResults", COUNT(*) AS PatientCount
    FROM patients
    GROUP BY "TestResults"
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def summary_by_blood_type():
    conn = get_connection()
    query = """
    SELECT "BloodType", COUNT(*) AS PatientCount
    FROM patients
    GROUP BY "BloodType"
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def summary_by_medication():
    conn = get_connection()
    query = """
    SELECT "Medication", COUNT(*) AS PatientCount
    FROM patients
    GROUP BY "Medication"
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def summary_by_insurance_provider():
    conn = get_connection()
    query = """
    SELECT "InsuranceProvider", COUNT(*) AS PatientCount
    FROM patients
    GROUP BY "InsuranceProvider"
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
