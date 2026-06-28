#!/bin/bash
echo "========================================="
echo "       Super Mario AI Visualizer "
echo "========================================="

# 1. Find Python
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
elif command -v python &>/dev/null; then
    PYTHON_CMD=python
else
    echo "[X] ERROR: Python not found!"
    echo "Please install Python 3 from https://www.python.org/downloads/"
    exit 1
fi

echo "[i] Using Python: $PYTHON_CMD"

# 2. Create virtual environment
if [ ! -d "venv" ]; then
    echo "[i] Creating virtual environment (venv)..."
    $PYTHON_CMD -m venv venv
fi

# 3. Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "[X] ERROR: Virtual environment activation script not found."
    echo "Please delete the 'venv' directory and run this script again."
    exit 1
fi

# 4. Install dependencies
echo "[i] Installing required packages from requirements.txt..."
export PYTHONHTTPSVERIFY=0
pip install --upgrade pip >/dev/null 2>&1
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
export PYTHONHTTPSVERIFY=1

# 5. Run the game
echo ""
echo "[i] Starting game..."
python main.py
