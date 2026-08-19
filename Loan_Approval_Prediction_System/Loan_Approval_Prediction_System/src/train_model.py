"""
train_model.py
---------------
Trains four classification models (Logistic Regression, Decision Tree,
Random Forest, K-Nearest Neighbors) on the loan approval dataset, evaluates
each with multiple metrics, saves a model comparison table, and persists
the best model + fitted preprocessing pipeline to disk.

Run directly:
    python train_model.py
"""

import os
import joblib
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)

from data_preprocessing import (
    load_and_split_data,
    build_preprocessing_pipeline,
    RANDOM_STATE,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODELS_DIR, "loan_approval_model.pkl")
PIPELINE_PATH = os.path.join(MODELS_DIR, "preprocessing_pipeline.pkl")
COMPARISON_PATH = os.path.join(RESULTS_DIR, "model_comparison.csv")

POSITIVE_LABEL = "Approved"


def get_models():
    return {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
        "Decision Tree": DecisionTreeClassifier(max_depth=6, random_state=RANDOM_STATE),
        "Random Forest": RandomForestClassifier(
            n_estimators=300, max_depth=8, random_state=RANDOM_STATE
        ),
        "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=9),
    }


def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, list(model.classes_).index(POSITIVE_LABEL)]

    return {
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred, pos_label=POSITIVE_LABEL),
        "Recall": recall_score(y_test, y_pred, pos_label=POSITIVE_LABEL),
        "F1_Score": f1_score(y_test, y_pred, pos_label=POSITIVE_LABEL),
        "ROC_AUC": roc_auc_score((y_test == POSITIVE_LABEL).astype(int), y_proba),
    }


def select_best_model(results_df: pd.DataFrame) -> str:
    """
    Select the best model using a balanced view of F1 Score and ROC-AUC
    rather than accuracy alone. Accuracy can be misleading on an
    imbalanced target (70/30 here), so F1 (balances precision & recall on
    the Approved class) and ROC-AUC (ranking quality across thresholds)
    are combined into a single composite score.
    """
    composite = 0.5 * results_df["F1_Score"] + 0.5 * results_df["ROC_AUC"]
    best_name = composite.idxmax()
    return best_name


def main():
    X_train, X_test, y_train, y_test = load_and_split_data()

    preprocessor = build_preprocessing_pipeline()
    X_train_transformed = preprocessor.fit_transform(X_train)
    X_test_transformed = preprocessor.transform(X_test)

    models = get_models()
    results = {}
    fitted_models = {}

    for name, model in models.items():
        model.fit(X_train_transformed, y_train)
        metrics = evaluate_model(model, X_test_transformed, y_test)
        results[name] = metrics
        fitted_models[name] = model
        print(f"{name}: {metrics}")

    results_df = pd.DataFrame(results).T
    results_df.index.name = "Model"
    results_df = results_df.round(4)
    results_df.to_csv(COMPARISON_PATH)
    print(f"\nModel comparison saved to: {COMPARISON_PATH}")
    print(results_df)

    best_model_name = select_best_model(results_df)
    best_model = fitted_models[best_model_name]
    print(f"\nBest model selected: {best_model_name}")

    joblib.dump(best_model, MODEL_PATH)
    joblib.dump(preprocessor, PIPELINE_PATH)
    print(f"Saved best model to: {MODEL_PATH}")
    print(f"Saved preprocessing pipeline to: {PIPELINE_PATH}")

    # Save the best model's name so evaluate_model.py / predict.py can
    # report it without re-running the whole comparison.
    with open(os.path.join(MODELS_DIR, "best_model_name.txt"), "w") as f:
        f.write(best_model_name)


if __name__ == "__main__":
    main()
