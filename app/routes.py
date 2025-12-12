# app/routes.py
from flask import Blueprint, render_template, request
import pandas as pd
from src.analysis import filter_by_age_range, filter_by_gender, summary_by_hospital
from src.logging_setup import logger

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():
    logger.info("Visited index page")
    return render_template("index.html")

@main_bp.route("/filter/age", methods=["GET"])
def filter_age():
    min_age = int(request.args.get("min_age", 0))
    max_age = int(request.args.get("max_age", 120))
    logger.info(f"Filtering by age: {min_age}-{max_age}")
    df = filter_by_age_range(min_age, max_age)
    return df.to_html()

@main_bp.route("/summary/hospital")
def hospital_summary():
    logger.info("Getting summary by hospital")
    df = summary_by_hospital()
    return df.to_html()
