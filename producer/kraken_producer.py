import os
import time
import requests
from confluent_kafka import Producer
from dotenv import load_dotenv

load_dotenv()

conf = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092'),
    'client.id': 'kraken-producer',
    'acks': 'all',
    'debug': 'msg,broker,fetch'
}

producer = Producer(conf)

KRAKEN_API_URL = 'https://api.kraken.com/0'

def fetch_kraken_trades(pair='XBTUSD'):
    url = f"{KRAKEN_API_URL}/public/Trades?pair={pair}"
    try:
        response = requests.get(url)
        data = response.json()
        if not data.get('result', {}).get(pair):
            print("No trades found for pair:", pair)
        return data.get('result', {}).get(pair, [])
    except Exception as e:
        print(f"API Error: {e}")
        return []

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition}] at offset {msg.offset()}")

if __name__ == "__main__":
    print("Producer started...")
    while True:
        trades = fetch_kraken_trades()
        for trade in trades:
            print("Trade data:", trade)
            producer.produce(
                'kraken-trades',
                key=str(trade[2]),  # Trade ID (ensure this is correct)
                value=str(trade),
                callback=delivery_report
    )
        producer.flush()  # blocks until sent:contentReference[oaicite:8]{index=8}
        time.sleep(5)  # Request Kraken API every 5 seconds
