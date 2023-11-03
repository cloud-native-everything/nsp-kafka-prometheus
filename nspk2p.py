#!/usr/bin/env python3

from prometheus_client import start_http_server, Gauge
import json
import argparse
import sys
import os
from datetime import datetime
import yaml
from kafka import KafkaConsumer, TopicPartition

# For gauge
metrics_gauge = {}

def parse_kafka_message(message):
    try:
        return json.loads(message)
    except json.JSONDecodeError:
        print(f"{datetime.now()} - ERROR: Error decoding JSON from Kafka message")
        return None

def update_metrics(telemetry_data, topic_metrics, debug):
    if debug:
        print(f"{datetime.now()} - DEBUG: topic_metrics: {topic_metrics}")
        print(f"{datetime.now()} - DEBUG: telemetry_data: {telemetry_data}")
    for key, metric in topic_metrics.items():
        if debug:
            print(f"{datetime.now()} - DEBUG: topic_metrics key: {key}")
            print(f"{datetime.now()} - DEBUG: topic_metrics metric: {metric}")
        metric_obj = metrics_gauge[metric['name']]
        #json_keys = metric['json_keys']
        #if debug:
        #    print(f"{datetime.now()} - DEBUG: topic_metrics metric json_keys: {json_keys}")        
        labels = {label: telemetry_data[label] for label in metric['labels']}
        if debug:
            print(f"{datetime.now()} - DEBUG: topic_metrics metric labels: {labels}")         
#        metric_obj.labels(**labels).set(telemetry_data[json_keys[key]])
        metric_obj.labels(**labels).set(telemetry_data[metric['nsp_counter']])

def start_app(bootstrap, cert, port, config, debug):
    # Start up the server to expose the metrics.
    start_http_server(int(port))
    print(f"{datetime.now()} - INFO: Prometheus metrics server running on port {port}")

    # Connect to Kafka and assign specific partitions
    try:
        consumer = KafkaConsumer(
            bootstrap_servers=[bootstrap],
            security_protocol='SSL',
            ssl_cafile=cert
        )
    except Exception as e:
        print(f"{datetime.now()} - ERROR: Error creating kafka consumer. {e}")
        sys.exit(1)    


    topic_partitions = [TopicPartition(topic['topic'], topic['partition']) for topic in config['metrics']]
    consumer.assign(topic_partitions)

    # Initialize Prometheus gauges
    for metric in config['metrics']:
        for counter_name, counter_info in metric['counters'].items():
            metrics_gauge[counter_info['name']] = Gauge(
                counter_info['name'],
                counter_info['description'],
                counter_info['labels']
            )

    # Consume messages from Kafka
    for message in consumer:
        if debug:
            print(f"{datetime.now()} - DEBUG: Kafka Consumer Message: {message}")
        data = parse_kafka_message(message.value)
        if data:
            telemetry_data = data.get('data', {}).get('ietf-restconf:notification', {}).get('nsp-kpi:real_time_kpi-event')
            if telemetry_data['kpiType']:
                print(f"{datetime.now()} - INFO: Processing Telemetry Data from {message.topic}: {telemetry_data['kpiType']}")
                for metric_config in config['metrics']:
                    if message.topic == metric_config['topic'] and metric_config['kpiType'] in telemetry_data['kpiType']:
                        update_metrics(telemetry_data, metric_config['counters'],debug)
            else:
                print(f"{datetime.now()} - ERROR: Error getting telemetry_data['kpiType']: {telemetry_data['kpiType']}")            

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Kafka to Prometheus (HTTP server working as source)')
    parser.add_argument('--bootstrap', required=True, type=str, help='Kafka Bootstrap Server (i.e., "10.10.10.10:9192")')
    parser.add_argument('--cert', required=True, type=str, help='CA certificate path for Kafka (i.e., "trustca.pem")')
    parser.add_argument('--port', required=True, type=str, help='HTTP server port (i.e., "8080")')
    parser.add_argument('--config', required=True, type=str, help='YAML file with the list of topics and metrics')
    parser.add_argument('--debug', action='store_true', help='Activate debug mode')

    args = parser.parse_args()
    debug = 1 if args.debug else 0
    try:
        with open(args.config, 'r') as file:
            config = yaml.safe_load(file)
    except Exception as e:
        print(f"{datetime.now()} - ERROR: Error reading configuration file: {e}")
        sys.exit()

    if not os.path.isfile(args.cert):
        print(f"{datetime.now()} - ERROR: The file certicate file does not exist. Exiting the application.", file=sys.stderr)
        sys.exit(1)  # Non-zero exit status indicates an error    

    start_app(args.bootstrap, args.cert, args.port, config, debug)
