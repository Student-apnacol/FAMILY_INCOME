# Financial Scoring Model

This application calculates financial scores for families based on various parameters, providing actionable insights to improve financial health.

---

## Process Overview

1. **Data Preparation**
   - Load family financial data from `family_financial_and_transactions_data.csv`.
   - Group transactions by family and member, aggregating amounts and categorizing expenses.

2. **Feature Engineering**
   - Calculate key metrics such as:
     - Savings-to-Income Ratio
     - Monthly Expenses Percentage
     - Loan Payments Percentage
     - Spending Distribution
     - Financial Goals Met Ratio
   - Compute the final financial score using weighted metrics.

3. **Web Application**
   - A user-friendly interface built with HTML, CSS, and JavaScript.
   - Users input financial details such as income, savings, and expenses.
   - The backend Flask API calculates the score and returns insights.

4. **Insights**
   - Highlights areas like:
     - Savings adequacy
     - Expense management
     - Loan repayment impact
   - Presented in an organized, actionable format.

---

## Installation and Usage

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/financial-scoring-model.git
   cd financial-scoring-model
