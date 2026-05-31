from db import db

cursor = db.cursor()

def store_alert(transaction_id, prediction, risk_score, risk_level):

    sql = """
    INSERT INTO fraud_alerts
    (
        transaction_id,
        prediction,
        risk_score,
        risk_level
    )
    VALUES (%s,%s,%s,%s)
    """

    values = (
        transaction_id,
        prediction,
        risk_score,
        risk_level
    )

    cursor.execute(sql, values)
    db.commit()

    print("🚨 Alert Stored")