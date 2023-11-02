#!/usr/bin/env python3

from prometheus_client import start_http_server, Gauge
import time
import json
import argparse
import sys
import yaml
from kafka import KafkaConsumer, TopicPartition


# For gauge
metrics_gauge = {}

# Prometheus metrics to collect
#AGGR_PACKETS = Gauge('aggregate_packets', 'Aggregate packets', ['name'])
#AGGR_OCTETS = Gauge('aggregate_octets', 'Aggregate octets', ['name'])
#CPU_USAGE = Gauge('cpu_usage', 'CPU usage', ['neId'])
#MEM_USE = Gauge('mem_use', 'Memory use', ['neId'])

def parse_kafka_message(message):
    try:
        return json.loads(message)
    except json.JSONDecodeError:
        print("Error decoding JSON from Kafka message")
        return None

def update_metrics_lsp_egress(data):
    # Extracting the relevant fields from the data
    #name = data['name']
    #aggregate_packets = data['aggregate-packets']
    #aggregate_octets = data['aggregate-octets']
    
    # Updating Prometheus gauges
    metrics_gauge['aggregate_packets'].labels(data['name']).set(data['aggregate-packets'])
    metrics_gauge['aggregate_octets'].labels(data['name']).set(data['aggregate-octets'])

def update_metrics_system(data):
    # Extracting the relevant fields from the data
    #neId = data['neId']
    #cpu_usage = data['cpu-usage']
    #mem_use = data['memory-used']
    
    # Updating Prometheus gauges
    metrics_gauge['cpu_usage'].labels(data['neId']).set(data['cpu-usage'])
    metrics_gauge['mem_use'].labels(data['neId']).set(data['memory-used'])

def start_app(bootstrap, cert, port, topics, metrics):
    # Start up the server to expose the metrics.
    start_http_server(int(port))
    print("Prometheus metrics server running on port 8000")

    # Connect to Kafka and assign specific partitions (only partition 0 for each topic)
    consumer = KafkaConsumer(
        bootstrap_servers=[bootstrap],
        security_protocol='SSL',
        ssl_cafile=cert
    )

    topic_partitions = [TopicPartition(topic['id'], topic['partition']) 
                        for topic in topics['topics']]     
    consumer.assign(topic_partitions)

    for metric_name, metric_info in metrics['metrics'].items():
        metrics_gauge[metric_name] = Gauge(
            metric_info['name'],
            metric_info['description'],
            metric_info['labels']
        )

    # Consume messages from Kafka
    for message in consumer:
        print(message)
        data = parse_kafka_message(message.value)
        if data:
            telemetry_data = data.get('data', {}).get('ietf-restconf:notification', {}).get('nsp-kpi:real_time_kpi-event')
            if 'lsp-egress' in telemetry_data['kpiType']:
                update_metrics_lsp_egress(telemetry_data)
            if 'system-info' in telemetry_data['kpiType']:
                update_metrics_system(telemetry_data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Kafka to Prometheus (http server working as source)')
    parser.add_argument('--bootstrap', type=str, help='Kafka Bootstrap Server (i.e. 10.10.10.10:9192)')
    parser.add_argument('--cert', type=str, help='CA certificate path for kafka (i.e. trustca.pem)')    
    parser.add_argument('--port', type=str, help='HTTP server port (i.e. 8080)')      
    parser.add_argument('--topics', type=str, help='YAML file with the list of topics')
    parser.add_argument('--metrics', type=str, help='YAML file with the list of presented metrics')     
    # Add more arguments as needed
    
    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        sys.exit() 

    if not args.topics:
        print("ERROR: Please, specify a topics file\n")
        parser.print_help()
        sys.exit()

    try:
        with open(args.topics, 'r') as file:
            topics = yaml.safe_load(file)
    except Exception as e:
        print(f"Error reading topic file: {e}")
        exit()

    try:
        with open(args.metrics, 'r') as file:
            metrics = yaml.safe_load(file)
    except Exception as e:
        print(f"Error reading metric file: {e}")
        exit()

    start_app(args.bootstrap, args.cert, args.port, topics, metrics)   