#!/usr/bin/env python3
"""
Simple HTTP server for health checks and basic responses
"""
import http.server
import socketserver
from datetime import datetime
import json
import logging
from config import config

# Configure logging
logging.basicConfig(
    level=getattr(logging, config["log_level"].upper()),
    format=config["log_format"],
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(config["log_file"])
    ]
)
logger = logging.getLogger(__name__)

class BasicHTTPServer(http.server.BaseHTTPRequestHandler):
  def do_GET(self):
    """Handle GET requests for the two endpoints"""

    # Set common headers
    self.send_response(200)
    self.send_header("Content-type", "text/plain")
    self.send_header("Access-Control-Allow-Origin", config["cors_origin"])
    self.end_headers()

    # Route to appropriate handler based on path
    if self.path == "/":
      self.handle_root()
    elif self.path == "/healthcheck":
      self.handle_healthcheck()
    else:
      self.handle_not_found()

  def handle_root(self):
    """Handle requests to the root endpoint"""
    response = f"{config['app_name']}!\n"
    self.wfile.write(response.encode("utf-8"))

  def handle_healthcheck(self):
    """Handle requests to the healthcheck endpoint"""
    response = "OK\n"

    self.wfile.write(response.encode("utf-8"))

  def handle_not_found(self):
    """Handle 404 requests"""
    self.send_response(404)
    self.send_header("Content-type", "text/plain")
    self.end_headers()

    response = f"404 - Not Found\n"
    response += f"Path '{self.path}' does not exist\n"
    response += "Available endpoints: /, /healthcheck\n"

    self.wfile.write(response.encode("utf-8"))

  def log_message(self, format, *args):
    """Override to provide better logging"""
    message = format % args
    logger.info(f"HTTP Request: {message}")
    
    # Also log as JSON for structured logging
    log_entry = {
      "timestamp": datetime.now().isoformat(),
      "level": "INFO",
      "message": message,
      "type": "access_log",
      "logger": "http_server"
    }
    logger.debug(json.dumps(log_entry))


def run_server(port=None):
  """Run the HTTP server on the specified port"""
  if port is None:
    port = config["server_port"]
  
  host = config["server_host"]
  handler = BasicHTTPServer

  with socketserver.TCPServer((host, port), handler) as httpd:
    logger.info(f"Server started at http://{host or 'localhost'}:{port}")
    logger.info("Available endpoints:")
    logger.info(f"  - http://{host or 'localhost'}:{port}/")
    logger.info(f"  - http://{host or 'localhost'}:{port}/healthcheck")
    logger.info("Press Ctrl+C to stop the server")

    try:
      httpd.serve_forever()
    except KeyboardInterrupt:
      logger.info("Shutting down server...")
      httpd.shutdown()


if __name__ == "__main__":
  import sys

  # Get port from command line argument or use config default
  port = None
  if len(sys.argv) > 1:
    try:
      port = int(sys.argv[1])
    except ValueError:
      logger.warning(f"Invalid port number. Using default port {config['server_port']}.")

  run_server(port)
