# Ansible Runner HTTP Plugin Examples

This guide will walk you through everything you need to know about using Ansible Runner with the HTTP plugin, including support for both HTTP and Unix socket endpoints.

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

### Step 3: Choose Your Demo Type

You can now try either HTTP or Unix socket communication:

#### Option A: HTTP Server Demo

**Terminal 1 - Start HTTP Server:**
```bash
# Make sure you're in your project directory and virtual environment is active
cd ansible-runner-http
source ansible-runner-env/bin/activate

# Start the HTTP server
python examples/simple_http_server.py
```

**Terminal 2 - Run Ansible with HTTP:**
```bash
# Navigate to your project directory
cd ansible-runner-http

# Activate the virtual environment
source ansible-runner-env/bin/activate

# Run the HTTP demo
python examples/run_ansible_with_http_plugin.py
```

#### Option B: Unix Socket Server Demo

**Terminal 1 - Start Unix Socket Server:**
```bash
# Make sure you're in your project directory and virtual environment is active
cd ansible-runner-http
source ansible-runner-env/bin/activate

# Start the Unix socket server
python examples/simple_unixsocket_server.py
```

**Terminal 2 - Run Ansible with Unix Socket:**
```bash
# Navigate to your project directory
cd ansible-runner-http

# Activate the virtual environment
source ansible-runner-env/bin/activate

# Run the Unix socket demo
python examples/run_ansible_with_unixsocket_plugin.py
```

**Keep Terminal 1 open!** This is your event receiver.

### Step 5: Watch the Magic Happen!

- **Terminal 1** (HTTP Server): Will show real-time events as they happen
- **Terminal 2** (Ansible Runner): Will show the playbook execution

## What Each File Does

### HTTP Examples
- **`examples/simple_http_server.py`**: Creates a web server on port 8080, receives POST requests with Ansible events, displays events in a readable format
- **`examples/run_ansible_with_http_plugin.py`**: Uses ansible-runner to execute the playbook, configures the HTTP plugin to send events over HTTP, shows multiple configuration methods

### Unix Socket Examples  
- **`examples/simple_unixsocket_server.py`**: Creates a Unix socket server at `/tmp/ansible-runner.sock`, receives HTTP requests over Unix socket, displays events in a readable format
- **`examples/run_ansible_with_unixsocket_plugin.py`**: Uses ansible-runner to execute the playbook, configures the HTTP plugin to send events over Unix socket, demonstrates custom socket paths

### Shared
- **`examples/simple_playbook.yml`**: A basic Ansible playbook with several tasks (creates files, shows messages, waits, cleans up) to demonstrate different types of Ansible events

## HTTP vs Unix Socket: Which to Choose?

| Feature              | HTTP                                   | Unix Socket                       |
| -------------------- | -------------------------------------- | --------------------------------- |
| **Network Access**   | ✅ Can receive events from remote hosts | ❌ Local machine only              |
| **Performance**      | Good                                   | ✅ Excellent (no network overhead) |
| **Security**         | Requires network security measures     | ✅ Filesystem-based permissions    |
| **Firewall Issues**  | ❌ May require firewall configuration   | ✅ No network traffic              |
| **Debugging**        | ✅ Easy with curl, Postman, browser     | Moderate (requires special tools) |
| **Docker/Container** | ✅ Works across containers              | ✅ Works with volume mounts        |
| **Load Balancing**   | ✅ Standard HTTP load balancers         | ❌ Not applicable                  |

**Choose HTTP when:**
- You need to receive events from remote machines
- You're integrating with web services (Slack, webhooks, APIs)
- You want to use standard HTTP tools for debugging
- You need to scale horizontally with load balancers

**Choose Unix Socket when:**
- All communication is local to one machine
- You want maximum performance and minimal overhead
- Security is a priority (no network exposure)
- You're avoiding firewall complications
- You're building high-performance local integrations

## Configuration Methods

### HTTP Configuration

**Method 1: Programmatic Configuration**
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

