@echo off
echo ========================================
echo   Person Tagger (PER)
echo ========================================
echo.

set /p BASE_DIR="Enter directory to process: "

REM Remove trailing backslash
if "%BASE_DIR:~-1%"=="\" set BASE_DIR=%BASE_DIR:~0,-1%

if not exist "%BASE_DIR%" (
    echo ERROR: Directory not found: %BASE_DIR%
    pause
    exit /b 1
)

echo.
echo Activating environment...
call venv_per\Scripts\activate

echo.
python tag_entities.py "%BASE_DIR%" PER

call deactivate
echo.
pause
