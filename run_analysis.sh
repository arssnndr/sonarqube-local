#!/bin/bash
# Quick script untuk export dan analyze SonarQube report
# Usage: ./run_analysis.sh <project_key> [token]

if [ -z "$1" ]; then
    echo "Usage: ./run_analysis.sh <project_key> [token]"
    echo ""
    echo "Example:"
    echo "  ./run_analysis.sh wec-fe-device-bundling"
    echo "  ./run_analysis.sh wec-fe-device-bundling squ_your_token_here"
    echo ""
    echo "Or set environment variable:"
    echo "  export SONARQUBE_TOKEN=squ_your_token_here"
    echo "  ./run_analysis.sh wec-fe-device-bundling"
    exit 1
fi

PROJECT_KEY=$1
SONARQUBE_TOKEN_ARG=$2
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "========================================"
echo "SonarQube Analysis Pipeline"
echo "========================================"
echo "Project: $PROJECT_KEY"
echo "Timestamp: $TIMESTAMP"
echo ""

# Step 1: Export data
echo "[1/2] Exporting data from SonarQube..."
if [ -z "$SONARQUBE_TOKEN_ARG" ]; then
    python3 scripts/export_sonarqube_data.py "$PROJECT_KEY"
else
    python3 scripts/export_sonarqube_data.py "$PROJECT_KEY" "$SONARQUBE_TOKEN_ARG"
fi

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to export data"
    exit 1
fi

# Use fixed report filename
REPORT_FILE="reports/sonarqube_report_${PROJECT_KEY}.json"

if [ ! -f "$REPORT_FILE" ]; then
    echo ""
    echo "ERROR: Report file not found"
    exit 1
fi

echo ""
echo "[2/2] Generating AI analysis prompt..."
python3 scripts/analyze_sonarqube_report.py "$REPORT_FILE"

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to generate AI prompt"
    exit 1
fi

# Use fixed prompt filename
PROMPT_FILE="reports/ai_analysis_prompt_${PROJECT_KEY}.md"

echo ""
echo "========================================"
echo "Analysis Complete!"
echo "========================================"
echo "Report: $REPORT_FILE"
echo "Prompt: $PROMPT_FILE"
echo ""
echo "Next steps:"
echo "1. Open $PROMPT_FILE"
echo "2. Copy content to your AI assistant"
echo "3. Get comprehensive analysis and recommendations"
echo ""
