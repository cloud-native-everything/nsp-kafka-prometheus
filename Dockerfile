# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./nspk2p.py /app/nspk2p.py

# Install any needed packages specified in requirements.txt
# Make sure to have a requirements.txt file with prometheus_client, kafka-python, PyYAML etc.
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Remeber to define environment variables, like:
#ENV KAFKA_BOOTSTRAP_SERVERS=localhost:9092
#ENV CA_CERT_PATH=/app/ca_cert.pem
#ENV METRICS_PORT=8000
#ENV CONFIG_FILE=/app/metrics.yml

# Run the Python application when the container launches
CMD python3 ./nspk2p.py --bootstrap ${KAFKA_BOOTSTRAP_SERVERS} --cert ${CA_CERT_PATH} --port ${METRICS_PORT} --config ${CONFIG_FILE} --debug
