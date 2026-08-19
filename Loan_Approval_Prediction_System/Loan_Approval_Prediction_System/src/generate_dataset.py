"""
generate_dataset.py
--------------------
Generates a realistic synthetic dataset for the Loan Approval Prediction
System and saves it to ../dataset/loan_approval_dataset.csv (relative to
this file, so it works regardless of the current working directory).

Run directly:
    python generate_dataset.py
"""

import os
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------
# Portable path handling (works from src/, project root, any IDE, etc.)
# ---------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
os.makedirs(DATASET_DIR, exist_ok=True)
OUTPUT_PATH = os.path.join(DATASET_DIR, "loan_approval_dataset.csv")


def generate_dataset(n_rows: int = 1000, random_state: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)

    property_areas = rng.choice(
        ["Urban", "Semiurban", "Rural"], size=n_rows, p=[0.40, 0.35, 0.25]
    )

    # Employment years (right-skewed: most applicants have shorter tenure)
    employment_years = rng.exponential(scale=6, size=n_rows).astype(int)
    employment_years = np.clip(employment_years, 0, 35)

    # Applicant income, mildly boosted by employment tenure
    base_income = rng.gamma(shape=3.0, scale=15000, size=n_rows) + 15000
    income_boost = employment_years * rng.uniform(300, 900, size=n_rows)
    applicant_income = (base_income + income_boost).astype(int)
    applicant_income = np.clip(applicant_income, 15000, 250000)

    # Coapplicant income - ~55% of applications have a coapplicant
    has_coapplicant = rng.random(n_rows) < 0.55
    coapplicant_income = np.where(
        has_coapplicant,
        rng.gamma(shape=2.0, scale=12000, size=n_rows).astype(int),
        0,
    )
    coapplicant_income = np.clip(coapplicant_income, 0, 150000)

    total_income = applicant_income + coapplicant_income

    # Loan amount scaled to total income, with variance
    loan_amount = (total_income * rng.uniform(6, 30, size=n_rows)).astype(int)
    loan_amount = np.clip(loan_amount, 50000, 5000000)

    # Loan term (months)
    loan_term = rng.choice(
        [120, 180, 240, 300, 360], size=n_rows, p=[0.10, 0.15, 0.20, 0.25, 0.30]
    )

    # Credit score - nudged by employment tenure and income for realism
    credit_score_base = rng.normal(650, 90, size=n_rows)
    credit_score_base += (employment_years - 10) * 1.5
    credit_score_base += (applicant_income - 80000) / 2000
    credit_score = np.clip(credit_score_base, 300, 850).astype(int)

    # Debt-to-income ratio - tied to loan burden relative to income
    dti_base = (loan_amount / loan_term) / (total_income + 1) * 3
    dti_noise = rng.normal(0, 0.08, size=n_rows)
    debt_to_income_ratio = dti_base + dti_noise + rng.uniform(0.05, 0.25, size=n_rows)
    debt_to_income_ratio = np.clip(debt_to_income_ratio, 0.05, 0.80)
    debt_to_income_ratio = np.round(debt_to_income_ratio, 2)

    # ------------------------------------------------------------------
    # Approval probability - logistic function of key realistic drivers
    # ------------------------------------------------------------------
    area_effect = np.where(
        property_areas == "Semiurban", 0.35,
        np.where(property_areas == "Urban", 0.05, -0.15),
    )

    z = (
        0.012 * (credit_score - 600)
        + 0.000009 * (applicant_income - 60000)
        + 0.000006 * coapplicant_income
        - 0.0000015 * (loan_amount - 500000)
        + 0.10 * (employment_years - 5)
        - 4.2 * (debt_to_income_ratio - 0.35)
        + area_effect
    )

    # Random noise keeps the target from being perfectly separable
    z += rng.normal(0, 1.0, size=n_rows)

    prob_approved = 1 / (1 + np.exp(-z))

    # Calibrate threshold so ~70% of applications are approved
    target_approval_rate = 0.70
    threshold_prob = np.quantile(prob_approved, 1 - target_approval_rate)
    loan_status = np.where(prob_approved >= threshold_prob, "Approved", "Rejected")

    df = pd.DataFrame(
        {
            "Applicant_Income": applicant_income,
            "Coapplicant_Income": coapplicant_income,
            "Loan_Amount": loan_amount,
            "Loan_Term": loan_term,
            "Credit_Score": credit_score,
            "Employment_Years": employment_years,
            "Debt_to_Income_Ratio": debt_to_income_ratio,
            "Property_Area": property_areas,
            "Loan_Status": loan_status,
        }
    )

    # Remove any accidental exact duplicate rows by nudging income slightly
    dup_mask = df.duplicated()
    guard = 0
    while dup_mask.sum() > 0 and guard < 20:
        idx = df[dup_mask].index
        for i in idx:
            df.loc[i, "Applicant_Income"] += int(rng.integers(1, 50))
        dup_mask = df.duplicated()
        guard += 1

    return df


if __name__ == "__main__":
    dataset = generate_dataset()
    dataset.to_csv(OUTPUT_PATH, index=False)

    print(f"Dataset saved to: {OUTPUT_PATH}")
    print(f"Shape: {dataset.shape}")
    print("Loan_Status distribution:")
    print(dataset["Loan_Status"].value_counts(normalize=True).round(3))
    print("Duplicate rows:", dataset.duplicated().sum())
    print("Missing values:", dataset.isnull().sum().sum())
