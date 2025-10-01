#!/usr/bin/env python3
"""
Master script to run all Flask/Dash applications for the Recommender Systems Review project.
Consolidated structure version.
"""

import subprocess
import os
import sys
import time
import signal
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Define all applications with their paths and assigned ports
APPS = {
    "homepage": {
        "path": BASE_DIR / "frontend",
        "port": 3000,
        "type": "static",
        "description": "Main homepage with static HTML files"
    },
    "allothers": {
        "path": BASE_DIR / "backend" / "allothers",
        "port": 8080,
        "type": "flask",
        "description": "Flask app for themes and references"
    },
    "interactiveApp": {
        "path": BASE_DIR / "backend" / "interactiveApp",
        "port": 8081,
        "type": "dash",
        "description": "Sunburst chart: Years & Countries"
    },
    "interactiveApp2": {
        "path": BASE_DIR / "backend" / "interactiveApp2",
        "port": 8082,
        "type": "dash",
        "description": "Sunburst chart: Years, Segments & Countries"
    },
    "segmentcountry": {
        "path": BASE_DIR / "backend" / "segmentcountry",
        "port": 8083,
        "type": "dash",
        "description": "Treemap: Segments & Countries"
    },
    "segmentyear": {
        "path": BASE_DIR / "backend" / "segmentyear",
        "port": 8084,
        "type": "dash",
        "description": "Stacked chart: Years & Segments"
    },
    "continentsCountries": {
        "path": BASE_DIR / "backend" / "continentsCountries",
        "port": 8085,
        "type": "dash",
        "description": "Interactive chart for continents and countries"
    }
}

# Store process references
processes = []

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print(f"\n🛑 Received signal {sig}. Shutting down all applications...")
    for name, process in processes:
        if process.poll() is None:  # Process is still running
            print(f"   Terminating {name}...")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print(f"   Force killing {name}...")
                process.kill()
    
    print("✅ All applications stopped.")
    sys.exit(0)

def create_homepage_server():
    """Create a simple HTTP server for static HTML files"""
    server_code = '''
import http.server
import socketserver
import os
from pathlib import Path

PORT = 3000
DIRECTORY = Path(__file__).parent

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def do_GET(self):
        # If requesting root path, serve homepage.html
        if self.path == '/' or self.path == '':
            self.path = '/homepage.html'
        super().do_GET()
    
    def end_headers(self):
        # Add CORS headers to allow iframe embedding
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🏠 Homepage server running at http://localhost:{PORT}")
        print(f"📁 Serving files from: {DIRECTORY}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\\n🛑 Homepage server stopped.")
'''
    
    server_path = APPS["homepage"]["path"] / "server.py"
    with open(server_path, 'w') as f:
        f.write(server_code)
    
    return server_path

def check_dependencies(app_path):
    """Check if dependencies are installed"""
    requirements_file = app_path / "requirements.txt"
    if requirements_file.exists():
        print(f"   📦 Found requirements.txt")
        return True
    return False

def get_venv_python():
    """Get the path to the Python executable in the virtual environment"""
    venv_dir = BASE_DIR / "venv"
    if sys.platform == "win32":
        return venv_dir / "Scripts" / "python.exe"
    else:
        return venv_dir / "bin" / "python"

def check_virtual_environment():
    """Check if virtual environment exists and is set up"""
    venv_python = get_venv_python()
    if not venv_python.exists():
        print("❌ Virtual environment not found!")
        print("💡 Please run: python install_dependencies.py")
        return False
    return True

def run_app(name, config):
    """Run a single application"""
    app_path = config["path"]
    port = config["port"]
    app_type = config["type"]
    
    if not app_path.exists():
        print(f"❌ Path does not exist: {app_path}")
        return None
    
    # Check dependencies for backend apps
    if app_type != "static":
        check_dependencies(app_path)
    
    # Set environment variable for port
    env = os.environ.copy()
    env["PORT"] = str(port)
    
    # Use virtual environment Python
    venv_python = get_venv_python()
    
    if app_type == "static":
        # Create and run the homepage server
        server_path = create_homepage_server()
        cmd = [str(venv_python), str(server_path)]
        cwd = app_path
    else:
        # Run Flask/Dash app with virtual environment Python
        app_file = app_path / "app.py"
        if not app_file.exists():
            print(f"❌ app.py not found in: {app_path}")
            return None
        cmd = [str(venv_python), "app.py"]
        cwd = app_path
    
    try:
        print(f"🚀 Starting {name} on port {port}...")
        print(f"   📄 {config['description']}")
        print(f"   📁 Working directory: {cwd}")
        print(f"   🌐 URL: http://localhost:{port}")
        
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        return process
        
    except Exception as e:
        print(f"❌ Failed to start {name}: {e}")
        return None

def check_ports():
    """Check if any required ports are already in use"""
    import socket
    
    print("🔍 Checking port availability...")
    occupied_ports = []
    
    for name, config in APPS.items():
        port = config["port"]
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex(('localhost', port))
            if result == 0:
                occupied_ports.append((name, port))
    
    if occupied_ports:
        print("⚠️  Warning: The following ports are already in use:")
        for name, port in occupied_ports:
            print(f"   • {name}: port {port}")
        print("   You may need to stop other services or change ports.")
        return False
    else:
        print("✅ All required ports are available.")
        return True

def main():
    """Main function to start all applications"""
    print("🔥 Recommender Systems Review - Local Development Environment")
    print("🏗️  Consolidated Structure Version")
    print("=" * 80)
    
    # Check if virtual environment is set up
    if not check_virtual_environment():
        return
    
    # Check port availability
    check_ports()
    print()
    
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start all applications
    for name, config in APPS.items():
        process = run_app(name, config)
        if process:
            processes.append((name, process))
        time.sleep(2)  # Small delay between starts
    
    if not processes:
        print("❌ No applications started successfully!")
        return
    
    print("\n" + "=" * 80)
    print("✅ All applications started successfully!")
    print("\n📋 Application URLs:")
    for name, config in APPS.items():
        if any(proc_name == name for proc_name, _ in processes):
            print(f"   • {name:20} → 🌐 http://localhost:{config['port']:4} - {config['description']}")
    
    print(f"\n🏠 Main Homepage: http://localhost:{APPS['homepage']['port']}")
    print("💡 Press Ctrl+C to stop all applications")
    print("=" * 80)
    
    # Keep the main process alive and monitor subprocesses
    try:
        while True:
            time.sleep(1)
            # Check if any processes have died
            active_processes = []
            for name, process in processes:
                if process.poll() is None:
                    active_processes.append((name, process))
                else:
                    print(f"⚠️  Process {name} has stopped unexpectedly")
            
            processes[:] = active_processes
            
            if not processes:
                print("🛑 All processes have stopped. Exiting...")
                break
                
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    main()