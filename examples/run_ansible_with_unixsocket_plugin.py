#!/usr/bin/env python3
"""
Example script showing how to use Ansible Runner with the HTTP plugin via Unix socket
This script will run an Ansible playbook and send events to a Unix socket endpoint
"""

import os
import sys
import ansible_runner
import tempfile
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_playbook_with_unixsocket_plugin():
    """
    Run an Ansible playbook using ansible-runner with HTTP plugin via Unix socket
    """
    
    # Configuration for the HTTP plugin via Unix socket
    # The key insight is that the plugin detects Unix sockets by checking if the URL is a file path
    socket_path = "/tmp/ansible-runner.sock"
    
    unixsocket_config = {
        'runner_http_url': socket_path,  # Unix socket path instead of HTTP URL
        'runner_http_path': '/ansible-events',  # Optional path (works with Unix sockets too)
        'runner_http_headers': {  # Optional headers
            'Content-Type': 'application/json',
            'X-Source': 'ansible-runner-unix-demo'
        }
    }
    
    logger.info("=" * 60)
    logger.info("STARTING ANSIBLE RUNNER WITH UNIX SOCKET PLUGIN")
    logger.info("=" * 60)
    logger.info(f"Sending events to Unix socket: {socket_path}")
    logger.info("Make sure your Unix socket server is running!")
    logger.info("=" * 60)
    
    # Check if socket exists (server should be running)
    if not os.path.exists(socket_path):
        logger.warning(f"⚠️  Unix socket not found at {socket_path}")
        logger.warning("Make sure to start the Unix socket server first!")
        logger.warning("Run: python examples/simple_unixsocket_server.py")
    
    # Create a temporary directory for ansible-runner
    with tempfile.TemporaryDirectory() as tmp_dir:
        project_dir = os.path.join(tmp_dir, 'project')
        os.makedirs(project_dir)
        
        # Copy our playbook to the project directory
        playbook_path = os.path.join(project_dir, 'simple_playbook.yml')
        
        # Read the playbook content
        script_dir = os.path.dirname(__file__)
        source_playbook = os.path.join(script_dir, 'simple_playbook.yml')
        
        if not os.path.exists(source_playbook):
            logger.error(f"Playbook not found at {source_playbook}")
            logger.error("Make sure you're running this script from the examples directory")
            return False
        
        with open(source_playbook, 'r') as f:
            playbook_content = f.read()
        
        with open(playbook_path, 'w') as f:
            f.write(playbook_content)
        
        # Run the playbook with ansible-runner
        try:
            result = ansible_runner.run(
                project_dir=project_dir,
                playbook='simple_playbook.yml',
                settings=unixsocket_config,  # This enables the HTTP plugin with Unix socket
                verbosity=1
            )
            
            logger.info("=" * 60)
            logger.info("ANSIBLE RUNNER RESULTS")
            logger.info("=" * 60)
            logger.info(f"Status: {result.status}")
            logger.info(f"Return code: {result.rc}")
            logger.info(f"Stats: {result.stats}")
            
            if result.status == 'successful':
                logger.info("✅ Playbook completed successfully!")
                logger.info("Check your Unix socket server logs to see the events that were sent.")
            else:
                logger.error("❌ Playbook failed!")
                
            return result.status == 'successful'
            
        except Exception as e:
            logger.error(f"Error running playbook: {e}")
            return False

