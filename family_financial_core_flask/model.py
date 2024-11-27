import pandas as pd

def load_and_prepare_data(file_path):
    # Load CSV
    df = pd.read_csv(file_path)

    # Group transactions and aggregate
    df_new = df.groupby(
        ['Family ID', 'Member ID', 'Category', 'Income', 'Savings',
         'Monthly Expenses', 'Loan Payments', 'Credit Card Spending',
         'Dependents', 'Financial Goals Met (%)']
    )['Amount'].sum().reset_index()

    # Aggregate data to family level
    family_data = df_new.groupby("Family ID").agg(
        Income=("Income", "first"),
        Savings=("Savings", "first"),
        Monthly_Expenses=("Monthly Expenses", "first"),
        Loan_Payments=("Loan Payments", "first"),
        Credit_Card_Spending=("Credit Card Spending", "sum"),
        Financial_Goals_Met=("Financial Goals Met (%)", "first"),
        Total_Spending=("Amount", "sum"),
        Non_essential_Spending=("Amount", lambda x: x[df.loc[x.index, "Category"].isin(["Travel", "Entertainment"])].sum())
    ).reset_index()

    return family_data

def calculate_scores(family_data):
    # Calculate financial metrics
    family_data["Savings_to_Income_Ratio"] = family_data["Savings"] / family_data["Income"]
    family_data["Monthly_Expenses_Percentage"] = family_data["Monthly_Expenses"] / family_data["Income"]
    family_data["Loan_Payments_Percentage"] = family_data["Loan_Payments"] / family_data["Income"]
    family_data["Spending_Category_Distribution"] = family_data["Non_essential_Spending"] / family_data["Total_Spending"]
    family_data["Financial_Goals_Met_Ratio"] = family_data["Financial_Goals_Met"] / 100

    # Define weights
    weights = {
        "Savings_to_Income_Ratio": 0.25,
        "Monthly_Expenses_Percentage": 0.2,
        "Loan_Payments_Percentage": 0.15,
        "Credit_Card_Spending": 0.15,
        "Spending_Category_Distribution": 0.1,
        "Financial_Goals_Met_Ratio": 0.15,
    }

    # Calculate financial scores
    family_data["Score"] = (
        weights["Savings_to_Income_Ratio"] * family_data["Savings_to_Income_Ratio"] +
        weights["Monthly_Expenses_Percentage"] * (1 - family_data["Monthly_Expenses_Percentage"]) +
        weights["Loan_Payments_Percentage"] * (1 - family_data["Loan_Payments_Percentage"]) +
        weights["Credit_Card_Spending"] * (1 - family_data["Credit_Card_Spending"] / family_data["Income"]) +
        weights["Spending_Category_Distribution"] * (1 - family_data["Spending_Category_Distribution"]) +
        weights["Financial_Goals_Met_Ratio"] * family_data["Financial_Goals_Met_Ratio"]
    ) * 100

    return family_data

def generate_insights(row):
    insights = []
    if row["Savings_to_Income_Ratio"] < 0.3:
        insights.append("Savings are below recommended levels.")
    if row["Monthly_Expenses_Percentage"] > 0.5:
        insights.append("Monthly expenses are high relative to income.")
    if row["Loan_Payments_Percentage"] > 0.2:
        insights.append("Loan payments are taking up a significant portion of income.")
    return insights
