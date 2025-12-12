# app/routes.py
from flask import Blueprint, render_template, request
import pandas as pd
from src.analysis import (
    filter_by_age_range,
    filter_by_gender,
    filter_by_hospital,
    summary_by_hospital,
    summary_by_medical_condition
)
from src.logging_setup import logger

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():
    logger.info("Visited index page")
    return render_template("index.html")

# -------------------
# Filtering routes
# -------------------
@main_bp.route("/filter/age", methods=["GET"])
def filter_age():
    min_age = int(request.args.get("min_age", 0))
    max_age = int(request.args.get("max_age", 120))
    logger.info(f"Filtering by age: {min_age}-{max_age}")
    df = filter_by_age_range(min_age, max_age)
    return df.to_html(classes="table table-striped", index=False)

@main_bp.route("/filter/gender", methods=["GET"])
def filter_gender():
    gender = request.args.get("gender", "Male")
    logger.info(f"Filtering by gender: {gender}")
    df = filter_by_gender(gender)
    return df.to_html(classes="table table-striped", index=False)

@main_bp.route("/filter/hospital", methods=["GET"])
def filter_hosp():
    hospital = request.args.get("hospital", "")
    if not hospital:
        return "<p>Please provide a hospital name</p>"
    df = filter_by_hospital(hospital)
    logger.info(f"Filtering by hospital: {hospital}")
    return df.to_html(classes="table table-striped", index=False)

# -------------------
# Summary routes
# -------------------
@main_bp.route("/summary/hospital")
def hospital_summary():
    logger.info("Getting summary by hospital")
    df = summary_by_hospital()
    return df.to_html(classes="table table-striped", index=False)

@main_bp.route("/summary/medical-condition")
def condition_summary():
    logger.info("Getting summary by medical condition")
    df = summary_by_medical_condition()
    return df.to_html(classes="table table-striped", index=False)

# app/routes.py
from flask import Blueprint, render_template, request
import pandas as pd
from src.analysis import (
    filter_by_age_range,
    filter_by_gender,
    filter_by_hospital,
    summary_by_hospital,
    summary_by_medical_condition
)
from src.logging_setup import logger

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():
    logger.info("Visited index page")
    return render_template("index.html")

# -------------------
# Filtering routes
# -------------------
@main_bp.route("/filter/age", methods=["GET"])
def filter_age():
    min_age = int(request.args.get("min_age", 0))
    max_age = int(request.args.get("max_age", 120))
    logger.info(f"Filtering by age: {min_age}-{max_age}")
    df = filter_by_age_range(min_age, max_age)
    return df.to_html(classes="table table-striped", index=False)

@main_bp.route("/filter/gender", methods=["GET"])
def filter_gender():
    gender = request.args.get("gender", "Male")
    logger.info(f"Filtering by gender: {gender}")
    df = filter_by_gender(gender)
    return df.to_html(classes="table table-striped", index=False)

@main_bp.route("/filter/hospital", methods=["GET"])
def filter_hosp():
    hospital = request.args.get("hospital", "")
    if not hospital:
        return "<p>Please provide a hospital name</p>"
    df = filter_by_hospital(hospital)
    logger.info(f"Filtering by hospital: {hospital}")
    return df.to_html(classes="table table-striped", index=False)

# -------------------
# Summary routes
# -------------------
@main_bp.route("/summary/hospital")
def hospital_summary():
    logger.info("Getting summary by hospital")
    df = summary_by_hospital()
    return df.to_html(classes="table table-striped", index=False)

@main_bp.route("/summary/medical-condition")
def condition_summary():
    logger.info("Getting summary by medical condition")
    df = summary_by_medical_condition()
    return df.to_html(classes="table table-striped", index=False)
