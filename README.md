# Kafka + Zookeeper Setup using Docker

This guide helps you run **Zookeeper** and **Kafka** locally using Docker.

---

### 🧩 Run Zookeeper

```bash
docker run --name zookeeper   -p 2181:2181   -e ZOOKEEPER_CLIENT_PORT=2181   confluentinc/cp-zookeeper:6.2.2
```

### ⚙️ Run Kafka

```bash
docker run --name kafka   -p 9092:9092   -e KAFKA_ZOOKEEPER_CONNECT=<your_ip>:2181   -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://<your_ip>:9092   -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1   confluentinc/cp-kafka:6.2.2
```

---

### ✅ Notes

- Replace `<your_ip>` with your **host machine's IP address**.
- Make sure Docker is running before executing these commands.
- Kafka will be accessible at `PLAINTEXT://<your_ip>:9092`.
