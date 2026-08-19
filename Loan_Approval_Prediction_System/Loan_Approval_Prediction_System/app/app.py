"""
app.py
------
Flask web application for the Loan Approval Prediction System.

Run directly:
    python app.py
Then open http://127.0.0.1:5000 in a browser.
"""

import os
import sys

# Make src/ importable regardless of the current working directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from flask import Flask, render_template, request, jsonify
from predict import predict_loan, VALID_PROPERTY_AREAS, VALID_LOAN_TERMS

app = Flask(__name__)


@app.route("/")
def index():
    return render_template(
        "index.html",
        loan_terms=sorted(VALID_LOAN_TERMS),
        property_areas=sorted(VALID_PROPERTY_AREAS),
    )


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)

        applicant_income = float(data.get("applicant_income"))
        coapplicant_income = float(data.get("coapplicant_income"))
        loan_amount = float(data.get("loan_amount"))
        loan_term = int(data.get("loan_term"))
        credit_score = int(data.get("credit_score"))
        employment_years = int(data.get("employment_years"))
        debt_to_income_ratio = float(data.get("debt_to_income_ratio"))
        property_area = data.get("property_area")

        result = predict_loan(
            applicant_income=applicant_income,
            coapplicant_income=coapplicant_income,
            loan_amount=loan_amount,
            loan_term=loan_term,
            credit_score=credit_score,
            employment_years=employment_years,
            debt_to_income_ratio=debt_to_income_ratio,
            property_area=property_area,
        )
        return jsonify({"success": True, **result})

    except ValueError as ve:
        return jsonify({"success": False, "error": str(ve)}), 400
    except Exception as exc:  # noqa: BLE001
        return jsonify({"success": False, "error": f"Unexpected error: {exc}"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
