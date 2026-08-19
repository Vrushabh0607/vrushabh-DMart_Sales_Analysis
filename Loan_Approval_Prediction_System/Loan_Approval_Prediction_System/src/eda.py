"""
eda.py
------
Performs exploratory data analysis on the loan approval dataset and saves
all visualizations to ../results/eda/ (relative to this file).

Run directly:
    python eda.py
"""

import os
import matplotlib
matplotlib.use("Agg")  # headless-safe backend
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from data_preprocessing import load_data, NUMERIC_FEATURES

sns.set_style("whitegrid")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDA_DIR = os.path.join(BASE_DIR, "results", "eda")
os.makedirs(EDA_DIR, exist_ok=True)


def save_fig(fig, filename):
    path = os.path.join(EDA_DIR, filename)
    fig.savefig(path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {path}")


def plot_loan_status_distribution(df):
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.countplot(data=df, x="Loan_Status", hue="Loan_Status",
                  palette="Set2", ax=ax, legend=False)
    ax.set_title("Loan Status Distribution")
    ax.set_xlabel("Loan Status")
    ax.set_ylabel("Count")
    save_fig(fig, "01_loan_status_distribution.png")


def plot_credit_score_distribution(df):
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.histplot(df["Credit_Score"], bins=30, kde=True, color="steelblue", ax=ax)
    ax.set_title("Credit Score Distribution")
    save_fig(fig, "02_credit_score_distribution.png")


def plot_credit_score_vs_status(df):
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.boxplot(data=df, x="Loan_Status", y="Credit_Score",
                hue="Loan_Status", palette="Set2", ax=ax, legend=False)
    ax.set_title("Credit Score vs Loan Status")
    save_fig(fig, "03_credit_score_vs_loan_status.png")


def plot_applicant_income_distribution(df):
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.histplot(df["Applicant_Income"], bins=30, kde=True, color="darkorange", ax=ax)
    ax.set_title("Applicant Income Distribution")
    save_fig(fig, "04_applicant_income_distribution.png")


def plot_applicant_income_vs_status(df):
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.boxplot(data=df, x="Loan_Status", y="Applicant_Income",
                hue="Loan_Status", palette="Set2", ax=ax, legend=False)
    ax.set_title("Applicant Income vs Loan Status")
    save_fig(fig, "05_applicant_income_vs_loan_status.png")


def plot_loan_amount_distribution(df):
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.histplot(df["Loan_Amount"], bins=30, kde=True, color="seagreen", ax=ax)
    ax.set_title("Loan Amount Distribution")
    save_fig(fig, "06_loan_amount_distribution.png")


def plot_loan_amount_vs_status(df):
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.boxplot(data=df, x="Loan_Status", y="Loan_Amount",
                hue="Loan_Status", palette="Set2", ax=ax, legend=False)
    ax.set_title("Loan Amount vs Loan Status")
    save_fig(fig, "07_loan_amount_vs_loan_status.png")


def plot_dti_distribution(df):
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.histplot(df["Debt_to_Income_Ratio"], bins=30, kde=True, color="indianred", ax=ax)
    ax.set_title("Debt-to-Income Ratio Distribution")
    save_fig(fig, "08_debt_to_income_ratio_distribution.png")


def plot_dti_vs_status(df):
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.boxplot(data=df, x="Loan_Status", y="Debt_to_Income_Ratio",
                hue="Loan_Status", palette="Set2", ax=ax, legend=False)
    ax.set_title("Debt-to-Income Ratio vs Loan Status")
    save_fig(fig, "09_debt_to_income_ratio_vs_loan_status.png")


def plot_property_area_vs_status(df):
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.countplot(data=df, x="Property_Area", hue="Loan_Status", palette="Set2", ax=ax)
    ax.set_title("Property Area vs Loan Status")
    save_fig(fig, "10_property_area_vs_loan_status.png")


def plot_employment_years_vs_status(df):
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.boxplot(data=df, x="Loan_Status", y="Employment_Years",
                hue="Loan_Status", palette="Set2", ax=ax, legend=False)
    ax.set_title("Employment Years vs Loan Status")
    save_fig(fig, "11_employment_years_vs_loan_status.png")


def plot_correlation_heatmap(df):
    fig, ax = plt.subplots(figsize=(8, 6))
    corr_df = df[NUMERIC_FEATURES].copy()
    corr = corr_df.corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    ax.set_title("Correlation Heatmap (Numeric Features)")
    save_fig(fig, "12_correlation_heatmap.png")


def run_eda():
    df = load_data()
    plot_loan_status_distribution(df)
    plot_credit_score_distribution(df)
    plot_credit_score_vs_status(df)
    plot_applicant_income_distribution(df)
    plot_applicant_income_vs_status(df)
    plot_loan_amount_distribution(df)
    plot_loan_amount_vs_status(df)
    plot_dti_distribution(df)
    plot_dti_vs_status(df)
    plot_property_area_vs_status(df)
    plot_employment_years_vs_status(df)
    plot_correlation_heatmap(df)
    print("\nEDA complete. All visualizations saved to results/eda/")


if __name__ == "__main__":
    run_eda()
