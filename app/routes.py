# app/routes.py
from flask import Blueprint, render_template, request
import pandas as pd
from src.analysis import (
    filter_by_age_range,
    summary_by_hospital
)
from src.logging_setup import logger

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():
    logger.info("Visited index page")
    return render_template("index.html")

@main_bp.route("/filter/age")
def filter_age():
    min_age = int(request.args.get("min_age", 0))
    max_age = int(request.args.get("max_age", 120))

    logger.info(f"Filtering age range {min_age}-{max_age}")

    df = filter_by_age_range(min_age, max_age)

    # MUST return HTML table for tests
    if df.empty:
        return "<p>No results found.</p>"

    return df.to_html(index=False)

@main_bp.route("/summary/hospital")
def hospital_summary():
    logger.info("Generating summary by hospital")

    df = summary_by_hospital()

    if df.empty:
        return "<p>No hospital summary available.</p>"

    return df.to_html(index=False)
