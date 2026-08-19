"""
data_preprocessing.py
----------------------
Loads the loan dataset, inspects it, separates features/target, and builds
a Scikit-learn preprocessing pipeline (ColumnTransformer) that scales
numeric features and one-hot encodes categorical features.

All paths are relative to this file's location so the project stays
portable across machines and IDEs (VS Code, PyCharm, Anaconda, Spyder).
"""

import os
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split

# ---------------------------------------------------------------------
# Portable paths
# ---------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "loan_approval_dataset.csv")

TARGET_COLUMN = "Loan_Status"

NUMERIC_FEATURES = [
    "Applicant_Income",
    "Coapplicant_Income",
    "Loan_Amount",
    "Loan_Term",
    "Credit_Score",
    "Employment_Years",
    "Debt_to_Income_Ratio",
]
CATEGORICAL_FEATURES = ["Property_Area"]
RANDOM_STATE = 42


def load_data(path: str = DATASET_PATH) -> pd.DataFrame:
    """Load the raw dataset from disk."""
    df = pd.read_csv(path)
    return df


def inspect_data(df: pd.DataFrame) -> None:
    """Print a data-quality inspection summary."""
    print("=" * 60)
    print("DATA INSPECTION SUMMARY")
    print("=" * 60)
    print(f"Shape: {df.shape}")
    print("\nData types:")
    print(df.dtypes)
    print("\nMissing values per column:")
    print(df.isnull().sum())
    print(f"\nDuplicate rows: {df.duplicated().sum()}")
    print("\nDescriptive statistics (numeric columns):")
    print(df.describe().T)
    print("\nLoan_Status distribution:")
    print(df[TARGET_COLUMN].value_counts())
    print(df[TARGET_COLUMN].value_counts(normalize=True).round(3))
    print("\nProperty_Area distribution:")
    print(df["Property_Area"].value_counts())
    print("=" * 60)


def check_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """Return a summary of potential outliers using the IQR method."""
    summary = {}
    for col in NUMERIC_FEATURES:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        n_outliers = ((df[col] < lower) | (df[col] > upper)).sum()
        summary[col] = n_outliers
    return pd.DataFrame.from_dict(summary, orient="index", columns=["outlier_count"])


def get_features_and_target(df: pd.DataFrame):
    """Split dataframe into feature matrix X and target vector y."""
    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES].copy()
    y = df[TARGET_COLUMN].copy()
    return X, y


def build_preprocessing_pipeline() -> ColumnTransformer:
    """Build the ColumnTransformer used to preprocess features."""
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown="ignore", drop="first")

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, NUMERIC_FEATURES),
            ("cat", categorical_transformer, CATEGORICAL_FEATURES),
        ]
    )
    return preprocessor


def load_and_split_data(path: str = DATASET_PATH, test_size: float = 0.2):
    """
    Load data and perform an 80/20 train-test split (raw, unencoded).
    Using a fixed random_state guarantees the SAME split is reproduced
    by train_model.py, evaluate_model.py, and any other script.
    """
    df = load_data(path)
    X, y = get_features_and_target(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=RANDOM_STATE, stratify=y
    )
    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    data = load_data()
    inspect_data(data)
    print("\nOutlier summary (IQR method):")
    print(check_outliers(data))
