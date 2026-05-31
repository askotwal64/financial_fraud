from fastapi import FastAPI
import mysql.connector
import pandas as pd

app = FastAPI()

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
    database="fraud_detection"
)

cursor = db.cursor(dictionary=True)

@app.get("/")
def home():
    return {"message": "Fraud Detection API Running"}

@app.get("/transactions")
def get_transactions():

    cursor.execute("""
        SELECT *
        FROM transactions
        ORDER BY id DESC
        LIMIT 100
    """)

    data = cursor.fetchall()

    return data


@app.get("/alerts")
def get_alerts():

    cursor.execute("""
        SELECT *
        FROM fraud_alerts
        ORDER BY alert_id DESC
    """)

    data = cursor.fetchall()

    return data