# Loan Approval Prediction System

A complete, end-to-end machine learning project that predicts whether a loan
application should be **Approved** or **Rejected**, based on the applicant's
financial and credit profile. Includes data generation, EDA, preprocessing,
model training/comparison, evaluation, a reusable prediction module, and a
Flask web application with a form-based interface.

---

## 1. Project Overview

Lenders must decide whether to approve or reject loan applications using a
mix of income, credit history, debt levels, and loan terms. This project
builds a classification model that learns these patterns from historical-style
applicant data and predicts the likely outcome for new applications, along
with a probability score for both outcomes.

## 2. Problem Statement

Given an applicant's income, coapplicant income, requested loan amount and
term, credit score, employment history, debt-to-income ratio, and property
area, predict whether the loan will be **Approved** or **Rejected**.

## 3. Objectives

- Generate a realistic synthetic dataset suitable for classification
- Perform thorough data cleaning, inspection, and exploratory analysis
- Build a reusable preprocessing pipeline (scaling + encoding)
- Train and compare multiple classification algorithms
- Select the best model using metrics appropriate for an imbalanced target
- Package the model behind a reusable prediction function
- Serve predictions through a Flask web application

## 4. Dataset Description

- **1,000** unique loan applications (rows)
- **9** columns, no index column
- No missing values, no duplicate rows
- Target distribution: **~70% Approved / ~30% Rejected**
- Generated synthetically with realistic statistical relationships between
  credit score, income, debt burden, employment history, and approval
  outcome (see `src/generate_dataset.py` for the exact generation logic)

## 5. Feature Description

| Column | Type | Description |
|---|---|---|
| `Applicant_Income` | int | Applicant's monthly income in INR (₹15,000–₹2,50,000) |
| `Coapplicant_Income` | int | Coapplicant's monthly income in INR, 0 if none (₹0–₹1,50,000) |
| `Loan_Amount` | int | Requested loan amount in INR (₹50,000–₹50,00,000) |
| `Loan_Term` | int | Repayment period in months (120 / 180 / 240 / 300 / 360) |
| `Credit_Score` | int | Applicant credit score (300–850) |
| `Employment_Years` | int | Years of employment (0–35) |
| `Debt_to_Income_Ratio` | float | Monthly debt obligations ÷ monthly income (0.05–0.80) |
| `Property_Area` | categorical | `Urban`, `Semiurban`, or `Rural` |
| `Loan_Status` | target | `Approved` or `Rejected` |

## 6. Data Preprocessing

Performed in `src/data_preprocessing.py`:

- Data loading from `dataset/loan_approval_dataset.csv`
- Inspection: shape, dtypes, missing values, duplicates, descriptive stats
- Outlier scan using the IQR method
- Feature / target separation
- `ColumnTransformer` pipeline:
  - `StandardScaler` on the 7 numeric features
  - `OneHotEncoder(drop='first')` on `Property_Area`
- Stratified 80/20 train-test split (`random_state=42`) so every script
  (training, evaluation, notebook) reproduces the exact same split

## 7. Exploratory Data Analysis

Performed in `src/eda.py`, with all 12 charts saved to `results/eda/`:

1. Loan Status distribution
2. Credit Score distribution
3. Credit Score vs Loan Status
4. Applicant Income distribution
5. Applicant Income vs Loan Status
6. Loan Amount distribution
7. Loan Amount vs Loan Status
8. Debt-to-Income Ratio distribution
9. Debt-to-Income Ratio vs Loan Status
10. Property Area vs Loan Status
11. Employment Years vs Loan Status
12. Correlation heatmap (numeric features)

## 8. Machine Learning Algorithms

Four classifiers are trained on the identical preprocessed train/test split
in `src/train_model.py`:

- Logistic Regression
- Decision Tree
- Random Forest
- K-Nearest Neighbors

## 9. Model Evaluation

Each model is scored on Accuracy, Precision, Recall, F1 Score, and ROC-AUC
(positive class = `Approved`). Results are saved to `results/model_comparison.csv`:

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|---|---|---|---|---|---|
| Logistic Regression | 0.850 | 0.877 | 0.914 | 0.895 | 0.910 |
| Decision Tree | 0.775 | 0.842 | 0.836 | 0.839 | 0.773 |
| Random Forest | 0.830 | 0.849 | 0.921 | 0.884 | 0.867 |
| K-Nearest Neighbors | 0.830 | 0.835 | 0.943 | 0.886 | 0.852 |

*(Your exact numbers may differ slightly if you regenerate the dataset with a
different random seed.)*

Additional evaluation artifacts saved to `results/`:
- `confusion_matrix.png` — confusion matrix for the best model
- `feature_importance.png` — feature importance / coefficient magnitude for
  the best model

