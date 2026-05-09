@echo off
REM Quick script untuk export dan analyze SonarQube report
REM Usage: run_analysis.bat <project_key> [token]

if "%1"=="" (
    echo Usage: run_analysis.bat ^<project_key^> [token]
    echo.
    echo Example:
    echo   run_analysis.bat wec-fe-device-bundling
    echo   run_analysis.bat wec-fe-device-bundling squ_your_token_here
    echo.
    echo Or set environment variable:
    echo   set SONARQUBE_TOKEN=squ_your_token_here
    echo   run_analysis.bat wec-fe-device-bundling
    exit /b 1
)

set PROJECT_KEY=%1
set SONARQUBE_TOKEN_ARG=%2
set TIMESTAMP=%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%

echo ========================================
echo SonarQube Analysis Pipeline
echo ========================================
echo Project: %PROJECT_KEY%
echo Timestamp: %TIMESTAMP%
echo.

REM Step 1: Export data
echo [1/2] Exporting data from SonarQube...
if "%SONARQUBE_TOKEN_ARG%"=="" (
    python scripts\export_sonarqube_data.py %PROJECT_KEY%
) else (
    python scripts\export_sonarqube_data.py %PROJECT_KEY% %SONARQUBE_TOKEN_ARG%
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to export data
    exit /b 1
)

REM Use fixed report filename
set REPORT_FILE=reports\sonarqube_report_%PROJECT_KEY%.json

if not exist "%REPORT_FILE%" (
    echo.
    echo ERROR: Report file not found
    exit /b 1
)

echo.
echo [2/2] Generating AI analysis prompt...
python scripts\analyze_sonarqube_report.py %REPORT_FILE%

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to generate AI prompt
    exit /b 1
)

REM Use fixed prompt filename
set PROMPT_FILE=reports\ai_analysis_prompt_%PROJECT_KEY%.md

echo.
echo ========================================
echo Analysis Complete!
echo ========================================
echo Report: %REPORT_FILE%
echo Prompt: %PROMPT_FILE%
