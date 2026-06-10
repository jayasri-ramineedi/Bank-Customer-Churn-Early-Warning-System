import streamlit as st
import requests
import json

st.title("🏦 Bank Customer Churn Prediction System")
st.write("Enter customer details to predict churn probability")

# Input form
credit_score = st.number_input("Credit Score", 300, 900, 600)
country = st.selectbox("Country", ["France", "Germany", "Spain"])
gender = st.selectbox("Gender", ["Male", "Female"])
age = st.number_input("Age", 18, 100, 40)
tenure = st.number_input("Tenure (Years)", 0, 10, 5)
balance = st.number_input("Balance", 0.0, 250000.0, 50000.0)
products_number = st.number_input("Products Number", 1, 4, 2)
credit_card = st.selectbox("Credit Card (1=Yes, 0=No)", [0, 1])
active_member = st.selectbox("Active Member (1=Yes, 0=No)", [0, 1])
estimated_salary = st.number_input("Estimated Salary", 0.0, 200000.0, 70000.0)

# Button
if st.button("Predict Churn"):

    url = "http://127.0.0.1:8000/evaluate-churn"

    payload = {
        "credit_score": credit_score,
        "country": country,
        "gender": gender,
        "age": age,
        "tenure": tenure,
        "balance": balance,
        "products_number": products_number,
        "credit_card": credit_card,
        "active_member": active_member,
        "estimated_salary": estimated_salary
    }

    response = requests.post(url, json=payload)

    result = response.json()

    st.subheader("Prediction Result")

    if result["prediction"] == 1:
        st.error("⚠ High Risk: Customer will leave the bank")
    else:
        st.success("✅ Low Risk: Customer will stay")

    st.write("Churn Probability:", result["churn_probability"], "%")