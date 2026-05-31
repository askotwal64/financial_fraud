import json
import joblib
import pandas as pd

from kafka import KafkaConsumer

from db import store_transaction
from alerts import store_alert
from behavior import calculate_behavior_risk
from email_alert import send_email_alert
from behavior_db import store_customer_behavior
# Load Model
model = joblib.load("fraud_model.pkl")

# Load Feature Columns
feature_columns = joblib.load("feature_columns.pkl")

# Kafka Consumer
consumer = KafkaConsumer(
    'transaction_stream',
    bootstrap_servers='127.0.0.1:9092',
    api_version=(0, 10, 1),
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Consumer Started...\n")

# Read Messages
for message in consumer:

    transaction = message.value

    print("\nReceived Transaction:")
    print(transaction)

    # Convert Transaction to DataFrame
    data = pd.DataFrame([transaction])

    # One Hot Encoding
    data = pd.get_dummies(
        data,
        columns=['type']
    )

    # Add Missing Columns
    for col in feature_columns:

        if col not in data.columns:
            data[col] = 0

    # Arrange Columns
    data = data[feature_columns]

    # Fraud Probability
    probability = model.predict_proba(data)[0][1]

    print("Probability =", probability)

    # ML Risk Score
    risk_score = round(
        probability * 100,
        2
    )

    # Prediction Label
    if risk_score >= 40:
        prediction_label = "Fraud"

    else:
        prediction_label = "Genuine"

    # Behavior Score
    behavior_score = calculate_behavior_risk(
        transaction
    )

    # Final Risk Score
    final_risk_score = min(
        risk_score + behavior_score,
        100
    )

    # Risk Level
    if final_risk_score >= 80:
        risk_level = "CRITICAL"

    elif final_risk_score >= 60:
        risk_level = "HIGH"

    elif final_risk_score >= 30:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"

    print(f"\nML Risk Score      : {risk_score}")
    print(f"Behavior Score     : {behavior_score}")
    print(f"Final Risk Score   : {final_risk_score}")
    print(f"Risk Level         : {risk_level}")

    # Store Transaction
    store_transaction(
        transaction,
        prediction_label,
        final_risk_score,
        risk_level
    )
    store_customer_behavior(
    transaction["nameOrig"],
    transaction["amount"],
    transaction["origin_location"],
    transaction["date"]
)

    # Fraud Message
    if prediction_label == "Fraud":

        print("🚨 FRAUD DETECTED 🚨")

    else:

        print("✅ Genuine Transaction")

    # Store Alert + Send Email
    if risk_level in ["HIGH", "CRITICAL"]:

        store_alert(
            None,
            prediction_label,
            final_risk_score,
            risk_level
        )

        send_email_alert(
            transaction,
            final_risk_score,
            risk_level
        )