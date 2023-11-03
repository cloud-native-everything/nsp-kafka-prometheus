# Kafka to Prometheus Python App for NSP

This application serves as a bridge to consume messages from Kafka and export them as Prometheus metrics for Network Services Platform Telemtry info (Insight Administrator).

The Nokia NSP is an advanced software solution providing intent-based network optimization and automation across multi-vendor environments. It ensures efficient resource utilization, reduces operational complexity, and enhances network performance through intelligent, automated decision-making and actions.

Nokia NSP telemetry provides real-time, granular network insights through high-frequency data collection, enhancing visibility and enabling proactive network management and optimization.

Apache Kafka is a high-throughput distributed messaging system, while Prometheus monitors and alerts based on time-series data for system observability. Grafana visualizes Prometheus metrics for monitoring and analytical dashboards.

NSP harnesses gRPC for telemetry extraction, funneling data and events into Kafka topics, ready for integrated applications and analytics.


## Setup Instructions

### Create and Activate Virtual Environment

It is recommended to use a virtual environment to isolate project dependencies. Use the following commands to create and activate a virtual environment:

```bash
sudo python3 -m venv .venv
source .venv/bin/activate
```

### Install requirements

After activating the virtual environment, install the required dependencies using pip:
```bash
pip3 install -r requirements.txt
```

## Usage
To start the application and begin consuming messages from Kafka to export as Prometheus metrics, use:

```bash
./nspk2p.py --bootstrap 10.10.10.10:9192 --cert catrust.pem --port 8000 --config metrics.yml
```
Ensure to replace the bootstrap server address, certificate, port, and configuration file path with the ones applicable to your setup.

## Docker image

Here's how you would build and run the container:

Build your Docker image:
```bash
docker build -t nsp-kafka-prometheus-exporter .
```

Run a container from the image:
```bash
docker run -d -p 8000:8000 --name=myexporter \
  -e KAFKA_BOOTSTRAP_SERVERS=your_kafka_server:9092 \
  -e CA_CERT_PATH=/path/inside/container/ca_cert.pem \
  -e METRICS_PORT=8000 \
  -e CONFIG_FILE=/path/inside/container/config.yaml \
  nsp-kafka-prometheus-exporter
```

In the docker run command, you would need to change the environment variables to point to the correct Kafka server, certificate file, and configuration file paths as necessary. Also, you would need to make sure that the CA certificate file and configuration file are available inside the container, either by copying them into the image at build time or by using Docker volumes to mount them at runtime. For example:

```bash
docker run -d -p 8000:8000 --name=myexporter \
  -v /path/to/your/ca_cert.pem:/app/ca_cert.pem \
  -v /path/to/your/config.yaml:/app/config.yaml \
  nsp-kafka-prometheus-exporter
```

This command mounts the CA certificate and the configuration file from your host to the appropriate locations inside the container. Adjust the paths /path/to/your/ca_cert.pem and /path/to/your/config.yaml to the actual paths on your Docker host.

## Contributing

Contributions to this project are welcome. Please fork the repository, make your changes, and submit a pull request.