# app/routes.py
from flask import Blueprint, render_template, request
import pandas as pd
from src.analysis import filter_patients  # Combined filter function
from src.logging_setup import logger

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():
    logger.info("Visited index page")
    return render_template("index.html")

# ---------------------------
# Filter page (form)
# ---------------------------
@main_bp.route("/filter")
def filter_page():
    logger.info("Visited filter page")
    return render_template("filter.html")

# ---------------------------
# Filter results
# ---------------------------
@main_bp.route("/filter/results", methods=["GET"])
def filter_results():
    try:
        # Get filter parameters from GET request
        min_age = request.args.get("min_age", type=int)
        max_age = request.args.get("max_age", type=int)
        gender = request.args.get("gender")
        hospital = request.args.get("hospital")
        medical_condition = request.args.get("medical_condition")

        logger.info(f"Filters applied: min_age={min_age}, max_age={max_age}, gender={gender}, hospital={hospital}, condition={medical_condition}")

        # Apply combined filter function
        df = filter_patients(
            min_age=min_age,
            max_age=max_age,
            gender=gender if gender else None,
            hospitals=hospital if hospital else None,
            conditions=medical_condition if medical_condition else None
        )


        logger.info(f"Filtered {len(df)} patients")

        # Convert DataFrame to HTML
        table_html = df.to_html(classes="table table-striped table-bordered", index=False)

        return render_template("filter.html", table_html=table_html)

    except Exception as e:
        logger.error(f"Error in filter_results: {e}")
        return render_template("filter.html", table_html="<p>Error loading data</p>")
