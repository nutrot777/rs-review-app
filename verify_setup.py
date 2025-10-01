#!/usr/bin/env python3
"""
Quick setup verification script to ensure everything is properly configured.
"""

import sys
import subprocess
from pathlib import Path
import importlib.util

BASE_DIR = Path(__file__).parent

def check_python_version():
    """Check if Python version is suitable"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.8+")
        return False

def check_directory_structure():
    """Check if all required directories exist"""
    required_dirs = [
        "frontend",
        "backend",
        "backend/allothers",
        "backend/interactiveApp",
        "backend/interactiveApp2", 
        "backend/segmentcountry",
        "backend/segmentyear",
        "backend/continentsCountries",
        "scripts"
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        full_path = BASE_DIR / dir_path
        if not full_path.exists():
            missing_dirs.append(dir_path)
    
    if not missing_dirs:
        print("✅ Directory structure - OK")
        return True
    else:
        print("❌ Missing directories:")
        for dir_path in missing_dirs:
            print(f"   • {dir_path}")
        return False

def check_required_files():
    """Check if all required files exist"""
    required_files = [
        "run_all.py",
        "install_dependencies.py",
        "frontend/homepage.html",
        "backend/allothers/app.py",
        "backend/interactiveApp/app.py",
        "backend/interactiveApp2/app.py",
        "backend/segmentcountry/app.py",
        "backend/segmentyear/app.py",
        "backend/continentsCountries/app.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = BASE_DIR / file_path
        if not full_path.exists():
            missing_files.append(file_path)
    
    if not missing_files:
        print("✅ Required files - OK")
        return True
    else:
        print("❌ Missing files:")
        for file_path in missing_files:
            print(f"   • {file_path}")
        return False

def check_virtual_environment():
    """Check if virtual environment exists"""
    venv_dir = BASE_DIR / "venv"
    if sys.platform == "win32":
        venv_python = venv_dir / "Scripts" / "python.exe"
    else:
        venv_python = venv_dir / "bin" / "python"
    
    if venv_python.exists():
        print("✅ Virtual environment - OK")
        return True
    else:
        print("❌ Virtual environment not found")
        print("   Run: python install_dependencies.py")
        return False

def check_key_dependencies():
    """Check if key Python packages are available in virtual environment"""
    venv_dir = BASE_DIR / "venv"
    if sys.platform == "win32":
        venv_python = venv_dir / "Scripts" / "python.exe"
    else:
        venv_python = venv_dir / "bin" / "python"
    
    if not venv_python.exists():
        print("❌ Virtual environment not found")
        print("   Run: python install_dependencies.py")
        return False
    
    key_packages = [
        "flask",
        "dash", 
        "pandas",
        "plotly",
        "requests"
    ]
    
    missing_packages = []
    for package in key_packages:
        try:
            result = subprocess.run(
                [str(venv_python), "-c", f"import {package}"],
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError:
            missing_packages.append(package)
    
    if not missing_packages:
        print("✅ Key dependencies in virtual environment - OK")
        return True
    else:
        print("❌ Missing key packages in virtual environment:")
        for package in missing_packages:
            print(f"   • {package}")
        print("   Run: python install_dependencies.py")
        return False

def check_port_availability():
    """Check if required ports are available"""
    import socket
    
    required_ports = [3000, 8080, 8081, 8082, 8083, 8084, 8085]
    occupied_ports = []
    
    for port in required_ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex(('localhost', port))
            if result == 0:
                occupied_ports.append(port)
    
    if not occupied_ports:
        print("✅ Required ports available - OK")
        return True
    else:
        print("⚠️  Some ports are occupied:")
        for port in occupied_ports:
            print(f"   • Port {port}")
        print("   This may cause conflicts when running applications")
        return False

def main():
    """Main verification function"""
    print("🔍 Recommender Systems Review - Setup Verification")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Directory Structure", check_directory_structure),
        ("Required Files", check_required_files),
        ("Virtual Environment", check_virtual_environment),
        ("Key Dependencies", check_key_dependencies),
        ("Port Availability", check_port_availability)
    ]
    
    passed_checks = 0
    total_checks = len(checks)
    
    for check_name, check_func in checks:
        print(f"\n🔎 Checking {check_name}...")
        if check_func():
            passed_checks += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Verification Results: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("🎉 Setup verification complete! Ready to run applications.")
        print("💡 Next step: python run_all.py")
    else:
        print("⚠️  Some issues found. Please address them before running applications.")
        if passed_checks >= total_checks - 1:
            print("💡 Most checks passed. You can probably still run the applications.")

if __name__ == "__main__":
    main()