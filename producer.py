from kafka import KafkaProducer
import pandas as pd
import json
import time

# Load your dataset
df = pd.read_csv("financial_fraud.csv")

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers='127.0.0.1:9092',
    api_version=(0, 10, 1),
    request_timeout_ms=60000,
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

print("Producer Started...\n")

# Send transactions one by one
for index, row in df.iterrows():

    transaction = row.to_dict()

    producer.send(
        'transaction_stream',
        value=transaction
    )

    print("Transaction Sent:", transaction)

    # Simulate real-time streaming
    time.sleep(2)