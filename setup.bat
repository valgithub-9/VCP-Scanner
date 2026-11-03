@echo off
REM VCP Scanner with AI Finance Agent - Windows Setup Script

echo ======================================
echo ^^ VCP Scanner AI Finance Agent Setup
echo ======================================
echo.

REM Check Python version
echo ^^ Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo ^×^ Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org
    exit /b 1
)

python --version
echo.

REM Create virtual environment
if not exist "venv" (
    echo ^^ Creating virtual environment...
    python -m venv venv
) else (
    echo ^^ Virtual environment already exists
)

echo.
echo ^^ Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo ^^ Upgrading pip...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1

REM Install requirements
echo ^^ Installing dependencies...
pip install -r requirements.txt

REM Create .env file
echo.
if not exist ".env" (
    echo ^^ Creating .env file from template...
    copy .env.example .env >nul
    echo   Please edit .env and add your ANTHROPIC_API_KEY
) else (
    echo ^^ .env file already exists
)

REM Create .gitignore
if not exist ".gitignore" (
    echo ^^ Creating .gitignore...
    (
        echo .env
        echo __pycache__/
        echo *.pyc
        echo *.pyo
        echo *.egg-info/
        echo venv/
        echo .vscode/
        echo .DS_Store
        echo vcp_scan_*.csv
        echo *.log
    ) > .gitignore
)

REM Verify installation
echo.
echo ^^ Verifying installation...

python -c "import yfinance; import pandas; import numpy" >nul 2>&1
if errorlevel 0 (
    echo   ^v Core dependencies verified
)

python -c "import anthropic" >nul 2>&1
if errorlevel 0 (
    echo   ^v Anthropic SDK verified
)

REM Final summary
echo.
echo ======================================
echo ^v Setup Complete!
echo ======================================
echo.
echo Next steps:
echo 1. Edit .env file and add your ANTHROPIC_API_KEY:
echo    notepad .env
echo.
echo 2. Get your API key from:
echo    https://console.anthropic.com/account/keys
echo.
echo 3. Run the VCP Scanner:
echo    python vcp_scanner.py
echo.
echo 4. Run the AI Finance Agent:
echo    python ai_finance_agent.py
echo.
echo For more help, see INSTALL.md
echo.
pause
