import os
import time
from confluent_kafka import Consumer, KafkaException, KafkaError
from dotenv import load_dotenv

load_dotenv()

conf = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092'),
    'group.id': 'kraken-consumer',
    'auto.offset.reset': 'earliest',
    # Critical settings:
    'session.timeout.ms': 30000,          # Increase from default 10s
    'heartbeat.interval.ms': 3000,        # Should be <1/3 of session timeout
    'group.instance.id': 'consumer-1' ,    # Static member ID (optional)
    'debug': 'msg,broker'
}

consumer = Consumer(conf)

def consume():
    consumer.subscribe(['kraken-trades'])

    while True:
        try:
            # Polling without timeout or with a very short timeout (0.1 seconds)
            msg = consumer.poll(timeout=0.1)
            
            if msg is None:
                continue  # No message received within timeout, continue polling
            
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(f"End of partition reached {msg.partition}, offset {msg.offset}")
                else:
                    raise KafkaException(msg.error())
            else:
                print(f"Consumed message: {msg.value().decode('utf-8')}")
        except KafkaException as e:
            print(f"Kafka exception: {e}")
        except Exception as e:
            print(f"General exception: {e}")
        time.sleep(0.1)  # A very short sleep to avoid tight looping

if __name__ == "__main__":
    retries = 10
    for _ in range(retries):
        try:
            print("Attempting to consume...")
            consume()
            break
        except KafkaException as e:
            print(f"Failed to connect to Kafka: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)  # Retry after 5 seconds

