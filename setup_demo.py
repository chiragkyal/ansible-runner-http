#!/usr/bin/env python3
"""
Ansible Runner HTTP Plugin Demo Setup Script

This script will set up everything you need to try the Ansible Runner HTTP plugin
on Mac and Linux systems.

Usage: 
1. Clone the repository: git clone https://github.com/chiragkyal/ansible-runner-http.git
2. cd ansible-runner-http
3. python3 setup_demo.py
"""

import os
import sys
import subprocess
import platform

def run_command(cmd, shell=False):
    """Run a command and return success/failure"""
    try:
        if shell:
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        else:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr



def main():
    print("🚀 Ansible Runner HTTP Plugin Demo Setup")
    print("=" * 50)
    
    # Detect platform
    system = platform.system()
    print(f"Detected platform: {system}")
    
    # Create demo directory
    demo_dir = "ansible-runner-demo"
    if os.path.exists(demo_dir):
        print(f"⚠️  Directory {demo_dir} already exists")
        response = input("Do you want to continue anyway? (y/n): ").lower()
        if response != 'y':
            print("Setup cancelled.")
            return
    else:
        os.makedirs(demo_dir)
        print(f"✅ Created directory: {demo_dir}")
    
    os.chdir(demo_dir)
    
    # Create virtual environment
    print("\n📦 Setting up virtual environment...")
    venv_cmd = [sys.executable, "-m", "venv", "ansible-runner-env"]
    success, output = run_command(venv_cmd)
    
    if not success:
        print(f"❌ Failed to create virtual environment: {output}")
        return
    
    print("✅ Virtual environment created")
    
    # Set paths for Unix-like systems (Mac/Linux)
    activate_script = os.path.join("ansible-runner-env", "bin", "activate")
    pip_path = os.path.join("ansible-runner-env", "bin", "pip")
    python_path = os.path.join("ansible-runner-env", "bin", "python")
    
    # Install packages
    print("\n📥 Installing required packages...")
    packages = [
        "ansible-core>=2.12.0",
        "ansible-runner>=2.0.0",
        "ansible-runner-http>=1.0.0",
        "requests>=2.25.0",
        "requests-unixsocket>=0.3.0"
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        success, output = run_command([pip_path, "install", package])
        if not success:
            print(f"❌ Failed to install {package}: {output}")
            return
    
    print("✅ All packages installed successfully")
    
    # Copy example files from the repository
    print("\n📁 Copying example files from repository...")
    
    # Get the script's directory (should be in the repo root)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    examples_dir = os.path.join(script_dir, "examples")
    
    files = [
        "simple_http_server.py",
        "simple_unixsocket_server.py",
        "simple_playbook.yml", 
        "run_ansible_with_http_plugin.py",
        "run_ansible_with_unixsocket_plugin.py"
    ]
    
    copy_success = True
    if not os.path.exists(examples_dir):
        print(f"❌ Examples directory not found: {examples_dir}")
        print("   Make sure you're running this script from the repository root")
        copy_success = False
    else:
        import shutil
        for filename in files:
            src_path = os.path.join(examples_dir, filename)
            dst_path = filename
            
            if os.path.exists(src_path):
                print(f"Copying {filename}...")
                shutil.copy2(src_path, dst_path)
            else:
                print(f"❌ File not found: {src_path}")
                copy_success = False
                break
    
    if copy_success:
        print("✅ Example files copied successfully")
    else:
        print("⚠️  Could not copy example files")
        print("📝 Make sure you're running this script from the repository root")
        print("   where the examples/ directory exists")
    
    # Create requirements.txt for reference
    with open("requirements.txt", "w") as f:
        for package in packages:
            f.write(package + "\n")
    
    print("✅ Created requirements.txt")
    
    # Make files executable (only if copied successfully)
    if copy_success:
        for filename in files:
            if filename.endswith(".py") and os.path.exists(filename):
                os.chmod(filename, 0o755)
        print("✅ Made Python files executable")
    
    # Verify installation
    print("\n🔍 Verifying installation...")
    test_commands = [
        [python_path, "-c", "import ansible_runner; print('ansible-runner works')"],
        [python_path, "-c", "import ansible_runner_http; print('HTTP plugin works')"]
    ]
    
    for cmd in test_commands:
        success, output = run_command(cmd)
        if success:
            print(f"✅ {output.strip()}")
        else:
            print(f"❌ Test failed: {output}")
            return
    
    # Final instructions
    print("\n🎉 Setup Complete!")
    print("=" * 50)
    print("\n📋 Next Steps:")
    print("1. Open TWO terminal windows")
    print(f"2. In both terminals, navigate to: {os.getcwd()}")
    print("3. In both terminals, activate the environment:")
    print("   source ansible-runner-env/bin/activate")
    
    if copy_success:
        print("\n4. Choose your demo type:")
        print("\n   🌐 HTTP DEMO:")
        print("   Terminal 1: python simple_http_server.py")
        print("   Terminal 2: python run_ansible_with_http_plugin.py")
        print("\n   🔌 UNIX SOCKET DEMO:")
        print("   Terminal 1: python simple_unixsocket_server.py")
        print("   Terminal 2: python run_ansible_with_unixsocket_plugin.py")
        print("\n5. Watch the events flow from Terminal 2 to Terminal 1!")
    else:
        print("\n4. First, fix the file copying issue:")
        print("   Make sure you're running this script from the repository root")
        print("   where the examples/ directory exists")
        print("\n5. Then run the demos as described in the README")
    
    print(f"\n📂 All files are in: {os.getcwd()}")
    print("\nHappy automating! 🚀")

if __name__ == "__main__":
    main() 