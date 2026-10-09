@echo off
echo ============================================
echo   NutriGuide - AI Nutrition Agent
echo ============================================
echo.

echo [1/2] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo [2/2] Starting NutriGuide...
echo.
echo Open your browser at: http://localhost:8501
echo Press Ctrl+C to stop the server.
echo.
streamlit run app.py

pause
