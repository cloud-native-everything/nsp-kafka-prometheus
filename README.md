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

Here's how you would build and run the container or pull it in case you don't want to build it on your own:

Build your Docker image:
```bash
docker build -t ghcr.io/cloud-native-everything/nsp-kafka-prometheus:v2311 .
```
The package is also publicly available in case you want to skip this step.
```bash
docker pull ghcr.io/cloud-native-everything/nsp-kafka-prometheus:v2311
```

Run a container from the image:
```bash
docker run -d -p 8000:8000 --name=myexporter \
  -v .:/app
  -e KAFKA_BOOTSTRAP_SERVERS=your_kafka_server:9092 \
  -e CA_CERT_PATH=/app/ca_cert.pem \
  -e METRICS_PORT=8000 \
  -e CONFIG_FILE=/app/config.yaml \
  ghcr.io/cloud-native-everything/nsp-kafka-prometheus:v2311
```

In the docker run command, you would need to change the environment variables to point to the correct Kafka server, certificate file, and configuration file paths as necessary. Also, you would need to make sure that the CA certificate file and configuration file are available inside the container, either by copying them into the image at build time or by using Docker volumes to mount them at runtime. In the example, `-v .:/app` is mounting the local directory assuming all required fikles are in it. 


This command mounts the CA certificate and the configuration file from your host to the appropriate locations inside the container. Adjust the paths /app/ca_cert.pem and /app/config.yaml to the actual paths are you planing to use.

## Docker Compose Setup

This project can be run using Docker Compose, which orchestrates the deployment of the Prometheus, Grafana, and Kafka Prometheus Exporter services.

### Prerequisites
- Docker and Docker Compose must be installed on your system.
- Ensure that the `prometheus.cfg`, `metrics.yml`, and the necessary Grafana provisioning files are present in the respective directories.

### Running the Services

To start the services, follow these steps:

1. **Set Environment Variables:**
   Optionally, you can set the `NSP_BOOTSTRAP_SERVER` environment variable to your Kafka bootstrap server address if it's different from the default in the `docker-compose.yml` file. Similarly, update the `CA_KAFKA_CERT` if you have a different certificate filename.

   ```bash
   export NSP_BOOTSTRAP_SERVER=your_kafka_bootstrap_server_address
   export CA_KAFKA_CERT=your_certificate_filename.pem

2. **Start Services:**
Navigate to the directory containing your docker-compose.yml file and run the following command:

```bash
docker-compose up -d
```
This command will start the Prometheus, Grafana, and Kafka Prometheus Exporter services in detached mode.

3. **Accessing the Services:**

* Prometheus will be available at `http://<your-server-ip>:9090`.
* Grafana will be available at `http://<your-server-ip>:3000`. The default login is admin and the password is secret (unless you've changed the `GF_SECURITY_ADMIN_PASSWORD` variable).
4. **Stopping the Services:**
To stop and remove all the running services, you can use the following command:
```bash
docker-compose down
```
### Troubleshooting
* If you encounter any issues with starting the services, you can check the logs for each service using:
```bash
docker-compose logs service_name
```
* Ensure that the volume mounts correspond to the actual directories and file paths on your host.

## Custom Configuration
* For custom configuration of Prometheus or Grafana, modify the configuration files located in `./prometheus/` and `./grafana/` directories respectively.
* The Kafka Prometheus Exporter service is configured via the metrics.yml file. If you need to make changes, update this file accordingly.

Replace `<your-server-ip>` with the actual IP address of your server. If you're running it locally.

