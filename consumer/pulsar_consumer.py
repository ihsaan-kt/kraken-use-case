import os
import time
from pulsar import Client, ConsumerType
from dotenv import load_dotenv

load_dotenv()

PULSAR_SERVICE_URL = os.getenv('PULSAR_SERVICE_URL', 'pulsar://pulsar:6650')
TOPIC = os.getenv('PULSAR_TOPIC', 'kraken-trades')
SUBSCRIPTION = os.getenv('PULSAR_SUBSCRIPTION', 'kraken-sub')

client = Client(PULSAR_SERVICE_URL)
consumer = client.subscribe(
    topic=TOPIC,
    subscription_name=SUBSCRIPTION,
    consumer_type=ConsumerType.Shared,
)


def main():
    print("Pulsar consumer started...")
    while True:
        msg = consumer.receive(timeout_millis=500)
        try:
            print(f"Received message: {msg.data().decode('utf-8')}")
            consumer.acknowledge(msg)
        except Exception as e:
            print(f"Error processing message: {e}")
            consumer.negative_acknowledge(msg)


if __name__ == '__main__':
    try:
        main()
    finally:
        client.close()