#!/usr/bin/env python3

import json
from confluent_kafka import Consumer, KafkaError
from confluent_kafka import TopicPartition

def create_consumer(bootstrap_servers, group_id, ssl_ca_location):
    consumer_config = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest',
        'security.protocol': 'ssl',
        'ssl.ca.location': ssl_ca_location
    }
    return Consumer(consumer_config)

def consume_any_topic(consumer):
    try:
        # Subscribe the consumer to all topics using a wildcard
        consumer.subscribe(['^.*'])

        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event - not an error
                    print("Reached end of partition")
                    continue
                else:
                    print(msg.error())
                    break

            # Print the message value as a JSON string
            # Print the message value
            try:
                message_value = msg.value().decode('utf-8')
                try:
                    json_message = json.loads(message_value)
                    print(json.dumps(json_message, indent=2))
                except json.JSONDecodeError:
                    print("Message is not a valid JSON format")
                    print(message_value)
            except UnicodeDecodeError:
                print("Message is not UTF-8 encoded, printing raw bytes:")
                print(msg.value())

    finally:
        # Close down consumer to commit final offsets.
        consumer.close()

def consume_topic(consumer, topic, partition):
    try:
        # Assign the consumer to a specific topic and partition
        topic_partition = TopicPartition(topic, partition)
        consumer.assign([topic_partition])        


        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event - not an error
                    print("Reached end of partition")
                    break
                else:
                    print(msg.error())
                    break

            # Print the message value as a JSON string
            try:
                message_value = json.loads(msg.value().decode('utf-8'))
                print(json.dumps(message_value, indent=2))
            except json.JSONDecodeError:
                print("Message is not a valid JSON format")

    finally:
        # Close down consumer to commit final offsets.
        consumer.close()

def main():
    bootstrap_servers = '10.2.16.11:9192'
    group_id = 'my-group'
    ssl_ca_location = 'truststore.pem'
    topic = 'ns-eg-6fef75a8-9476-406b-9efe-795cb4371f94'
    partition = 0

    consumer = create_consumer(bootstrap_servers, group_id, ssl_ca_location)
    consume_topic(consumer, topic, partition)
    #consume_any_topic(consumer)

if __name__ == "__main__":
    main()
