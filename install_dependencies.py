#!/usr/bin/env python3
"""
Script to create a unified virtual environment and install all dependencies.
Solves the macOS "externally managed environment" issue.
"""

import subprocess
import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
VENV_DIR = BASE_DIR / "venv"
REQUIREMENTS_FILE = BASE_DIR / "requirements.txt"

def create_virtual_environment():
    """Create a virtual environment if it doesn't exist"""
    if VENV_DIR.exists():
        print("🔄 Virtual environment already exists. Removing old one...")
        import shutil
        shutil.rmtree(VENV_DIR)
    
    print("🏗️  Creating virtual environment...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "venv", str(VENV_DIR)],
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment:")
        print(f"   Error: {e.stderr}")
        return False

def get_venv_python():
    """Get the path to the Python executable in the virtual environment"""
    if sys.platform == "win32":
        return VENV_DIR / "Scripts" / "python.exe"
    else:
        return VENV_DIR / "bin" / "python"

def get_venv_pip():
    """Get the path to pip in the virtual environment"""
    if sys.platform == "win32":
        return VENV_DIR / "Scripts" / "pip"
    else:
        return VENV_DIR / "bin" / "pip"

def upgrade_pip():
    """Upgrade pip in the virtual environment"""
    print("⬆️  Upgrading pip...")
    try:
        result = subprocess.run(
            [str(get_venv_python()), "-m", "pip", "install", "--upgrade", "pip"],
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ Pip upgraded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Failed to upgrade pip: {e.stderr}")
        return False  # Not critical, continue anyway

def install_dependencies():
    """Install dependencies from requirements.txt"""
    if not REQUIREMENTS_FILE.exists():
        print(f"❌ Requirements file not found: {REQUIREMENTS_FILE}")
        return False
    
    print("📦 Installing dependencies from requirements.txt...")
    print(f"   Using: {REQUIREMENTS_FILE}")
    
    try:
        result = subprocess.run(
            [str(get_venv_python()), "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)],
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies:")
        print(f"   Error: {e.stderr}")
        print(f"   Stdout: {e.stdout}")
        return False

def verify_installation():
    """Verify that key packages are installed"""
    print("🔍 Verifying installation...")
    
    key_packages = ["flask", "dash", "pandas", "plotly", "requests"]
    failed_packages = []
    
    for package in key_packages:
        try:
            result = subprocess.run(
                [str(get_venv_python()), "-c", f"import {package}; print(f'{package} version: {{getattr({package}, '__version__', 'unknown')}}')"],
                check=True,
                capture_output=True,
                text=True
            )
            print(f"   ✅ {result.stdout.strip()}")
        except subprocess.CalledProcessError:
            failed_packages.append(package)
            print(f"   ❌ {package}: Failed to import")
    
    if not failed_packages:
        print("✅ All key packages verified successfully")
        return True
    else:
        print(f"⚠️  Some packages failed verification: {', '.join(failed_packages)}")
        return False

def create_activation_script():
    """Create a simple activation script for convenience"""
    if sys.platform == "win32":
        activate_script = BASE_DIR / "activate_env.bat"
        script_content = f"""@echo off
echo 🐍 Activating Recommender Systems Review virtual environment...
call "{VENV_DIR}\\Scripts\\activate.bat"
echo ✅ Virtual environment activated!
echo 💡 Run: python run_all.py
cmd /k
"""
    else:
        activate_script = BASE_DIR / "activate_env.sh"
        script_content = f"""#!/bin/bash
echo "🐍 Activating Recommender Systems Review virtual environment..."
source "{VENV_DIR}/bin/activate"
echo "✅ Virtual environment activated!"
echo "💡 Run: python run_all.py"
bash
"""
    
    with open(activate_script, 'w') as f:
        f.write(script_content)
    
    if sys.platform != "win32":
        os.chmod(activate_script, 0o755)
    
    print(f"📝 Created activation script: {activate_script}")

def main():
    """Main function to set up the unified environment"""
    print("🏗️  Recommender Systems Review - Unified Environment Setup")
    print("=" * 70)
    print("🔧 This will create a single virtual environment for all applications")
    print("💡 This solves the macOS 'externally managed environment' issue")
    print("=" * 70)
    
    steps = [
        ("Create Virtual Environment", create_virtual_environment),
        ("Upgrade Pip", upgrade_pip),
        ("Install Dependencies", install_dependencies),
        ("Verify Installation", verify_installation),
        ("Create Activation Script", create_activation_script)
    ]
    
    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        if not step_func():
            if step_name != "Upgrade Pip":  # Pip upgrade failure is not critical
                print(f"❌ Setup failed at: {step_name}")
                return
        print()
    
    print("=" * 70)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("   1. Run: python run_all.py")
    print("   2. Open: http://localhost:3000")
    print(f"\n💡 Virtual environment location: {VENV_DIR}")
    print(f"📁 All dependencies are installed in this isolated environment")
    print("=" * 70)

if __name__ == "__main__":
    main()