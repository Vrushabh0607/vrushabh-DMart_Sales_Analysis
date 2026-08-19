"""
evaluate_model.py
------------------
Loads the saved best model + preprocessing pipeline, re-evaluates it on
the held-out test set (using the SAME random_state split as training),
and saves:
    - results/confusion_matrix.png
    - results/feature_importance.png (only if the model supports it)

Run directly:
    python evaluate_model.py
"""

import os
import joblib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import confusion_matrix, classification_report

from data_preprocessing import load_and_split_data, NUMERIC_FEATURES, CATEGORICAL_FEATURES

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

MODEL_PATH = os.path.join(MODELS_DIR, "loan_approval_model.pkl")
PIPELINE_PATH = os.path.join(MODELS_DIR, "preprocessing_pipeline.pkl")
BEST_MODEL_NAME_PATH = os.path.join(MODELS_DIR, "best_model_name.txt")

POSITIVE_LABEL = "Approved"
LABELS = ["Rejected", "Approved"]


def get_feature_names(preprocessor):
    """Reconstruct readable feature names after ColumnTransformer encoding."""
    cat_encoder = preprocessor.named_transformers_["cat"]
    cat_names = list(cat_encoder.get_feature_names_out(CATEGORICAL_FEATURES))
    return NUMERIC_FEATURES + cat_names


def plot_confusion_matrix(y_test, y_pred):
    cm = confusion_matrix(y_test, y_pred, labels=LABELS)
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues",
        xticklabels=LABELS, yticklabels=LABELS, ax=ax,
    )
    ax.set_xlabel("Predicted Label")
    ax.set_ylabel("True Label")
    ax.set_title("Confusion Matrix - Best Model")
    path = os.path.join(RESULTS_DIR, "confusion_matrix.png")
    fig.savefig(path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {path}")


def plot_feature_importance(model, feature_names):
    importances = None
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    elif hasattr(model, "coef_"):
        importances = np.abs(model.coef_[0])

    if importances is None:
        print("Selected model does not expose feature importances/coefficients; skipping plot.")
        return

    order = np.argsort(importances)[::-1]
    sorted_features = np.array(feature_names)[order]
    sorted_importances = importances[order]

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=sorted_importances, y=sorted_features, hue=sorted_features,
                palette="viridis", ax=ax, legend=False)
    ax.set_title("Feature Importance - Best Model")
    ax.set_xlabel("Importance")
    path = os.path.join(RESULTS_DIR, "feature_importance.png")
    fig.savefig(path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {path}")


def main():
    _, X_test, _, y_test = load_and_split_data()

    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PIPELINE_PATH)

    if os.path.exists(BEST_MODEL_NAME_PATH):
        with open(BEST_MODEL_NAME_PATH) as f:
            print(f"Evaluating best model: {f.read().strip()}")

    X_test_transformed = preprocessor.transform(X_test)
    y_pred = model.predict(X_test_transformed)

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, labels=LABELS))

    plot_confusion_matrix(y_test, y_pred)

    feature_names = get_feature_names(preprocessor)
    plot_feature_importance(model, feature_names)


if __name__ == "__main__":
    main()
