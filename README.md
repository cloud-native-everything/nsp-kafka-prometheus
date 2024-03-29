# Kafka to Prometheus Python App for NSP

This application serves as a bridge to consume messages from Kafka and export them as Prometheus metrics for Network Services Platform Telemetry info (Insight Administrator).

The Nokia NSP is an advanced software solution providing intent-based network optimization and automation across multi-vendor environments. It ensures efficient resource utilization, reduces operational complexity, and enhances network performance through intelligent, automated decision-making and actions.

Nokia NSP telemetry provides real-time, granular network insights through high-frequency data collection, enhancing visibility and enabling proactive network management and optimization.

Apache Kafka is a high-throughput distributed messaging system, while Prometheus monitors and alerts based on time-series data for system observability. Grafana visualizes Prometheus metrics for monitoring and analytical dashboards.

NSP harnesses gRPC for telemetry extraction, funneling data and events into Kafka topics, ready for integrated applications and analytics.

![NSP Python Prometheus Exporter for Kafka - Telemetry - Top Level Architecture](images/nsp-python-prometheus-exporter-kafka-telemetry.png)


## Setup Instructions

### Create and Activate Virtual Environment

tested with:
* NSP 23.8
* Linux Rocky 9

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

tested with:
* Docker Compose version v2.21.0
* Docker Engine – Community Version 24.0.6

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

## Troubleshooting

* **How can I get the certificate from my NSP Server?** 
Get it from your NSP Node (k8s node) like this `kubectl cp default/nspos-kafka-0:/opt/bitnami/kafka/config/certs/kafka.truststore.jks ./kafka.truststore.jks`
Then, you need to copy it to the repo folder you git-cloned. And convert it to PEM format. I did my own in two steps, with something like this:
```bash
keytool -importkeystore -srckeystore kafka.truststore.jks -srcstorepass $TRUST_PASS -srcstoretype JKS -destkeystore truststore.p12 -deststoretype PKCS12 -deststorepass $TRUST_PASS
openssl pkcs12 -in truststore.p12 -nokeys -out truststore.pem -passin pass:$TRUST_PASS
```
TRUST_PASS is your password set in the nsp-config.yml file when you deployed NSP

* **--bootstrap server I assume is the NSP server?**
Most of cases, the bootstrap server is your NSP IP and the port 9192 (i.e. 10.10.10.10:9192)


# Disclaimer

**Note:** The code and information provided in this repository are for educational and informational purposes only. By using any code, scripts, or information from this repository, you agree that:

1. **No Warranty**: The code is provided "as is" without warranty of any kind, either expressed or implied, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose. 

2. **No Liability**: In no event shall the author(s) or the employer(s) be liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limited to, procurement of substitute goods or services, loss of use, data, or profits, or business interruption) however caused and on any theory of liability, whether in contract, strict liability, or tort (including negligence or otherwise) arising in any way out of the use of this software, even if advised of the possibility of such damage.

3. **Use at Your Own Risk**: The use of code and information from this repository is entirely at your own risk. You are solely responsible for any technical or financial consequences that may result from using this code.

4. **Compliance**: You are responsible for ensuring that your use of the code complies with all relevant laws, regulations, and ethical standards.

5. **No Support**: The author(s) and the employer(s) are not obligated to provide any support or assistance related to the code or its usage.

Please exercise caution and due diligence when using the code and information provided in this repository. Always thoroughly review and test any code before using it in production environments. This disclaimer is subject to change without notice. By using the code and information in this repository, you acknowledge and agree to this disclaimer.

If you do not agree with this disclaimer, do not use the code or information provided in this repository.