## 10. Best Model

**Selected model: Logistic Regression**

The best model is **not** chosen by accuracy alone. `train_model.py` combines
**F1 Score** and **ROC-AUC** into a composite score (`0.5 × F1 + 0.5 × ROC-AUC`)
before picking a winner. This matters because the target is imbalanced
(~70/30). A model could reach high accuracy simply by leaning toward the
majority `Approved` class while doing a poor job separating genuinely risky
applicants — F1 checks that precision and recall on the `Approved` class are
both solid, and ROC-AUC checks that the model ranks applicants well across
*all* probability thresholds, not just the default 0.5 cutoff. Logistic
Regression scored highest on both, while also being simple, fast, and highly
interpretable — a practical advantage in lending, where regulators and
underwriters often need to explain *why* a decision was made.

## 11. Technologies Used

- Python 3.10+
- pandas, NumPy — data handling
- scikit-learn — preprocessing, modeling, evaluation
- matplotlib, seaborn — visualization
- Flask — web application
- joblib — model persistence
- Jupyter — exploratory notebook

## 12. Project Architecture

```
Raw Data Generation → Preprocessing Pipeline → Model Training (4 models)
        → Model Comparison & Selection → Saved Model + Pipeline (.pkl)
        → predict.py (reusable inference function)
        → Flask App (form UI → /predict endpoint → JSON result)
```

## 13. Project Folder Structure

```
Loan_Approval_Prediction_System/
│
├── dataset/
│   └── loan_approval_dataset.csv
│
├── notebooks/
│   └── loan_analysis.ipynb
│
├── src/
│   ├── generate_dataset.py
│   ├── data_preprocessing.py
│   ├── eda.py
│   ├── train_model.py
│   ├── evaluate_model.py
│   └── predict.py
│
├── models/
│   ├── loan_approval_model.pkl
│   ├── preprocessing_pipeline.pkl
│   └── best_model_name.txt
│
├── app/
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── style.css
│       └── script.js
│
├── results/
│   ├── model_comparison.csv
│   ├── confusion_matrix.png
│   ├── feature_importance.png
│   └── eda/
│       └── (12 PNG charts)
│
├── requirements.txt
├── README.md
└── .gitignore
```

## 14. Installation Instructions

From the project root:

```bash
pip install -r requirements.txt
```

(Optional but recommended) create a virtual environment first:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
pip install -r requirements.txt
```

## 15. How to Train the Model

All scripts use relative paths, so run them from inside `src/` (or adapt with
`python -m` from the project root):

```bash
cd src
python generate_dataset.py     # regenerate the synthetic dataset (optional — already included)
python eda.py                  # regenerate EDA charts into results/eda/
python train_model.py          # train all 4 models, save comparison + best model
python evaluate_model.py       # confusion matrix + feature importance for the best model
```

## 16. How to Run the Flask Application

```bash
cd app
python app.py
```

Then open the URL below in a browser.

## 17. How to Make Predictions

**Option A — Python function:**

```python
import sys
sys.path.append("src")
from predict import predict_loan

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
print(result)
# {'Loan_Status': 'Approved', 'Approval_Probability': 99.75, 'Rejection_Probability': 0.25}
```

**Option B — CLI demo:**

```bash
cd src
python predict.py
```

**Option C — Web form:** run the Flask app and submit the form (see above).

## 18. Results

- 1,000-row synthetic dataset with realistic, non-random relationships
  between credit score, income, debt burden, employment history, and
  approval outcome
- 4 classifiers trained and compared on an identical, reproducible 80/20 split
- Best model: **Logistic Regression** (Accuracy 0.850, F1 0.895, ROC-AUC 0.910)
- Fully working Flask web application with client + server-side validation
- All deliverables (dataset, notebook, scripts, models, plots, app) verified
  to run end-to-end without errors

## 19. Future Improvements

- Add hyperparameter tuning (GridSearchCV / RandomizedSearchCV) for each model
- Add cross-validation instead of a single train/test split
- Add SHAP-based explainability for individual predictions
- Add a database layer to store submitted applications and predictions
- Add authentication and role-based access for a real underwriting workflow
- Containerize the Flask app with Docker for deployment
- Replace the synthetic dataset with real, anonymized lending data (with
  appropriate fairness and bias audits before production use)

---

## Compatibility Notes

This project uses **relative paths** throughout (`os.path.dirname(__file__)`
based resolution), so the same folder works unmodified in VS Code, PyCharm,
Anaconda (Jupyter/Spyder), or plain terminal use — no hard-coded absolute
paths are used inside any Python file. The only fixed location is wherever
you place the `Loan_Approval_Prediction_System` folder itself.
