@echo off
REM Gmail API Setup Helper Script for Windows
REM This script guides you through setting up Gmail API credentials

echo ============================================================
echo Gmail API Setup Helper
echo ============================================================
echo.

REM Check if credentials directory exists
set CREDS_DIR=credentials
set CREDS_FILE=%CREDS_DIR%\gmail_credentials.json

if not exist "%CREDS_DIR%" (
    echo Creating credentials directory...
    mkdir "%CREDS_DIR%"
)

REM Check if credentials file exists
if exist "%CREDS_FILE%" (
    echo [32m✓[0m Credentials file found: %CREDS_FILE%
    echo.
    echo Testing credentials...
    python test_gmail_credentials.py
) else (
    echo [31m✗[0m Credentials file not found: %CREDS_FILE%
    echo.
    echo ============================================================
    echo SETUP INSTRUCTIONS
    echo ============================================================
    echo.
    echo Step 1: Go to Google Cloud Console
    echo   -^> https://console.cloud.google.com/
    echo.
    echo Step 2: Create a new project
    echo   -^> Click 'Select a project' -^> 'New Project'
    echo   -^> Name: 'AI-Employee-Gmail'
    echo   -^> Click 'Create'
    echo.
    echo Step 3: Enable Gmail API
    echo   -^> Search for 'Gmail API'
    echo   -^> Click 'Enable'
    echo.
    echo Step 4: Create OAuth Credentials
    echo   -^> Go to 'APIs ^& Services' -^> 'Credentials'
    echo   -^> Click 'Create Credentials' -^> 'OAuth client ID'
    echo   -^> Configure consent screen if prompted:
    echo     * User Type: External
    echo     * App name: AI Employee
    echo     * Add your email as test user
    echo   -^> Application type: Desktop app
    echo   -^> Name: AI Employee Desktop
    echo   -^> Click 'Create'
    echo.
    echo Step 5: Download credentials
    echo   -^> Click 'Download JSON'
    echo   -^> Save the file as:
    echo     %CD%\%CREDS_FILE%
    echo.
    echo Step 6: Run this script again
    echo   -^> setup_gmail.bat
    echo.
    echo ============================================================
    echo.
    echo For detailed instructions, see: credentials\README.md
    echo.
    echo Opening Google Cloud Console in your browser...
    timeout /t 3 /nobreak >nul
    start https://console.cloud.google.com/
)

pause