**Method 2: Environment Variables**
```bash
export RUNNER_HTTP_URL="http://localhost:8080"
export RUNNER_HTTP_PATH="/events"
export RUNNER_HTTP_HEADERS='{"Authorization": "Bearer token"}'

# Then run ansible-runner normally - it will pick up the variables
```

### Unix Socket Configuration

**Method 1: Programmatic Configuration**
```python
unixsocket_config = {
    'runner_http_url': '/tmp/ansible-runner.sock',  # Unix socket path
    'runner_http_path': '/ansible-events',          # Optional path
    'runner_http_headers': {'X-Source': 'my-app'}   # Optional headers
}

ansible_runner.run(
    project_dir=project_dir,
    playbook='my_playbook.yml',
    settings=unixsocket_config
)
```

**Method 2: Environment Variables**
```bash
export RUNNER_HTTP_URL="/tmp/ansible-runner.sock"
export RUNNER_HTTP_PATH="/events"

# The plugin automatically detects Unix sockets by checking if the URL is a file path
```

## Real-World Use Cases

### HTTP Use Cases

**1. Monitoring Dashboards**
Send Ansible events to Grafana, Kibana, or custom dashboards:
```python
http_config = {
    'runner_http_url': 'https://my-monitoring.company.com',
    'runner_http_path': '/api/ansible-events',
    'runner_http_headers': {'Authorization': 'Bearer monitoring-token'}
}
```

**2. Slack/Teams Notifications**
Trigger notifications when deployments complete:
```python
http_config = {
    'runner_http_url': 'https://hooks.slack.com/services/...',
    'runner_http_headers': {'Content-Type': 'application/json'}
}
```

**3. CI/CD Integration**
Notify CI/CD systems about deployment status:
```python
http_config = {
    'runner_http_url': 'https://jenkins.company.com/ansible-webhook',
    'runner_http_headers': {'X-API-Key': 'jenkins-api-key'}
}
```

### Unix Socket Use Cases

**1. Local Process Communication**
For local services or when avoiding network overhead:
```python
unixsocket_config = {
    'runner_http_url': '/var/run/monitoring.sock',
    'runner_http_path': '/ansible-events'
}
```

**2. Container-to-Host Communication**
Share sockets between containers and host:
```python
unixsocket_config = {
    'runner_http_url': '/shared/sockets/ansible.sock',
    'runner_http_headers': {'X-Container': 'ansible-runner'}
}
```

**3. Security-Conscious Environments**
When network traffic should be avoided:
```python
unixsocket_config = {
    'runner_http_url': '/tmp/secure-ansible.sock',
    'runner_http_path': '/secure-events'
}
```

**4. High-Performance Logging**
For high-volume event processing with minimal overhead:
```python
unixsocket_config = {
    'runner_http_url': '/var/log/ansible.sock',
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

### HTTP-specific Issues

**"Connection refused" errors**
- Make sure the HTTP server is running first
- Check that you're using the correct port (8080)
- Verify the URL in your configuration

**No events received**
- Verify HTTP server is listening
- Check the URL configuration matches
- Look for error messages in ansible-runner output

### Unix Socket-specific Issues

**"No such file or directory" errors**
- Make sure the Unix socket server is running first
- Check that the socket path exists: `ls -la /tmp/ansible-runner.sock`
- Verify you have permissions to access the socket

**"Permission denied" errors**
- Check socket file permissions: `ls -la /tmp/ansible-runner.sock`
- Ensure the socket directory is writable
- Try using a different socket path (e.g., in your home directory)

**Socket path in use**
- Kill any previous server instances
- Remove the socket file manually: `rm /tmp/ansible-runner.sock`
- Restart the Unix socket server

### General Issues

**"Plugin not found" errors**
- Ensure the HTTP plugin is installed: `pip list | grep ansible-runner-http`
- Check virtual environment is activated
- If using the alternative setup method, verify you copied all example files correctly

**Events not formatted correctly**
- Check that the Content-Type header is set to `application/json`
- Verify the server is receiving valid JSON data

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

