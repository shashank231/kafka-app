# File: producer.py
import sys
import json
import time
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

# --- Configuration ---
KAFKA_BROKER = '192.168.1.5:9092'
TOPIC_NAME = 'driver_locations'
# ---------------------

def get_partition(location):
    """
    Assigns a partition based on location.
    Partition 0 for 'North', Partition 1 for 'South'.
    """
    if location.lower() == 'north':
        return 0
    elif location.lower() == 'south':
        return 1
    else:
        # Default partition for other locations (optional)
        return 0

# Check for command-line arguments
if len(sys.argv) != 3:
    print("Usage: python producer.py <driver_id> <location>")
    print("Example: python producer.py driver1 North")
    sys.exit(1)

driver_id = sys.argv[1]
location = sys.argv[2]
partition_to_use = get_partition(location)

# Create the message
message = {
    'driver': driver_id,
    'location': location,
    'timestamp': time.time()
}

# Connect to Kafka
try:
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        # Encode key and value as bytes
        key_serializer=lambda k: k.encode('utf-8'),
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    # Serializers are translators. 
        # Kafka doesn't understand Python objects like strings, numbers, or dictionaries. 
        # It only understands raw bytes
        # The serializer's job is to convert your Python data into bytes before sending it to Kafka.
        # key_serializer
            # This tells the producer how to translate the key (in your case, the driver_id string).
            # Your Code: lambda k: k.encode('utf-8')
            # What it does: It takes a Python string (the key, k) and calls the .encode('utf-8') method on it. 
            #   This turns the string into its byte representation.
        # value_serializer
            # This tells the producer how to translate the value (your main message, which is a Python dictionary). 
            # This one is a two-step process.
            # Your Code: lambda v: json.dumps(v).encode('utf-8')
            # What it does:
            # json.dumps(v): First, it takes the Python dictionary (the value, v) and uses
            # the json library to serialize it into a JSON-formatted string.
            # .encode('utf-8'): Second, it takes that new JSON string and encodes that into bytes.
except NoBrokersAvailable:
    print(f"Error: Could not connect to Kafka broker at {KAFKA_BROKER}")
    sys.exit(1)

# Send the message
try:
    print(f"Sending message: {message} to partition {partition_to_use}")
    producer.send(
        TOPIC_NAME,
        key=driver_id,
        value=message,
        partition=partition_to_use  # Manually specify the partition
    )
    # Block until messages are sent (or timeout)
    producer.flush()
    print("Message sent successfully.")
except Exception as e:
    print(f"An error occurred while sending message: {e}")
finally:
    producer.close()
    print("Producer closed.")

