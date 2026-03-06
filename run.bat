@echo off
TITLE AI Interview Coach
COLOR 0A

echo ========================================
echo    🎯 AI INTERVIEW COACH LAUNCHER
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✅ Python is installed
echo.

:: Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment exists
)
echo.

:: Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment activated
echo.

:: Upgrade pip
echo 📦 Upgrading pip...
python -m pip install --upgrade pip >nul
echo ✅ Pip upgraded
echo.

:: Install requirements
echo 📦 Installing requirements (this may take a few minutes)...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install requirements
    echo.
    echo Trying to install packages one by one...
    
    pip install streamlit
    pip install openai
    pip install python-dotenv
    pip install pandas
    pip install plotly
    pip install numpy
    pip install speechrecognition
    pip install pyttsx3
    pip install google-generativeai
    
    echo ✅ Packages installed
) else (
    echo ✅ Requirements installed successfully
)
echo.

:: Check if .env file exists
if not exist ".env" (
    echo ⚠️ .env file not found. Creating template...
    echo OPENAI_API_KEY=your_api_key_here > .env
    echo GOOGLE_API_KEY=your_google_api_key_here >> .env
    echo ✅ .env template created
    echo.
    echo ⚠️ Please edit the .env file and add your API keys
    echo   Press any key to continue...
    pause >nul
)

:: Clear screen before running
cls

:: Display startup message
echo ========================================
echo    🚀 STARTING AI INTERVIEW COACH
echo ========================================
echo.
echo 📊 Your personal AI interview trainer
echo 💡 Get instant feedback on your answers
echo 📈 Track your progress over time
echo.
echo Opening browser at: http://localhost:8501
echo.
echo ========================================
echo Press Ctrl+C to stop the application
echo ========================================
echo.

:: Run the Streamlit app
streamlit run app.py

:: If streamlit fails, try alternative
if errorlevel 1 (
    echo.
    echo ❌ Failed to start with streamlit command
    echo Trying alternative method...
    python -m streamlit run app.py
)

:: Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ❌ Failed to start the application
    echo.
    echo Possible issues:
    echo 1. Make sure app.py exists in current folder
    echo 2. Check if all packages installed correctly
    echo 3. Try running manually: streamlit run app.py
    pause
)

:: Deactivate virtual environment when done
deactivate