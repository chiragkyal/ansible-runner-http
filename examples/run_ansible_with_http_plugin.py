#!/usr/bin/env python3
"""
Example script showing how to use Ansible Runner with the HTTP plugin
This script will run an Ansible playbook and send events to an HTTP endpoint
"""

import os
import sys
import ansible_runner
import tempfile
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_playbook_with_http_plugin():
    """
    Run an Ansible playbook using ansible-runner with HTTP plugin enabled
    """
    
    # Configuration for the HTTP plugin
    # These can also be set as environment variables
    http_config = {
        'runner_http_url': 'http://localhost:8080',  # Where to send events
        'runner_http_path': '/ansible-events',       # Optional path
        'runner_http_headers': {                     # Optional headers
            'Content-Type': 'application/json',
            'X-Source': 'ansible-runner-demo'
        }
    }
    
    logger.info("=" * 60)
    logger.info("STARTING ANSIBLE RUNNER WITH HTTP PLUGIN")
    logger.info("=" * 60)
    logger.info(f"Sending events to: {http_config['runner_http_url']}{http_config['runner_http_path']}")
    logger.info("Make sure your HTTP server is running on port 8080!")
    logger.info("=" * 60)
    
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
                settings=http_config,  # This enables the HTTP plugin
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
                logger.info("Check your HTTP server logs to see the events that were sent.")
            else:
                logger.error("❌ Playbook failed!")
                
            return result.status == 'successful'
            
        except Exception as e:
            logger.error(f"Error running playbook: {e}")
            return False

def run_with_environment_variables():
    """
    Alternative method: Configure HTTP plugin using environment variables
    """
    
    logger.info("=" * 60)
    logger.info("RUNNING WITH ENVIRONMENT VARIABLES")
    logger.info("=" * 60)
    
    # Set environment variables for HTTP plugin
    os.environ['RUNNER_HTTP_URL'] = 'http://localhost:8080'
    os.environ['RUNNER_HTTP_PATH'] = '/ansible-events-env'
    
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

if __name__ == '__main__':
    print("\n🚀 Ansible Runner HTTP Plugin Demo")
    print("=" * 50)
    print("\nThis script demonstrates two ways to use the HTTP plugin:")
    print("1. Using runner settings (programmatic configuration)")
    print("2. Using environment variables")
    print("\n⚠️  IMPORTANT: Make sure the HTTP server is running first!")
    print("   Run: python examples/simple_http_server.py")
    print("   (in another terminal)")
    
    choice = input("\nWhich method would you like to try? (1/2): ").strip()
    
    if choice == '1':
        success = run_playbook_with_http_plugin()
    elif choice == '2':
        success = run_with_environment_variables()
    else:
        print("Invalid choice. Defaulting to method 1.")
        success = run_playbook_with_http_plugin()
    
    if success:
        print("\n✅ Demo completed successfully!")
        print("Check the HTTP server terminal to see the events that were received.")
    else:
        print("\n❌ Demo failed. Check the logs above for details.")
    
    sys.exit(0 if success else 1) 