import time
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, NoBrokersAvailable

# --- Configuration ---
KAFKA_BROKER = '192.168.1.5:9092'
TOPIC_NAME = 'driver_locations'
PARTITIONS = 2
REPLICATION_FACTOR = 1  # Since you are running a single broker
# ---------------------

print(f"Connecting to Kafka broker at {KAFKA_BROKER}...")
admin_client = KafkaAdminClient(
    bootstrap_servers=KAFKA_BROKER,
    client_id='topic_creator'
)
print("Connection successful.")

# Create the new topic
topic = NewTopic(
    name=TOPIC_NAME,
    num_partitions=PARTITIONS,
    replication_factor=REPLICATION_FACTOR
)

print(f"Attempting to create topic '{TOPIC_NAME}' with {PARTITIONS} partitions...")
try:
    admin_client.create_topics(new_topics=[topic], validate_only=False)
    print(f"Topic '{TOPIC_NAME}' created successfully.")
except TopicAlreadyExistsError:
    print(f"Topic '{TOPIC_NAME}' already exists.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    admin_client.close()
    print("Admin client closed.")

