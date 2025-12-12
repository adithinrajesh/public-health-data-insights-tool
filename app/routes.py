from flask import Blueprint, render_template, request
from src.analysis import filter_patients
from src.logging_setup import logger
import pandas as pd
from flask import send_file
import matplotlib.pyplot as plt
import io
from src.cleaning import load_data_from_db, clean_data

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
    
@main_bp.route("/summary", methods=["GET"])
def summary_page():
    """Render the summary/analysis page."""
    return render_template("summary.html")
from src.cleaning import load_data_from_db, clean_data

from src.cleaning import load_data_from_db, clean_data

@main_bp.route("/summary", methods=["POST"])
def summary_process():
    try:
        data = request.get_json() or {}

        group_by = data.get("group_by")      # categorical column
        agg_column = data.get("column")      # numeric column (optional)
        agg_func = data.get("agg_func")      # mean, min, max, count, or None

        # Load and clean full dataset
        df = load_data_from_db()
        df = clean_data(df)

        # Convert empty strings or "none" to None
        if agg_func in [None, "", "none"]:
            agg_func = None
        if agg_column == "":
            agg_column = None
        if group_by == "":
            group_by = None

        # If nothing selected, return alert
        if not group_by and not agg_column:
            return "<div class='alert'>Please select an option above to display summary.</div>"

        # Grouping + optional aggregation
        if group_by:
            if agg_column and agg_func:  # Group + aggregation
                grouped = df.groupby(group_by)[agg_column]
                if agg_func == "mean":
                    result = grouped.mean().reset_index()
                elif agg_func == "min":
                    result = grouped.min().reset_index()
                elif agg_func == "max":
                    result = grouped.max().reset_index()
                elif agg_func == "count":
                    result = grouped.count().reset_index()
                else:
                    result = grouped.count().reset_index()
            else:  # Group only → count rows per group
                result = df.groupby(group_by).size().reset_index(name="Count")
        else:
            # No grouping, only aggregation
            if agg_column and agg_func:
                if agg_func == "mean":
                    result = pd.DataFrame({agg_column: [df[agg_column].mean()]})
                elif agg_func == "min":
                    result = pd.DataFrame({agg_column: [df[agg_column].min()]})
                elif agg_func == "max":
                    result = pd.DataFrame({agg_column: [df[agg_column].max()]})
                elif agg_func == "count":
                    result = pd.DataFrame({agg_column: [df[agg_column].count()]})
                else:
                    result = pd.DataFrame({agg_column: [df[agg_column].count()]})
            else:
                # Neither grouping nor aggregation → total rows
                result = pd.DataFrame({"Total Records": [len(df)]})

        # Pretty column names
        result.columns = [col.replace("_", " ").title() for col in result.columns]

        return result.to_html(classes="table table-striped", index=False)

    except Exception as e:
        logger.exception("Summary process error")
        return "<div class='alert'>Error processing summary request.</div>"
    
# -------------------------
# Visualization Routes
# -------------------------
from flask import Blueprint, render_template, request, send_file
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
from src.cleaning import load_data_from_db, clean_data

# ---------- Visualisation Pages ----------
@main_bp.route("/visualisation", methods=["GET"])
def visualisation_page():
    return render_template("visualisation.html")

