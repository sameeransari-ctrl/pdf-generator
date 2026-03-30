#!/bin/bash
# Western Air Compliance - Desktop PDF Application Launcher
# For Mac and Linux systems

cd "$(dirname "$0")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Western Air Compliance PDF Report Generator"
echo "Desktop Application Launcher"
echo "=========================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo -e "${RED}ERROR: Python 3 is not installed.${NC}"
        echo "Please install Python 3.8 or higher from https://python.org"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo -e "${GREEN}Python found: $($PYTHON_CMD --version)${NC}"

# Check if dependencies are installed
echo "Checking dependencies..."
$PYTHON_CMD -c "import tkinter, pypdf, reportlab" 2>/dev/null

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Installing required dependencies...${NC}"
    $PYTHON_CMD -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}ERROR: Failed to install dependencies.${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}Dependencies OK...${NC}"
echo ""
echo "Starting Desktop PDF Application..."
echo ""

# Launch the application
$PYTHON_CMD desktop_pdf_app.py

if [ $? -ne 0 ]; then
    echo -e "${RED}Application exited with an error.${NC}"
    read -p "Press Enter to continue..."
fi
