import mysql.connector

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
    database="fraud_detection"
)

cursor = db.cursor()

print("✅ Database Connected Successfully")


def store_transaction(
        transaction,
        prediction,
        risk_score,
        risk_level):

    sql = """
    INSERT INTO transactions
    (
        step,
        transaction_type,
        amount,
        sender,
        oldbalanceOrg,
        newbalanceOrig,
        receiver,
        oldbalanceDest,
        newbalanceDest,
        prediction,
        risk_score,
        risk_level
    )
    VALUES
    (
        %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s
    )
    """

    values = (
        transaction['step'],
        transaction['type'],
        transaction['amount'],

        transaction['nameOrig'],
        transaction['oldbalanceOrg'],
        transaction['newbalanceOrig'],

        transaction['nameDest'],
        transaction['oldbalanceDest'],
        transaction['newbalanceDest'],

        prediction,
        risk_score,
        risk_level
    )

    

    try:
        cursor.execute(sql, values)
        db.commit()

        print("✅ Transaction Stored in MySQL")

    except Exception as e:
        print("❌ Database Error:")
        print(e)