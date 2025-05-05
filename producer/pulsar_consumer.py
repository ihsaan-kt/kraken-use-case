import os
import time
from pulsar import Client, Producer
from dotenv import load_dotenv

load_dotenv()

# Pulsar service URL (use Pulsar broker container name)
PULSAR_SERVICE_URL = os.getenv('PULSAR_SERVICE_URL', 'pulsar://pulsar:6650')
TOPIC = os.getenv('PULSAR_TOPIC', 'kraken-trades')

client = Client(PULSAR_SERVICE_URL)
producer: Producer = client.create_producer(
    topic=TOPIC,
    schema=None  # sending raw bytes/strings
)

KRAKEN_API_URL = 'https://api.kraken.com/0/public/Trades'


def fetch_kraken_trades(pair='XBTUSD'):
    url = f"{KRAKEN_API_URL}?pair={pair}"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get('result', {}).get(pair, [])
    except Exception as e:
        print(f"API Error: {e}")
        return []


def main():
    print("Pulsar producer started...")
    while True:
        trades = fetch_kraken_trades()
        for trade in trades:
            msg = str(trade)
            producer.send(msg.encode('utf-8'))
            print(f"Sent trade: {msg}")
        time.sleep(5)


if __name__ == '__main__':
    try:
        main()
    finally:
        client.close()