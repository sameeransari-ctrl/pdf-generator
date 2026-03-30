#!/usr/bin/env python3
"""
Western Air Compliance - Desktop PDF Application Setup
Run this script to set up the desktop application
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("ERROR: Python 3.8 or higher is required.")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"Python {version.major}.{version.minor}.{version.micro} detected - OK!")
    return True

def install_dependencies():
    """Install required packages"""
    print("\nInstalling required dependencies...")
    print("-" * 50)

    requirements = [
        "reportlab>=4.0.0",
        "pypdf>=4.0.0",
        "python-docx>=1.1.0",
        "Pillow>=10.0.0"
    ]

    if sys.platform.startswith("win"):
        requirements.append("comtypes>=1.4.0")

    for package in requirements:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"  ✓ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Failed to install {package}")
            return False

    return True

def verify_installation():
    """Verify all dependencies are installed"""
    print("\nVerifying installation...")
    print("-" * 50)

    try:
        import tkinter
        print("✓ tkinter (built-in GUI library)")
    except ImportError:
        print("✗ tkinter not found - this is unusual for Python installations")
        return False

    try:
        import pypdf
        print("✓ pypdf (PDF manipulation)")
    except ImportError:
        print("✗ pypdf not found")
        return False

    try:
        import reportlab
        print("✓ reportlab (PDF generation)")
    except ImportError:
        print("✗ reportlab not found")
        return False

    try:
        import docx
        print("✓ python-docx (Word template support)")
    except ImportError:
        print("✗ python-docx not found")
        return False

    try:
        from PIL import Image
        print("✓ Pillow (Image handling)")
    except ImportError:
        print("✗ Pillow not found")
        return False

    if sys.platform.startswith("win"):
        try:
            import comtypes  # noqa: F401
            print("✓ comtypes (Microsoft Word PDF conversion)")
        except ImportError:
            print("✗ comtypes not found")
            return False

    return True

def create_launcher():
    """Create desktop shortcut or launcher script"""
    print("\nCreating launcher...")
    print("-" * 50)

    # Windows batch file already exists
    if os.path.exists("run_app.bat"):
        print("✓ Windows launcher (run_app.bat) exists")

    # Create shell script for Mac/Linux
    shell_script = """#!/bin/bash
# Western Air Compliance - Desktop PDF Application Launcher

cd "$(dirname "$0")"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed."
    echo "Please install Python 3.8 or higher."
    exit 1
fi

# Check dependencies
python3 -c "import tkinter, pypdf, reportlab" 2>/dev/null || {
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
}

# Launch application
python3 desktop_pdf_app.py
"""

    with open("run_app.sh", "w") as f:
        f.write(shell_script)

    # Make executable on Unix systems
    try:
        os.chmod("run_app.sh", 0o755)
        print("✓ Unix/Mac launcher (run_app.sh) created")
    except:
        print("✓ Unix/Mac launcher script created (may need chmod +x on Mac/Linux)")

def main():
    """Main setup function"""
    print("=" * 50)
    print("Western Air Compliance")
    print("Desktop PDF Application Setup")
    print("=" * 50)
    print()

    # Check Python version
    if not check_python_version():
        input("\nPress Enter to exit...")
        sys.exit(1)

    # Install dependencies
    if not install_dependencies():
        print("\nFailed to install dependencies. Please check your internet connection.")
        input("Press Enter to exit...")
        sys.exit(1)

    # Verify installation
    if not verify_installation():
        print("\nSome components failed to install correctly.")
        input("Press Enter to exit...")
        sys.exit(1)

    # Create launcher
    create_launcher()

    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("=" * 50)
    print()
    print("To run the application:")
    print("  Windows: Double-click 'run_app.bat'")
    print("  Mac/Linux: Run './run_app.sh' in terminal")
    print("  Or run: python desktop_pdf_app.py")
    print()
    print("Features:")
    print("  ✓ Works completely offline")
    print("  ✓ Generates filled PDF reports locally")
    print("  ✓ Automatic ±3% tolerance calculator")
    print("  ✓ Both Safety Valve and Pressure Vessel reports")
    print()

    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
