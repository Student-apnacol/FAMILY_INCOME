import streamlit as st
import pandas as pd
import pickle
import numpy as np
from datetime import datetime
import os
from xgboost import XGBRegressor

# Define file paths relative to the current working directory (the folder where the script is located)
model_path = os.path.join(os.getcwd(), 'xgb_model.pkl')
preprocessor_path = os.path.join(os.getcwd(), 'preprocessor.pkl')
data_path = os.path.join(os.getcwd(), 'family_financial_and_transactions_data.csv')

# Ensure files exist
if not os.path.exists(model_path):
    st.error(f"Model file not found at {model_path}. Please upload the correct file.")
    st.stop()  # Stop the script if the file is not found

if not os.path.exists(preprocessor_path):
    st.error(f"Preprocessor file not found at {preprocessor_path}. Please upload the correct file.")
    st.stop()  # Stop the script if the file is not found

if not os.path.exists(data_path):
    st.error(f"Data file not found at {data_path}. Please upload the correct file.")
    st.stop()  # Stop the script if the file is not found

# Load the trained model and preprocessor
with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)

with open(preprocessor_path, 'rb') as preprocessor_file:
    preprocessor = pickle.load(preprocessor_file)

# Load the dataset (CSV)
df_train = pd.read_csv(data_path)

# Function to predict Monthly Expenses
def predict_expenses(input_data):
    # Preprocess the input data
    input_df = pd.DataFrame([input_data])
    processed_data = preprocessor.transform(input_df)
    
    # Make prediction using the trained model
    prediction = model.predict(processed_data)
    
    return prediction[0]

# Streamlit app UI
st.set_page_config(page_title="Monthly Expenses Prediction", page_icon="💸")
st.title('Monthly Expenses Prediction 💰')
st.markdown("""
    This app predicts **Monthly Expenses** based on the provided financial details.
    Enter the data below to get the prediction.
""")

# Create sections for each input field for better organization
st.sidebar.header("Input Details")

# Sidebar inputs for user details
category = st.sidebar.selectbox('Category', df_train['Category'].unique())
amount = st.sidebar.number_input('Amount Spent', min_value=0.0, format="%.2f")
income = st.sidebar.number_input('Income', min_value=0)
savings = st.sidebar.number_input('Savings', min_value=0)
loan_payments = st.sidebar.number_input('Loan Payments', min_value=0)
credit_card_spending = st.sidebar.number_input('Credit Card Spending', min_value=0)
dependents = st.sidebar.number_input('Dependents', min_value=0)
financial_goals_met = st.sidebar.slider('Financial Goals Met (%)', min_value=0, max_value=100, step=1)

# Display the input details entered by the user
st.write("### Input Details")
st.write(f"**Category**: {category}")
st.write(f"**Amount Spent**: ₹{amount:,.2f}")
st.write(f"**Income**: ₹{income:,.2f}")
st.write(f"**Savings**: ₹{savings:,.2f}")
st.write(f"**Loan Payments**: ₹{loan_payments:,.2f}")
st.write(f"**Credit Card Spending**: ₹{credit_card_spending:,.2f}")
st.write(f"**Dependents**: {dependents}")
st.write(f"**Financial Goals Met**: {financial_goals_met}%")

# Button to trigger prediction
if st.sidebar.button('Predict Monthly Expenses'):
    input_data = {
        'Category': category,
        'Amount': amount,
        'Income': income,
        'Savings': savings,
        'Loan Payments': loan_payments,
        'Credit Card Spending': credit_card_spending,
        'Dependents': dependents,
        'Financial Goals Met (%)': financial_goals_met
    }
    
    prediction = predict_expenses(input_data)
    
    # Display the predicted monthly expenses
    st.write("### Predicted Monthly Expenses")
    st.write(f"The predicted Monthly Expenses are: ₹{prediction:,.2f}")

# Footer
st.markdown("""
    ---
    Made with ❤️ by **devansh**
    """)
