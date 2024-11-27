from flask import Flask, request, jsonify, render_template
from model import load_and_prepare_data, calculate_scores, generate_insights

app = Flask(__name__)

# Load and prepare the dataset
data_path = "data/family_financial_and_transactions_data.csv"
family_data = load_and_prepare_data(data_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate_score', methods=['POST'])
def calculate_score():
    try:
        # Parse JSON data from the request
        request_data = request.get_json()
        family_id = request_data.get("Family ID")
        income = request_data.get("income")
        savings = request_data.get("savings")
        monthly_expenses = request_data.get("monthly_expenses")
        loan_payments = request_data.get("loan_payments")
        credit_card_spending = request_data.get("credit_card_spending")
        total_spending = request_data.get("total_spending")
        financial_goals_met = request_data.get("financial_goals_met")

        # Validate input
        if not family_id:
            return jsonify({"error": "Family ID is required"}), 400

        # Check if Family ID exists in the dataset
        family_row = family_data[family_data["Family ID"] == family_id]
        if family_row.empty:
            return jsonify({"error": "Family ID not found in dataset"}), 404

        # Update the family_row with new inputs from the form
        family_row["Income"] = income
        family_row["Savings"] = savings
        family_row["Monthly_Expenses"] = monthly_expenses
        family_row["Loan_Payments"] = loan_payments
        family_row["Credit_Card_Spending"] = credit_card_spending
        family_row["Total_Spending"] = total_spending
        family_row["Financial_Goals_Met"] = financial_goals_met

        # Recalculate scores
        family_row = calculate_scores(family_row)
        insights = generate_insights(family_row.iloc[0])

        # Prepare and send response
        response = {
            "Family ID": family_id,
            "Score": round(family_row["Score"].iloc[0], 2),
            "Insights": insights
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
