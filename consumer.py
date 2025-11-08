# File: consumer.py
import sys
import json
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

# --- Configuration ---
KAFKA_BROKER = '192.168.1.5:9092'
TOPIC_NAME = 'driver_locations'
# ---------------------

# Check for command-line arguments
if len(sys.argv) != 2:
    print("Usage: python consumer.py <group_id>")
    print("Example: python consumer.py group1")
    sys.exit(1)

group_id = sys.argv[1]
print(f"Starting consumer for group '{group_id}' on topic '{TOPIC_NAME}'...")

try:
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BROKER,
        group_id=group_id,
        auto_offset_reset='earliest',  # Start reading from the beginning of the topic
        # Decode values from bytes (assuming JSON)
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    # Loop forever, polling for new messages
    for message in consumer:
        print(f"\nReceived message from Partition: {message.partition}")
        print(f"Key: {message.key.decode('utf-8') if message.key else 'None'}")
        print(f"Value: {message.value}")

except NoBrokersAvailable:
    print(f"Error: Could not connect to Kafka broker at {KAFKA_BROKER}")
    sys.exit(1)
except KeyboardInterrupt:
    print("\nConsumer stopped.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if 'consumer' in locals():
        consumer.close()
    print("Consumer closed.")