# ---------- Curated Visualisations ----------
@main_bp.route("/visualisation/curated", methods=["POST"])
def curated_visualisation():
    try:
        data = request.get_json() or {}
        plot_name = data.get("plot_name")

        # Load and clean dataset
        df = load_data_from_db()
        df = clean_data(df)

        # Precompute derived columns
        df["LengthOfStay"] = (df["DischargeDate"] - df["DateOfAdmission"]).dt.days
        df["AgeGroup"] = pd.cut(df["Age"], bins=[0,18,35,50,65,150], labels=["0-18","19-35","36-50","51-65","65+"])

        plt.figure(figsize=(8,6))

        # ---------- Patient Demographics ----------
        if plot_name == "age_histogram":
            df["Age"].hist(bins=20, color="skyblue")
            plt.xlabel("Age")
            plt.ylabel("Count")
            plt.title("Histogram of Age Distribution")

        elif plot_name == "gender_pie":
            counts = df["Gender"].value_counts()
            counts.plot(kind="pie", autopct='%1.1f%%', colors=["skyblue","lightgreen"])
            plt.ylabel("")
            plt.title("Gender Breakdown")

        elif plot_name == "bloodtype_bar":
            counts = df["BloodType"].value_counts()
            counts.plot(kind="bar", color="skyblue")
            plt.xlabel("Blood Type")
            plt.ylabel("Count")
            plt.title("Blood Type Frequency")

        # ---------- Admissions & Hospitals ----------
        elif plot_name == "admission_type_bar":
            df["AdmissionType"].value_counts().plot(kind="bar", color="salmon")
            plt.xlabel("Admission Type")
            plt.ylabel("Count")
            plt.title("Admissions by Type")

        elif plot_name == "admissions_over_time":
            df.groupby("DateOfAdmission").size().plot(kind="line", color="purple")
            plt.xlabel("Date")
            plt.ylabel("Number of Admissions")
            plt.title("Admissions Over Time")

        elif plot_name == "hospital_bar":
            df["Hospital"].value_counts().plot(kind="bar", color="orange")
            plt.xlabel("Hospital")
            plt.ylabel("Patients")
            plt.title("Hospital Comparison")

        # ---------- Financial Insights ----------
        elif plot_name == "billing_histogram":
            df["BillingAmount"].hist(bins=20, color="green")
            plt.xlabel("Billing Amount")
            plt.ylabel("Count")
            plt.title("Billing Amount Distribution")

        elif plot_name == "billing_box_admission":
            sns.boxplot(x="AdmissionType", y="BillingAmount", data=df)
            plt.xlabel("Admission Type")
            plt.ylabel("Billing Amount")
            plt.title("Billing by Admission Type")

        elif plot_name == "billing_avg_insurance":
            df.groupby("InsuranceProvider")["BillingAmount"].mean().plot(kind="bar", color="lightblue")
            plt.xlabel("Insurance Provider")
            plt.ylabel("Average Billing")
            plt.title("Average Billing per Insurance Provider")

        # ---------- Medical & Treatment ----------
        elif plot_name == "condition_bar":
            df["MedicalCondition"].value_counts().plot(kind="barh", color="teal")
            plt.xlabel("Count")
            plt.ylabel("Medical Condition")
            plt.title("Medical Condition Frequency")

        elif plot_name == "medication_bar":
            df["Medication"].value_counts().plot(kind="bar", color="pink")
            plt.xlabel("Medication")
            plt.ylabel("Count")
            plt.title("Medication Usage")

        elif plot_name == "condition_test_results":
            df.groupby("MedicalCondition")["TestResults"].value_counts().unstack(fill_value=0).plot(
                kind="bar", stacked=True
            )
            plt.xlabel("Medical Condition")
            plt.ylabel("Count")
            plt.title("Condition vs Test Results")

        # ---------- Outcomes & Test Results ----------
        elif plot_name == "test_results_pie":
            df["TestResults"].value_counts().plot(kind="pie", autopct='%1.1f%%', colors=["skyblue","lightgreen","salmon"])
            plt.ylabel("")
            plt.title("Test Results Distribution")

        elif plot_name == "length_of_stay_hist":
            df["LengthOfStay"].hist(bins=20, color="purple")
            plt.xlabel("Days")
            plt.ylabel("Count")
            plt.title("Length of Stay Distribution")

        elif plot_name == "test_results_age_group":
            df.groupby("AgeGroup")["TestResults"].value_counts().unstack(fill_value=0).plot(kind="bar", stacked=True)
            plt.xlabel("Age Group")
            plt.ylabel("Count")
            plt.title("Test Results by Age Group")

        # ---------- Advanced/Multivariate ----------
        elif plot_name == "correlation_heatmap":
            numeric_df = df[["Age","BillingAmount","LengthOfStay"]].sample(min(len(df), 2000), random_state=42)
            sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm")
            plt.title("Correlation Heatmap")

        elif plot_name == "pairplot":
            numeric_df = df[["Age","BillingAmount","LengthOfStay","TestResults"]].sample(min(len(df), 2000), random_state=42)
            sns.pairplot(numeric_df, hue="TestResults")

        elif plot_name == "clustered_bar":
            df.groupby(["InsuranceProvider","AdmissionType","TestResults"]).size().unstack(fill_value=0).plot(kind="bar")
            plt.xlabel("Insurance Provider / Admission Type")
            plt.ylabel("Count")
            plt.title("Insurance × Admission × Test Results")

        else:
            return "<div class='alert'>Invalid curated plot name.</div>", 400

        # Convert plot to PNG
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close()

        return send_file(buf, mimetype="image/png")

    except Exception as e:
        logger.exception("Curated visualisation error")
        return "<div class='alert'>Error generating curated plot.</div>", 500
