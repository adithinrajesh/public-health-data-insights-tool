import sqlite3
import pandas as pd
import os

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "health_data.db")
DB_PATH = os.path.abspath(DB_PATH)


def get_connection():
    """Return a sqlite3 connection."""
    return sqlite3.connect(DB_PATH)


# -------------------------------
# Fetch unique values for a column
# -------------------------------
def get_unique_values(column):
    """
    Return sorted list of unique, non-null values for a column.
    Useful for dropdowns or validation.
    """
    allowed_columns = [
        "Gender", "Hospital", "MedicalCondition", "Doctor", 
        "AdmissionType", "InsuranceProvider", "BloodType", "Medication", "TestResults"
    ]
    if column not in allowed_columns:
        return []

    conn = get_connection()
    query = f"SELECT DISTINCT {column} FROM patients WHERE {column} IS NOT NULL"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return sorted(df[column].astype(str).tolist())


# -------------------------------
# Universal dynamic filter function
# -------------------------------
def filter_patients(
    min_age=None, max_age=None,
    gender=None,
    hospital=None,
    condition=None,
    doctor=None,
    ad_start=None, ad_end=None,
    bill_min=None, bill_max=None
):
    """
    Returns a pandas DataFrame filtered dynamically based on the provided fields.
    All filters are optional.
    """

    conn = get_connection()
    base_query = "SELECT * FROM patients WHERE 1=1"
    clauses = []
    params = []

    # Age filters
    if min_age is not None:
        clauses.append("Age >= ?")
        params.append(int(min_age))
    if max_age is not None:
        clauses.append("Age <= ?")
        params.append(int(max_age))

    # Text filters (exact match)
    if gender:
        clauses.append("Gender = ?")
        params.append(str(gender))
    if hospital:
        clauses.append("Hospital = ?")
        params.append(str(hospital))
    if condition:
        clauses.append("MedicalCondition LIKE ?")
        params.append(f"%{condition}%")  # partial match
    if doctor:
        clauses.append("Doctor LIKE ?")
        params.append(f"%{doctor}%")  # partial match

    # Date range
    if ad_start and ad_end:
        clauses.append("DateOfAdmission BETWEEN ? AND ?")
        params.extend([ad_start, ad_end])

    # Billing range
    if bill_min is not None:
        clauses.append("BillingAmount >= ?")
        params.append(float(bill_min))
    if bill_max is not None:
        clauses.append("BillingAmount <= ?")
        params.append(float(bill_max))

    # Final query
    if clauses:
        final_query = base_query + " AND " + " AND ".join(clauses)
    else:
        final_query = base_query

    # Execute
    df = pd.read_sql_query(final_query, conn, params=params)
    conn.close()
    return df

import pandas as pd

def get_summary(df, column, agg_type="mean"):
    """
    Return summary statistics for a column.
    agg_type: 'mean', 'min', 'max', 'count'
    """
    if column not in df.columns:
        return None
    
    if agg_type == "mean":
        return df[column].mean()
    elif agg_type == "min":
        return df[column].min()
    elif agg_type == "max":
        return df[column].max()
    elif agg_type == "count":
        return df[column].count()
    else:
        raise ValueError("Unsupported aggregation type")

def group_summary(df, group_col, agg_col, agg_type="mean"):
    """
    Group by `group_col` and aggregate `agg_col` using `agg_type`.
    """
    if group_col not in df.columns or agg_col not in df.columns:
        return pd.DataFrame()
    
    grouped = df.groupby(group_col)[agg_col]
    
    if agg_type == "mean":
        return grouped.mean().reset_index()
    elif agg_type == "min":
        return grouped.min().reset_index()
    elif agg_type == "max":
        return grouped.max().reset_index()
    elif agg_type == "count":
        return grouped.count().reset_index()
    else:
        raise ValueError("Unsupported aggregation type")

def trend_over_time(df, date_col, value_col, freq="M"):
    """
    Summarise trends over time.
    date_col: date column in df
    value_col: column to aggregate
    freq: 'D' daily, 'W' weekly, 'M' monthly
    """
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    trend = df.groupby(pd.Grouper(key=date_col, freq=freq))[value_col].mean().reset_index()
    return trend
