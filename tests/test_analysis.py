import pytest
import pandas as pd
import src.analysis
from src.analysis import (
    filter_by_hospital,
    filter_by_gender,
    filter_by_age_range,
    filter_by_admission_date,
    summary_by_hospital,
    summary_by_medical_condition,
    trend_admissions_over_time,
    billing_stats
)

# --------------------------
# Filtering tests
# --------------------------

def test_filter_by_hospital_existing():
    df = filter_by_hospital("General Hospital")
    assert isinstance(df, pd.DataFrame)
    assert "Hospital" in df.columns
    assert all(df["Hospital"] == "General Hospital")

def test_filter_by_hospital_nonexistent():
    df = filter_by_hospital("NonExistentHospital")
    assert df.empty

def test_filter_by_gender_existing():
    df = filter_by_gender("Male")
    assert isinstance(df, pd.DataFrame)
    assert all(df["Gender"] == "Male")

def test_filter_by_gender_nonexistent():
    df = filter_by_gender("UnknownGender")
    assert df.empty

def test_filter_by_age_range_normal():
    df = filter_by_age_range(20, 40)
    assert isinstance(df, pd.DataFrame)
    assert df["Age"].min() >= 20
    assert df["Age"].max() <= 40

def test_filter_by_age_range_no_results():
    df = filter_by_age_range(200, 300)  # impossible age range
    assert df.empty

def test_filter_by_admission_date_valid():
    df = filter_by_admission_date("2023-01-01", "2023-12-31")
    assert isinstance(df, pd.DataFrame)
    # Dates within range
    if not df.empty:
        assert df["DateOfAdmission"].min() >= "2023-01-01"
        assert df["DateOfAdmission"].max() <= "2023-12-31"

def test_filter_by_admission_date_no_results():
    df = filter_by_admission_date("1900-01-01", "1900-12-31")
    assert df.empty

# --------------------------
# Summary tests
# --------------------------

def test_summary_by_hospital():
    df = summary_by_hospital()
    assert isinstance(df, pd.DataFrame)
    assert "Hospital" in df.columns
    assert "PatientCount" in df.columns
    assert "AvgBilling" in df.columns
    # PatientCount should be >= 0
    assert all(df["PatientCount"] >= 0)

def test_summary_by_medical_condition():
    df = summary_by_medical_condition()
    assert isinstance(df, pd.DataFrame)
    assert "MedicalCondition" in df.columns
    assert "PatientCount" in df.columns

def test_trend_admissions_over_time():
    df = trend_admissions_over_time()
    assert isinstance(df, pd.DataFrame)
    assert "Month" in df.columns
    assert "Admissions" in df.columns

def test_billing_stats():
    df = billing_stats()
    assert isinstance(df, pd.DataFrame)
    assert "MinBill" in df.columns
    assert "MaxBill" in df.columns
    assert "AvgBill" in df.columns
