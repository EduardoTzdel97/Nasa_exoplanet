import json

from extract_sample import fetch_sample
from confluent_kafka import Producer



def report_delivery(err, msg) -> None:
    """
    Callback function to report the delivery status of a message.

    Args:
        err (KafkaError): The error object if the message failed to deliver.
        msg (Message): The message object that was sent.
    """
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")



def main() -> None:
    producer = Producer(    {
        "bootstrap.servers": "127.0.0.1:9092",
        "broker.address.family": "v4",
    })
    planets = fetch_sample()

    for planet in planets:
        producer.produce('learning.planets', value = json.dumps(planet).encode('utf-8'),
                         on_delivery=report_delivery,)

    pending_messages = producer.flush(timeout=10)

    if pending_messages > 0:
        print(f"Warning: {pending_messages} messages were not delivered within the timeout period.")



if __name__ == "__main__":
    main()