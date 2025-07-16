#!/usr/bin/env python3
"""
Simple HTTP server to receive Ansible Runner events
This server will log all POST requests it receives from the HTTP plugin
"""

import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EventHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST requests from Ansible Runner HTTP plugin"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            # Parse the JSON data
            event_data = json.loads(post_data.decode('utf-8'))
            
            # Log the event with timestamp
            logger.info("=" * 60)
            logger.info(f"ANSIBLE EVENT RECEIVED at {datetime.now()}")
            logger.info("=" * 60)
            logger.info(f"Event Type: {event_data.get('event', 'Unknown')}")
            logger.info(f"Status: {event_data.get('status', 'Unknown')}")
            
            # Pretty print the full event data
            print(json.dumps(event_data, indent=2))
            
            # Send response back
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "received"}')
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            self.send_response(400)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Override to reduce noise in logs"""
        pass

def run_server(port=8080):
    """Start the HTTP server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, EventHandler)
    logger.info(f"Starting HTTP server on port {port}")
    logger.info("This server will receive Ansible events from the HTTP plugin")
    logger.info("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        httpd.server_close()

if __name__ == '__main__':
    run_server() 