def run_with_environment_variables():
    """
    Alternative method: Configure HTTP plugin for Unix socket using environment variables
    """
    
    logger.info("=" * 60)
    logger.info("RUNNING WITH ENVIRONMENT VARIABLES (UNIX SOCKET)")
    logger.info("=" * 60)
    
    socket_path = "/tmp/ansible-runner.sock"
    
    # Set environment variables for HTTP plugin with Unix socket
    os.environ['RUNNER_HTTP_URL'] = socket_path
    os.environ['RUNNER_HTTP_PATH'] = '/ansible-events-env'
    
    logger.info(f"Using Unix socket: {socket_path}")
    
    # Check if socket exists
    if not os.path.exists(socket_path):
        logger.warning(f"⚠️  Unix socket not found at {socket_path}")
        logger.warning("Make sure to start the Unix socket server first!")
    
    # Create a temporary directory for ansible-runner
    with tempfile.TemporaryDirectory() as tmp_dir:
        project_dir = os.path.join(tmp_dir, 'project')
        os.makedirs(project_dir)
        
        # Copy our playbook to the project directory
        playbook_path = os.path.join(project_dir, 'simple_playbook.yml')
        
        # Read the playbook content
        script_dir = os.path.dirname(__file__)
        source_playbook = os.path.join(script_dir, 'simple_playbook.yml')
        
        with open(source_playbook, 'r') as f:
            playbook_content = f.read()
        
        with open(playbook_path, 'w') as f:
            f.write(playbook_content)
        
        # Run without explicit settings - will use environment variables
        result = ansible_runner.run(
            project_dir=project_dir,
            playbook='simple_playbook.yml',
            verbosity=1
        )
        
        logger.info(f"Status: {result.status}")
        return result.status == 'successful'

def run_with_custom_socket_path():
    """
    Method using a custom socket path for demonstration
    """
    
    custom_socket = "/tmp/my-custom-ansible.sock"
    
    logger.info("=" * 60)
    logger.info("RUNNING WITH CUSTOM SOCKET PATH")
    logger.info("=" * 60)
    logger.info(f"Using custom socket: {custom_socket}")
    
    unixsocket_config = {
        'runner_http_url': custom_socket,
        'runner_http_path': '/custom-events',
        'runner_http_headers': {
            'Content-Type': 'application/json',
            'X-Source': 'ansible-runner-custom-socket'
        }
    }
    
    logger.info("Note: Make sure to start the server with this custom path:")
    logger.info(f"python examples/simple_unixsocket_server.py {custom_socket}")
    
    # Check if socket exists
    if not os.path.exists(custom_socket):
        logger.warning(f"⚠️  Custom Unix socket not found at {custom_socket}")
        logger.warning("This demo will likely fail unless the server is running with this path!")
    
    # Create a temporary directory for ansible-runner
    with tempfile.TemporaryDirectory() as tmp_dir:
        project_dir = os.path.join(tmp_dir, 'project')
        os.makedirs(project_dir)
        
        # Copy our playbook to the project directory
        playbook_path = os.path.join(project_dir, 'simple_playbook.yml')
        
        # Read the playbook content
        script_dir = os.path.dirname(__file__)
        source_playbook = os.path.join(script_dir, 'simple_playbook.yml')
        
        with open(source_playbook, 'r') as f:
            playbook_content = f.read()
        
        with open(playbook_path, 'w') as f:
            f.write(playbook_content)
        
        # Run the playbook
        result = ansible_runner.run(
            project_dir=project_dir,
            playbook='simple_playbook.yml',
            settings=unixsocket_config,
            verbosity=1
        )
        
        logger.info(f"Status: {result.status}")
        return result.status == 'successful'

if __name__ == '__main__':
    print("\n🚀 Ansible Runner Unix Socket Plugin Demo")
    print("=" * 50)
    print("\nThis script demonstrates three ways to use the HTTP plugin with Unix sockets:")
    print("1. Using runner settings with default socket (/tmp/ansible-runner.sock)")
    print("2. Using environment variables with default socket")
    print("3. Using a custom socket path")
    print("\n⚠️  IMPORTANT: Make sure the Unix socket server is running first!")
    print("   Default: python examples/simple_unixsocket_server.py")
    print("   Custom:  python examples/simple_unixsocket_server.py /path/to/socket")
    print("   (in another terminal)")
    
    choice = input("\nWhich method would you like to try? (1/2/3): ").strip()
    
    if choice == '1':
        success = run_playbook_with_unixsocket_plugin()
    elif choice == '2':
        success = run_with_environment_variables()
    elif choice == '3':
        success = run_with_custom_socket_path()
    else:
        print("Invalid choice. Defaulting to method 1.")
        success = run_playbook_with_unixsocket_plugin()
    
    if success:
        print("\n✅ Demo completed successfully!")
        print("Check the Unix socket server terminal to see the events that were received.")
    else:
        print("\n❌ Demo failed. Check the logs above for details.")
    
    sys.exit(0 if success else 1) 