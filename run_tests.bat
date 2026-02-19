@echo off
REM Playwright Pytest Test Execution Script for Windows

echo ================================
echo Playwright Test Automation
echo ================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Parse command line arguments
set TEST_TYPE=%1
set BROWSER=%2
set HEADED=%3

if "%TEST_TYPE%"=="" set TEST_TYPE=all
if "%BROWSER%"=="" set BROWSER=chromium
if "%HEADED%"=="" set HEADED=false

echo Configuration:
echo   Test Type: %TEST_TYPE%
echo   Browser: %BROWSER%
echo   Headed: %HEADED%
echo.

REM Run tests based on type
if "%TEST_TYPE%"=="smoke" (
    echo Running smoke tests...
    pytest -m smoke --browser=%BROWSER% --headed=%HEADED%
) else if "%TEST_TYPE%"=="regression" (
    echo Running regression tests...
    pytest -m regression --browser=%BROWSER% --headed=%HEADED%
) else if "%TEST_TYPE%"=="critical" (
    echo Running critical tests...
    pytest -m critical --browser=%BROWSER% --headed=%HEADED%
) else if "%TEST_TYPE%"=="login" (
    echo Running login tests...
    pytest tests/test_login.py --browser=%BROWSER% --headed=%HEADED%
) else if "%TEST_TYPE%"=="products" (
    echo Running products tests...
    pytest tests/test_products.py --browser=%BROWSER% --headed=%HEADED%
) else if "%TEST_TYPE%"=="parallel" (
    echo Running all tests in parallel...
    pytest -n auto --browser=%BROWSER% --headed=%HEADED%
) else if "%TEST_TYPE%"=="all" (
    echo Running all tests...
    pytest --browser=%BROWSER% --headed=%HEADED%
) else (
    echo Invalid test type: %TEST_TYPE%
    echo Usage: run_tests.bat [smoke^|regression^|critical^|login^|products^|parallel^|all] [chromium^|firefox^|webkit] [true^|false]
    pause
    exit /b 1
)

echo.
echo ================================

REM Check test exit code
if %ERRORLEVEL% EQU 0 (
    echo Tests completed successfully!
    echo Generating Allure report...
    allure serve reports/allure-results
) else (
    echo Some tests failed!
    echo Generating Allure report for failed tests...
    allure serve reports/allure-results
)

pause
