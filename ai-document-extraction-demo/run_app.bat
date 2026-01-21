@echo off
SETLOCAL EnableDelayedExpansion

echo ==========================================
echo   AI Document Extraction Pipeline Launcher
echo ==========================================

:: Step 1: Check and Pull Llama 3 from Ollama
echo.
echo [1/3] Ensuring Llama 3 model is available...
echo Running: ollama pull llama3
ollama pull llama3
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to pull model. Is Ollama running? 
    echo Please start Ollama Desktop first.
    pause
    exit /b %ERRORLEVEL%
)

:: Step 2: Check Virtual Environment
echo.
echo [2/3] Checking virtual environment...
if not exist "venv\Scripts\activate" (
    echo [ERROR] Virtual environment 'venv' not found!
    echo Please run the setup steps in README first.
    pause
    exit /b 1
)

:: Step 3: Run the application
echo.
echo [3/3] Launching Streamlit interface...
echo.
call .\venv\Scripts\activate
streamlit run app.py

pause
