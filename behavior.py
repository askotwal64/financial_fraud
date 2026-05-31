from db import db

cursor = db.cursor(dictionary=True)

def calculate_behavior_risk(transaction):

    risk = 0

    amount = transaction['amount']

    transaction_type = transaction['type']

    customer_id = transaction['nameOrig']

    # High Amount Transactions
    if amount > 100000:
        risk += 40

    elif amount > 50000:
        risk += 20

    # High Risk Transaction Types
    if transaction_type == "TRANSFER":
        risk += 20

    elif transaction_type == "CASH_OUT":
        risk += 10
    return min(risk, 100)

    # Customer Transaction History
    cursor.execute("""
        SELECT COUNT(*) AS total_transactions
        FROM transactions
        WHERE sender = %s
    """, (customer_id,))

    result = cursor.fetchone()

    if result:

        total_transactions = result["total_transactions"]

        if total_transactions > 100:
            risk += 10

    return min(risk, 100)