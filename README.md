# Ansible Runner HTTP Plugin Example

This guide will walk you through everything you need to know about using Ansible Runner with the HTTP plugin.

## Quick Start

### Option 1: Easy Setup (Recommended)

Clone this repository and run the automated setup:

```bash
# Clone the repository
git clone https://github.com/chiragkyal/ansible-runner-http.git
cd ansible-runner-http

# Run the setup (works on Mac and Linux)
python3 setup_demo.py
```

The script will:
- ✅ Create a demo directory
- ✅ Set up a virtual environment  
- ✅ Install all required packages from PyPI
- ✅ Copy example files from the repository
- ✅ Verify everything works
- ✅ Show you exactly what to do next

Follow the instructions the script gives you.

---

### Option 2: Manual Setup
If you prefer using a requirements file:

```bash
# Clone this repository
git clone https://github.com/chiragkyal/ansible-runner-http.git
cd ansible-runner-http

# Create a virtual environment
python3 -m venv ansible-runner-env

# Activate the virtual environment
source ansible-runner-env/bin/activate

# Install packages
pip install -r requirements.txt

# Make the Python files executable
chmod +x examples/*.py
```

### Step 2: Understanding the Components

**Ansible Runner**: A Python library that runs Ansible playbooks programmatically
**HTTP Plugin**: Sends real-time events from Ansible runs to HTTP endpoints
**Playbook**: A YAML file containing automation tasks

### Step 3: Start the HTTP Server (Terminal 1)

This server will receive and display events from Ansible:

```bash
# Make sure you're in your project directory and virtual environment is active
cd ansible-runner-http
source ansible-runner-env/bin/activate

# Start the HTTP server
python examples/simple_http_server.py
```

You should see:
```
INFO:__main__:Starting HTTP server on port 8080
INFO:__main__:This server will receive Ansible events from the HTTP plugin
INFO:__main__:Press Ctrl+C to stop the server
```

**Keep this terminal open!** This is your event receiver.

### Step 4: Run the Ansible Demo (Terminal 2)

Open a new terminal and run:

```bash
# Navigate to your project directory
cd ansible-runner-http

# Activate the virtual environment
source ansible-runner-env/bin/activate

# Run the demo
python examples/run_ansible_with_http_plugin.py
```

### Step 5: Watch the Magic Happen!

- **Terminal 1** (HTTP Server): Will show real-time events as they happen
- **Terminal 2** (Ansible Runner): Will show the playbook execution

## What Each File Does

### `examples/simple_http_server.py`
- Creates a web server on port 8080
- Receives POST requests with Ansible events
- Displays events in a readable format
- **Purpose**: Simulates an external system that monitors Ansible

### `examples/simple_playbook.yml`
- A basic Ansible playbook with several tasks
- Creates files, shows messages, waits, cleans up
- **Purpose**: Demonstrates different types of Ansible events

### `examples/run_ansible_with_http_plugin.py`
- Uses ansible-runner to execute the playbook
- Configures the HTTP plugin to send events
- Shows two configuration methods
- **Purpose**: The main integration example

## Configuration Methods

### Method 1: Programmatic Configuration
```python
http_config = {
    'runner_http_url': 'http://localhost:8080',
    'runner_http_path': '/ansible-events',
    'runner_http_headers': {'X-Source': 'my-app'}
}

ansible_runner.run(
    project_dir=project_dir,
    playbook='my_playbook.yml',
    settings=http_config  # Pass configuration here
)
```

### Method 2: Environment Variables
```bash
export RUNNER_HTTP_URL="http://localhost:8080"
export RUNNER_HTTP_PATH="/events"
export RUNNER_HTTP_HEADERS='{"Authorization": "Bearer token"}'

# Then run ansible-runner normally - it will pick up the variables
```

## Real-World Use Cases

### 1. Monitoring Dashboards
Send Ansible events to Grafana, Kibana, or custom dashboards:
```python
http_config = {
    'runner_http_url': 'https://my-monitoring.company.com',
    'runner_http_path': '/api/ansible-events',
    'runner_http_headers': {'Authorization': 'Bearer monitoring-token'}
}
```

### 2. Slack/Teams Notifications
Trigger notifications when deployments complete:
```python
http_config = {
    'runner_http_url': 'https://hooks.slack.com/services/...',
    'runner_http_headers': {'Content-Type': 'application/json'}
}
```

### 3. CI/CD Integration
Notify CI/CD systems about deployment status:
```python
http_config = {
    'runner_http_url': 'https://jenkins.company.com/ansible-webhook',
    'runner_http_headers': {'X-API-Key': 'jenkins-api-key'}
}
```

### 4. Audit Logging
Send detailed event logs to centralized logging:
```python
http_config = {
    'runner_http_url': 'https://logging.company.com',
    'runner_http_path': '/api/logs/ansible',
    'runner_http_headers': {'X-Source': 'production-ansible'}
}
```

## Event Types You'll See

The HTTP plugin sends various event types:

- **playbook_on_start**: Playbook begins
- **playbook_on_task_start**: Each task starts
- **runner_on_ok**: Task completes successfully
- **runner_on_failed**: Task fails
- **playbook_on_stats**: Final statistics
- **And many more...**

Each event contains rich metadata like timestamps, task details, and results.

## Verify Your Installation

Before running the examples, verify everything is installed correctly:

```bash
# Activate your virtual environment
source ansible-runner-env/bin/activate

# Check that all packages are installed
pip list | grep -E "(ansible|requests)"

# Should show something like:
# ansible-core          2.15.13
# ansible-runner        2.4.1  
# ansible-runner-http   1.0.0
# requests              2.32.4
# requests-unixsocket   0.4.1

# Test imports
python -c "import ansible_runner; print('✅ ansible-runner works')"
python -c "import ansible_runner_http; print('✅ HTTP plugin works')"
```

If all tests pass, you're ready to run the examples!

## Troubleshooting

### "Connection refused" errors
- Make sure the HTTP server is running first
- Check that you're using the correct port (8080)
- Verify the URL in your configuration

### "Plugin not found" errors
- Ensure the HTTP plugin is installed: `pip list | grep ansible-runner-http`
- Check virtual environment is activated
- If using the alternative setup method, verify you copied all example files correctly

### No events received
- Verify HTTP server is listening
- Check the URL configuration matches
- Look for error messages in ansible-runner output

## Understanding the Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Your Python   │    │  Ansible Runner  │    │   HTTP Plugin   │
│     Script      │───▶│    (Executor)    │───▶│   (Notifier)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                                ┌─────────────────┐
                                                │   HTTP Server   │
                                                │ (Event Receiver)│
                                                └─────────────────┘
```

