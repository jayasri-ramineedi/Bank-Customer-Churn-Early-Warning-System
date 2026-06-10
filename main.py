import streamlit as st
import requests

# Page Config
st.set_page_config(
    page_title="Bank Customer Churn Prediction",
    page_icon="🏦",
    layout="centered"
)

# Title
st.title("🏦 Bank Customer Churn Prediction System")
st.write("Enter customer details to predict churn probability")

# Input Form
credit_score = st.number_input("Credit Score", 300, 900, 600)

country = st.selectbox(
    "Country",
    ["France", "Germany", "Spain"]
)

gender = st.selectbox(
    "Gender",
    ["Male", "Female"]
)

age = st.number_input("Age", 18, 100, 40)

tenure = st.number_input(
    "Tenure (Years)",
    0,
    10,
    5
)

balance = st.number_input(
    "Balance",
    0.0,
    250000.0,
    50000.0
)

products_number = st.number_input(
    "Products Number",
    1,
    4,
    2
)

credit_card = st.selectbox(
    "Credit Card",
    [0, 1]
)

active_member = st.selectbox(
    "Active Member",
    [0, 1]
)

estimated_salary = st.number_input(
    "Estimated Salary",
    0.0,
    200000.0,
    70000.0
)

# Prediction Button
if st.button("🔍 Predict Churn"):

    # Your FastAPI URL
    url = "https://bank-customer-churn-early-warning-system.onrender.com/evaluate-churn"

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

    try:
        with st.spinner("Predicting..."):

            response = requests.post(
                url,
                json=payload,
                timeout=60
            )

            st.write("Status Code:", response.status_code)

            if response.status_code == 200:

                result = response.json()

                st.subheader("Prediction Result")

                if result["prediction"] == 1:
                    st.error("⚠ High Risk: Customer will leave the bank")
                else:
                    st.success("✅ Low Risk: Customer will stay")

                st.metric(
                    "Churn Probability",
                    f"{result['churn_probability']}%"
                )

            else:
                st.error(f"API Error: {response.status_code}")
                st.write("Response:")
                st.code(response.text)

    except requests.exceptions.Timeout:
        st.error("Request timed out. Render may be waking up from sleep.")

    except requests.exceptions.ConnectionError:
        st.error("Unable to connect to FastAPI service.")

    except Exception as e:
        st.error(f"Unexpected Error: {e}")
