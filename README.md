# Kafka to Prometheus Pyhton App

## Setup
### Create and Activate Virtual Environment

First, create a virtual environment in Python to isolate the dependencies for this project and activate it:

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

```bash
./nspk2p-0.1.py --bootstrap 10.10.10.10:9192 --cert catrust.pem --port 8000 --topics topics.yml --metrics metrics.yml
```