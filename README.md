# Basic HTTP Server

A simple HTTP server built with Python's built-in [`http.server` module](https://docs.python.org/3/library/http.server.html).

## Table of Contents

- [Basic HTTP Server](#basic-http-server)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Usage](#usage)
    - [Running the server Locally](#running-the-server-locally)
    - [Testing the endpoints](#testing-the-endpoints)
    - [Running the server on Minikube](#running-the-server-on-minikube)
  - [Stopping the server](#stopping-the-server)

---

## Features

- **Root endpoint (`/`)**: Returns a welcome message with server information
- **Health check endpoint (`/healthcheck`)**: Returns server health status
- **Content-Type**: All responses are served as `text/plain`
- **Logging**: Request logging with timestamps in json format
- **Error handling**: 404 responses for unknown endpoints
- **Environment configuration**: App name can be customized via `APP_NAME` environment variable either via config map or secrets
- **Simple Kubernetes Cluster**: Creates a Minikube cluster
- **Helm Charts**: Deploy in any Kubernetes environment

## Requirements

- Python 3 (uses built-in modules only)
- Helm (create an empty chart using `helm create airtasker-server `)
- No external dependencies required
- Docker 27.4.0
- Minikube Kubernetes Cluster v1.36.0

## Usage

### Running the server Locally

```bash
# Run with default port (8000)
python server.py

# Run with custom port
python server.py 8080

# Run with custom app name
APP_NAME="airtasker1" python server.py

# Run with both custom app name and port
APP_NAME="airtasker2" python server.py 8080
```

Additional config for the application can be set in [`src/config.py`](src/config.py) file. 

### Testing the endpoints

Once the server is running, you can test the endpoints:

```bash
# Test root endpoint
curl http://localhost:8000/

# Test health check endpoint
curl http://localhost:8000/healthcheck

# Test with browser
# Open http://localhost:8000/ in your browser
```

### Running the server on Minikube

```bash
# Start the Minikube cluster, use `--nodes 2` for multi-node cluster
# This will also enable the registry and dashboard add ons.
minikube start \
  --driver=docker\
  --addons=registry,dashboard,ingress,ingress-dns,metrics-server 

make push-docker

make deploy-chart

# Stop the minikube cluster 
minikube stop
```

## Stopping the server

Press `Ctrl+C` to stop the server gracefully.