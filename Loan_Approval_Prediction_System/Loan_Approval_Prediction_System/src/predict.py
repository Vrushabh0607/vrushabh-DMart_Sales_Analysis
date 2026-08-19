"""
predict.py
----------
Loads the trained model and preprocessing pipeline, then exposes a
predict_loan() function that accepts a single applicant's details and
returns the predicted Loan Status plus approval / rejection probability.

Run directly for a demo prediction:
    python predict.py
"""

import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")

MODEL_PATH = os.path.join(MODELS_DIR, "loan_approval_model.pkl")
PIPELINE_PATH = os.path.join(MODELS_DIR, "preprocessing_pipeline.pkl")

VALID_PROPERTY_AREAS = {"Urban", "Semiurban", "Rural"}
VALID_LOAN_TERMS = {120, 180, 240, 300, 360}

_model = None
_preprocessor = None


def _load_artifacts():
    """Lazily load model + pipeline once and cache them."""
    global _model, _preprocessor
    if _model is None or _preprocessor is None:
        if not os.path.exists(MODEL_PATH) or not os.path.exists(PIPELINE_PATH):
            raise FileNotFoundError(
                "Model or preprocessing pipeline not found. "
                "Run train_model.py first to generate models/loan_approval_model.pkl "
                "and models/preprocessing_pipeline.pkl."
            )
        _model = joblib.load(MODEL_PATH)
        _preprocessor = joblib.load(PIPELINE_PATH)
    return _model, _preprocessor


def validate_input(
    applicant_income,
    coapplicant_income,
    loan_amount,
    loan_term,
    credit_score,
    employment_years,
    debt_to_income_ratio,
    property_area,
):
    errors = []

    if applicant_income is None or applicant_income < 0:
        errors.append("Applicant_Income must be >= 0.")
    if coapplicant_income is None or coapplicant_income < 0:
        errors.append("Coapplicant_Income must be >= 0.")
    if loan_amount is None or loan_amount < 0:
        errors.append("Loan_Amount must be >= 0.")
    if loan_term not in VALID_LOAN_TERMS:
        errors.append(f"Loan_Term must be one of {sorted(VALID_LOAN_TERMS)}.")
    if credit_score is None or not (300 <= credit_score <= 850):
        errors.append("Credit_Score must be between 300 and 850.")
    if employment_years is None or not (0 <= employment_years <= 35):
        errors.append("Employment_Years must be between 0 and 35.")
    if debt_to_income_ratio is None or not (0 <= debt_to_income_ratio <= 1):
        errors.append("Debt_to_Income_Ratio must be between 0 and 1.")
    if property_area not in VALID_PROPERTY_AREAS:
        errors.append(f"Property_Area must be one of {sorted(VALID_PROPERTY_AREAS)}.")

    return errors


def predict_loan(
    applicant_income: float,
    coapplicant_income: float,
    loan_amount: float,
    loan_term: int,
    credit_score: int,
    employment_years: int,
    debt_to_income_ratio: float,
    property_area: str,
) -> dict:
    """
    Predict loan approval status for a single applicant.

    Returns a dict:
        {
            "Loan_Status": "Approved" | "Rejected",
            "Approval_Probability": float (0-100, 2 decimals),
            "Rejection_Probability": float (0-100, 2 decimals),
        }
    """
    errors = validate_input(
        applicant_income, coapplicant_income, loan_amount, loan_term,
        credit_score, employment_years, debt_to_income_ratio, property_area,
    )
    if errors:
        raise ValueError("Invalid input: " + " ".join(errors))

    model, preprocessor = _load_artifacts()

    input_df = pd.DataFrame([{
        "Applicant_Income": applicant_income,
        "Coapplicant_Income": coapplicant_income,
        "Loan_Amount": loan_amount,
        "Loan_Term": loan_term,
        "Credit_Score": credit_score,
        "Employment_Years": employment_years,
        "Debt_to_Income_Ratio": debt_to_income_ratio,
        "Property_Area": property_area,
    }])

    input_transformed = preprocessor.transform(input_df)

    predicted_label = model.predict(input_transformed)[0]
    probabilities = model.predict_proba(input_transformed)[0]

    classes = list(model.classes_)
    approval_idx = classes.index("Approved")
    rejection_idx = classes.index("Rejected")

    approval_prob = round(float(probabilities[approval_idx]) * 100, 2)
    rejection_prob = round(float(probabilities[rejection_idx]) * 100, 2)

    return {
        "Loan_Status": predicted_label,
        "Approval_Probability": approval_prob,
        "Rejection_Probability": rejection_prob,
    }


if __name__ == "__main__":
    # Demo prediction with a realistic sample applicant
    result = predict_loan(
        applicant_income=85000,
        coapplicant_income=25000,
        loan_amount=1200000,
        loan_term=240,
        credit_score=740,
        employment_years=8,
        debt_to_income_ratio=0.28,
        property_area="Semiurban",
    )
    print("Loan Status:", result["Loan_Status"])
    print(f"Approval Probability: {result['Approval_Probability']}%")
    print(f"Rejection Probability: {result['Rejection_Probability']}%")
