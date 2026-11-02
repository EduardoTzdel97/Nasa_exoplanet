import json

from confluent_kafka import Consumer, KafkaError, KafkaException, kafkaException

def main() -> None:
    consumer = Consumer({
        "bootstrap.servers": "127.0.0.1:9092",
        "group.id": "exoplanet-learning",
        "broker.address.family": "v4",
        "enable.auto.commit": False,
        "auto.offset.reset": "earliest",
    })

    consumer.subscribe(["learning.planets"])

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    raise KafkaException(msg.error())


            raw_value = msg.value()
            if raw_value is not None:
                print(f"Received message: {raw_value.decode('utf-8')}")
                continue

            planet = json.loads(raw_value.decode('utf-8'))
            print(f"Received planet: {planet}")

    except KeyboardInterrupt:
            print("Aborted by user")
    finally:
        consumer.close()


if __name__ == "__main__":
    main()