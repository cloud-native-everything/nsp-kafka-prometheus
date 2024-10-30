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
    #topic = 'ns-eg-5ac43fe9-00f3-4817-ab32-a695712b5395'  ##{ "categories": [ { "name": "NSP-FAULT", "propertyFilter": "severity = 'info'" } ], "asyncCreate": "false", "persist": "true", "clientId":"FM" }
    #topic = 'ns-eg-062534de-68d8-4000-87bd-88988cbf0e42'  ##{ "categories": [ { "name": "NSP-EQUIPMENT" } ], "asyncCreate": "false", "persist": "true", "clientId":"FM" }
    #topic = 'ns-eg-0dc98268-a1df-442d-8c44-c5dd1571e040'  ## system-info
    #topic = 'ns-eg-f3e0581f-9e40-422c-83a5-3dc26cd38426'  ## lsp octects stats
    topic = 'ns-eg-748d7e3c-0194-4b2b-85ca-bf6dd72ca1ad' ## telemetry:/base/sros-router/router_bgp_statistics
    #topic = 'nsp-act-action-event'  ## treshold indicator events
    partition = 0

    consumer = create_consumer(bootstrap_servers, group_id, ssl_ca_location)
    consume_topic(consumer, topic, partition)
    #consume_any_topic(consumer)

if __name__ == "__main__":
    main()
