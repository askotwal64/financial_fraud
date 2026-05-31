from db import db

cursor = db.cursor()

def store_customer_behavior(
    customer_id,
    amount,
    location,
    transaction_time
):

    sql = """
    INSERT INTO customer_behavior
    (
        customer_id,
        avg_transaction_amount,
        total_transactions,
        last_location,
        last_transaction_time
    )

    VALUES (%s,%s,%s,%s,%s)

    ON DUPLICATE KEY UPDATE

    avg_transaction_amount =
    (
        avg_transaction_amount + VALUES(avg_transaction_amount)
    ) / 2,

    total_transactions =
    total_transactions + 1,

    last_location =
    VALUES(last_location),

    last_transaction_time =
    VALUES(last_transaction_time)
    """

    values = (
        customer_id,
        amount,
        1,
        location,
        transaction_time
    )

    cursor.execute(sql, values)
    db.commit()