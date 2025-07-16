#!/usr/bin/env python3
"""
Simple Unix socket server to receive Ansible Runner events
"""

import json
import os
import socket

def handle_request(client_socket):
    """Handle a single request"""
    # Read the request
    data = client_socket.recv(8192).decode('utf-8')
    
    # Find JSON in the request (after the headers)
    if '\r\n\r\n' in data:
        _, body = data.split('\r\n\r\n', 1)
        
        if body.strip():
            try:
                # Parse and display the event
                event = json.loads(body)
                print("=" * 50)
                print(f"🎯 Ansible Event: {event.get('event', 'Unknown')}")
                print(f"📊 Status: {event.get('status', 'Unknown')}")
                print("📄 Full Event:")
                print(json.dumps(event, indent=2))
                print("=" * 50)
            except:
                print("❌ Failed to parse event")
    
    # Send simple response
    response = "HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n"
    client_socket.send(response.encode())
    client_socket.close()

def start_server(socket_path="/tmp/ansible-runner.sock"):
    """Start the Unix socket server"""
    # Remove old socket if exists
    if os.path.exists(socket_path):
        os.unlink(socket_path)
    
    # Create and bind socket
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(socket_path)
    os.chmod(socket_path, 0o666)  # Allow connections
    server.listen(5)
    
    print(f"🚀 Unix Socket Server listening on: {socket_path}")
    print("📨 Waiting for Ansible events...")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            client_socket, _ = server.accept()
            handle_request(client_socket)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    finally:
        server.close()
        if os.path.exists(socket_path):
            os.unlink(socket_path)

if __name__ == '__main__':
    import sys
    
    socket_path = "/tmp/ansible-runner.sock"
    if len(sys.argv) > 1:
        socket_path = sys.argv[1]
    
    start_server(socket_path) 