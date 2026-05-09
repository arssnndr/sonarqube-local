@echo off
REM Script untuk export dan analyze SonarQube report dari dalam folder project
REM Usage: 
REM   1. Copy script ini ke folder project (contoh: wec-fe-device-bundling/)
REM   2. Jalankan: run_analysis_in_project.bat
REM   atau dari sonarqube folder: run_analysis_in_project.bat <path_to_project>

setlocal enabledelayedexpansion

REM Detect if running from project folder or sonarqube folder
if exist "sonar-project.properties" (
    REM Running from project folder
    set "PROJECT_DIR=%CD%"
    
    REM Read project key from sonar-project.properties
    for /f "tokens=1,2 delims==" %%a in (sonar-project.properties) do (
        if "%%a"=="sonar.projectKey" set "PROJECT_KEY=%%b"
    )
    
    REM Find sonarqube tools folder (assume it's in parent or sibling directory)
    if exist "..\sonarqube\scripts\export_sonarqube_data.py" (
        set "SONARQUBE_DIR=%CD%\..\sonarqube"
    ) else if exist "..\..\sonarqube\scripts\export_sonarqube_data.py" (
        set "SONARQUBE_DIR=%CD%\..\..\sonarqube"
    ) else (
        echo ERROR: Cannot find sonarqube tools directory
        echo Please ensure sonarqube folder exists with scripts/export_sonarqube_data.py
        exit /b 1
    )
) else if "%~1" NEQ "" (
    REM Running from sonarqube folder with project path argument
    set "PROJECT_DIR=%~1"
    
    if not exist "!PROJECT_DIR!\sonar-project.properties" (
        echo ERROR: sonar-project.properties not found in !PROJECT_DIR!
        exit /b 1
    )
    
    REM Read project key from sonar-project.properties
    for /f "tokens=1,2 delims==" %%a in (!PROJECT_DIR!\sonar-project.properties) do (
        if "%%a"=="sonar.projectKey" set "PROJECT_KEY=%%b"
    )
    
    set "SONARQUBE_DIR=%CD%"
) else (
    echo Usage:
    echo   Option 1: Copy this script to your project folder and run it
    echo   Option 2: run_analysis_in_project.bat ^<path_to_project^>
    echo.
    echo Example:
    echo   run_analysis_in_project.bat D:\SALT-Workspace\wec-fe-device-bundling
    exit /b 1
)

if "!PROJECT_KEY!"=="" (
    echo ERROR: Could not read sonar.projectKey from sonar-project.properties
    exit /b 1
)

set TIMESTAMP=%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%

echo ========================================
echo SonarQube Analysis Pipeline
echo ========================================
echo Project: !PROJECT_KEY!
echo Project Dir: !PROJECT_DIR!
echo SonarQube Tools: !SONARQUBE_DIR!
echo Timestamp: %TIMESTAMP%
echo.

REM Create reports folder in project directory
if not exist "!PROJECT_DIR!\sonarqube-reports" mkdir "!PROJECT_DIR!\sonarqube-reports"

REM Step 1: Export data
echo [1/2] Exporting data from SonarQube...
python "!SONARQUBE_DIR!\scripts\export_sonarqube_data.py" !PROJECT_KEY! --output "!PROJECT_DIR!\sonarqube-reports\sonarqube_report_!PROJECT_KEY!.json"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to export data
    exit /b 1
)

set REPORT_FILE=!PROJECT_DIR!\sonarqube-reports\sonarqube_report_!PROJECT_KEY!.json

if not exist "!REPORT_FILE!" (
    echo.
    echo ERROR: Report file not found
    exit /b 1
)

echo.
echo [2/2] Generating AI analysis prompt...
python "!SONARQUBE_DIR!\scripts\analyze_sonarqube_report.py" "!REPORT_FILE!" --output "!PROJECT_DIR!\sonarqube-reports\ai_analysis_prompt_!PROJECT_KEY!.md"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to generate AI prompt
    exit /b 1
)

set PROMPT_FILE=!PROJECT_DIR!\sonarqube-reports\ai_analysis_prompt_!PROJECT_KEY!.md

echo.
echo ========================================
echo Analysis Complete!
echo ========================================
echo Report: !REPORT_FILE!
echo Prompt: !PROMPT_FILE!
