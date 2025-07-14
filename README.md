# Basic HTTP Server

A simple HTTP server built with Python's built-in [`http.server` module](https://docs.python.org/3/library/http.server.html).

## Features

- **Root endpoint (`/`)**: Returns a welcome message with server information
- **Health check endpoint (`/healthcheck`)**: Returns server health status
- **Content-Type**: All responses are served as `text/plain`
- **Logging**: Request logging with timestamps in json format
- **Error handling**: 404 responses for unknown endpoints
- **Environment configuration**: App name can be customized via `APP_NAME` environment variable
- **Helm Charts**: Deploy in any Kubernetes environment
- 
## Requirements

- Python 3 (uses built-in modules only)
- Helm (create an empty chart using `helm create airtasker-server `)
- No external dependencies required
- Docker

## Usage

### Running the server

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

## Stopping the server

Press `Ctrl+C` to stop the server gracefully.