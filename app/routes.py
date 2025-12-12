from flask import Blueprint, render_template, request
from src.analysis import filter_patients
from src.logging_setup import logger
import pandas as pd

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    """Render home page."""
    return render_template("index.html")


@main_bp.route("/filter", methods=["GET"])
def filter_page():
    """Render filter page."""
    return render_template("filter.html")

@main_bp.route("/filter", methods=["POST"])
def filter_process():
    try:
        data = request.get_json() or {}

        def clean(x):
            return x.strip() if isinstance(x, str) and x.strip() else None

        # Extract inputs
        min_age = clean(data.get("min_age"))
        max_age = clean(data.get("max_age"))
        gender = clean(data.get("gender"))
        hospital = clean(data.get("hospital"))
        condition = clean(data.get("condition"))
        doctor = clean(data.get("doctor"))
        ad_start = clean(data.get("ad_start"))
        ad_end = clean(data.get("ad_end"))
        bill_min = clean(data.get("bill_min"))
        bill_max = clean(data.get("bill_max"))

        # Pagination inputs
        page = int(data.get("page", 1))
        per_page = int(data.get("per_page", 50))  # default 50 rows per page
        offset = (page - 1) * per_page

        # --------------------
        # AGE VALIDATION
        # --------------------
        for age_val in [("min_age", min_age), ("max_age", max_age)]:
            if age_val[1]:
                val = int(age_val[1])
                if val < 0:
                    return "<div class='alert'>Age has to be positive.</div>"
                if val > 150:
                    return "<div class='alert'>Age has to be less than 150.</div>"
                if age_val[0] == "min_age":
                    min_age = val
                else:
                    max_age = val

        # --------------------
        # BILLING VALIDATION
        # --------------------
        for bill_val in [("bill_min", bill_min), ("bill_max", bill_max)]:
            if bill_val[1]:
                val = float(bill_val[1])
                if val < 0:
                    return "<div class='alert'>Billing amount cannot be negative.</div>"
                if bill_val[0] == "bill_min":
                    bill_min = val
                else:
                    bill_max = val

        # --------------------
        # FILTER DATA
        # --------------------
        df = filter_patients(
            min_age=min_age,
            max_age=max_age,
            gender=gender,
            hospital=hospital,
            condition=condition,
            doctor=doctor,
            ad_start=ad_start,
            ad_end=ad_end,
            bill_min=bill_min,
            bill_max=bill_max
        )

        if df.empty:
            return "<div class='alert'>No matching patients found.</div>"

        # Total pages
        total_rows = len(df)
        total_pages = (total_rows + per_page - 1) // per_page

        # Paginate
        df_page = df.iloc[offset:offset+per_page]

        # --------------------
        # FORMAT DATE COLUMNS
        # --------------------
        for date_col in ["DateOfAdmission", "DischargeDate"]:
            if date_col in df_page.columns:
                df_page[date_col] = pd.to_datetime(df_page[date_col], errors="coerce").dt.strftime("%Y-%m-%d")

        # --------------------
        # RENAME COLUMNS
        # --------------------
        col_map = {
            "Name": "Patient Name",
            "Age": "Patient Age",
            "Gender": "Sex",
            "BloodType": "Blood Type",
            "MedicalCondition": "Condition",
            "DateOfAdmission": "Admission Date",
            "DischargeDate": "Discharge Date",
            "Doctor": "Attending Doctor",
            "Hospital": "Hospital Name",
            "InsuranceProvider": "Insurance",
            "BillingAmount": "Bill Amount",
            "RoomNumber": "Room No",
            "AdmissionType": "Admission Type",
            "Medication": "Medication",
            "TestResults": "Test Results"
        }
        df_page.rename(columns=col_map, inplace=True)

        # --------------------
        # CONVERT TO HTML
        # --------------------
        table_html = df_page.to_html(classes="table table-striped", index=False)

        # Add pagination controls
        pagination_html = "<div style='margin-top:15px;'>"
        for p in range(1, total_pages + 1):
            if p == page:
                pagination_html += f"<strong>{p}</strong> "
            else:
                pagination_html += f"<a href='#' onclick='goToPage({p})'>{p}</a> "
        pagination_html += "</div>"

        return table_html + pagination_html

    except Exception as e:
        logger.exception("Filter process error")
        return "<div class='alert'>Error processing request.</div>"
