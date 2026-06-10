from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI()
model = joblib.load("models/churn_model.pkl")
country_encoder = joblib.load("models/country_encoder.pkl")
gender_encoder = joblib.load("models/gender_encoder.pkl")

class Customer(BaseModel):
    credit_score: int
    country: str
    gender: str
    age: int
    tenure: int
    balance: float
    products_number: int
    credit_card: int
    active_member: int
    estimated_salary: float

@app.get("/")
def home():
    return {"message": "Bank Churn API Running Successfully"}

@app.post("/evaluate-churn")
def evaluate_churn(customer: Customer):

    country = country_encoder.transform([customer.country])[0]
    gender = gender_encoder.transform([customer.gender])[0]

    data = pd.DataFrame([{
        "credit_score": customer.credit_score,
        "country": country,
        "gender": gender,
        "age": customer.age,
        "tenure": customer.tenure,
        "balance": customer.balance,
        "products_number": customer.products_number,
        "credit_card": customer.credit_card,
        "active_member": customer.active_member,
        "estimated_salary": customer.estimated_salary
    }])

    pred = model.predict(data)[0]

    prob = model.predict_proba(data)[0][1]

    return {
        "prediction": int(pred),
        "churn_probability": round(prob * 100, 2)
    }

from typing import List

class BulkCustomer(Customer):
    customer_id: int

@app.post("/bulk-churn-check")
def bulk_churn_check(customers: List[BulkCustomer]):

    results = []

    for customer in customers:

        country = country_encoder.transform([customer.country])[0]
        gender = gender_encoder.transform([customer.gender])[0]

        data = pd.DataFrame([{
            "credit_score": customer.credit_score,
            "country": country,
            "gender": gender,
            "age": customer.age,
            "tenure": customer.tenure,
            "balance": customer.balance,
            "products_number": customer.products_number,
            "credit_card": customer.credit_card,
            "active_member": customer.active_member,
            "estimated_salary": customer.estimated_salary
        }])

        prob = model.predict_proba(data)[0][1]

        results.append({
            "customer_id": customer.customer_id,
            "risk": round(prob * 100, 2)
        })

    results.sort(
        key=lambda x: x["risk"],
        reverse=True
    )

    return results