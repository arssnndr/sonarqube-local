# 📁 Project Structure

## Overview

Project ini terorganisir dalam struktur folder yang jelas untuk memudahkan maintenance dan penggunaan.

```
sonarqube/
├── scripts/                    # Python scripts
│   ├── export_sonarqube_data.py       # Export data dari SonarQube API
│   ├── analyze_sonarqube_report.py    # Generate AI analysis prompt
│   ├── automated_analysis.py          # Automated AI analysis via API
│   └── check_quality_gate.py          # Quick Quality Gate checker
│
├── reports/                    # Generated reports (gitignored)
│   ├── sonarqube_report_*.json        # Raw SonarQube data exports
│   └── ai_analysis_prompt_*.md        # AI-ready analysis prompts
│
├── docs/                       # Documentation
│   ├── README_EXPORT.md               # Complete export tool documentation
│   ├── HOW_TO_GET_TOKEN.md            # Token setup guide
│   ├── QUICK_START.md                 # Quick start guide
│   ├── AUTHENTICATION.md              # Authentication methods
│   └── PROJECT_FOLDER_ANALYSIS.md     # Project folder analysis guide
│
├── examples/                   # Example configurations
│   ├── .env.example                   # Environment variable template
│   ├── sonar-report.bat.example       # Shortcut command template
│   └── SONAR_REPORT_USAGE.md          # Usage guide for sonar-report
│
├── sonar-scanner-*/            # SonarQube Scanner CLI (gitignored)
│   ├── bin/                           # Scanner executables
│   └── conf/                          # Scanner configuration
│
├── docker-compose.yml          # SonarQube server setup
├── run_analysis.bat            # Quick run script (Windows)
├── run_analysis.sh             # Quick run script (Linux/Mac)
├── run_analysis_in_project.bat # Run and save to project folder
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── .env                        # Environment variables (gitignored)
├── README.md                   # Main documentation
└── STRUCTURE.md               # This file
```

## Folder Descriptions

### 📂 scripts/
Contains all Python scripts for SonarQube data export and analysis.

**Files:**
- `export_sonarqube_data.py` - Main export script that fetches data from SonarQube API
- `analyze_sonarqube_report.py` - Generates comprehensive AI analysis prompts
- `automated_analysis.py` - Integrates with AI APIs for automated analysis
- `check_quality_gate.py` - Quick utility to check Quality Gate status

**Usage:**
```bash
python scripts/export_sonarqube_data.py project-key
python scripts/analyze_sonarqube_report.py reports/report.json
python scripts/check_quality_gate.py
```

### 📂 reports/
Stores all generated reports. This folder is gitignored to avoid committing large JSON files.

**Generated files:**
- `sonarqube_report_<project>_<timestamp>.json` - Complete SonarQube data export
- `ai_analysis_prompt_<project>_<timestamp>.md` - AI-ready analysis prompt

**Auto-created:** Yes, scripts automatically create this folder if it doesn't exist.

### 📂 docs/
Complete documentation for the project.

**Files:**
- `README_EXPORT.md` - Detailed documentation for export and analysis tools
- `HOW_TO_GET_TOKEN.md` - Step-by-step guide to get SonarQube authentication token
- `QUICK_START.md` - Quick start guide for new users
- `AUTHENTICATION.md` - Complete authentication methods guide
- `PROJECT_FOLDER_ANALYSIS.md` - Guide for saving reports to project folder

### 📂 examples/
Example configuration files and templates.

**Files:**
- `.env.example` - Template for environment variables (copy to `.env` and fill in)
- `sonar-report.bat.example` - Template for project shortcut command
- `SONAR_REPORT_USAGE.md` - Complete usage guide for sonar-report shortcut

**Usage:**
```bash
# Setup authentication
copy examples\.env.example .env
# Edit .env with your values

# Setup project shortcut
copy examples\sonar-report.bat.example D:\path\to\your-project\sonar-report.bat
# See SONAR_REPORT_USAGE.md for detailed instructions
```

### 📂 sonar-scanner-*/
SonarQube Scanner CLI tool. Downloaded separately from SonarQube website.

**Not included in git** - Download from: https://docs.sonarsource.com/sonarqube/latest/analyzing-source-code/scanners/sonarscanner/

## Quick Commands

### Run Full Analysis

**Option 1: Save to sonarqube/reports/ (default)**
```bash
# Windows
.\run_analysis.bat project-key

# Linux/Mac
./run_analysis.sh project-key
```

**Option 2: Save to project folder**
```bash
# From sonarqube folder
.\run_analysis_in_project.bat D:\SALT-Workspace\wec-fe-device-bundling

# From project folder (after copying script)
cd D:\SALT-Workspace\wec-fe-device-bundling
.\run_analysis_in_project.bat
```

### Direct Script Usage
```bash
# Export only
python scripts/export_sonarqube_data.py project-key

# Export to custom location
python scripts/export_sonarqube_data.py project-key --output /path/to/report.json

# Analyze existing report
python scripts/analyze_sonarqube_report.py reports/report.json

# Analyze with custom output
python scripts/analyze_sonarqube_report.py report.json --output prompt.md

# Check Quality Gate
python scripts/check_quality_gate.py
```

## File Naming Conventions

### Reports (Fixed Filenames - No Timestamps)
- Format: `sonarqube_report_<project-key>.json`
- Example: `sonarqube_report_wec-fe-device-bundling.json`
- **Note:** Old report automatically deleted when new one is created

### AI Prompts (Fixed Filenames - No Timestamps)
- Format: `ai_analysis_prompt_<project-key>.md`
- Example: `ai_analysis_prompt_wec-fe-device-bundling.md`
- **Note:** Old prompt automatically deleted when new one is created

### Benefits of Fixed Filenames
- ✅ No file accumulation - always only 2 files per project
- ✅ Easy to find - predictable filename
- ✅ Git-friendly - same filename for tracking changes
- ✅ No manual cleanup needed

## Gitignore Rules

The following are excluded from git:

```
# Generated reports
reports/*.json
reports/*.md

# Environment variables
.env

# SonarQube scanner
sonar-scanner-*

# Python
*.pyc
__pycache__/
.pytest_cache/

# IDE
.vscode/

# Logs
*.log
```

**Note:** Project folders may also have `sonarqube-reports/` folder when using `run_analysis_in_project.bat`. Add to project's `.gitignore` if needed.

## Adding New Scripts

When adding new Python scripts:

1. Place in `scripts/` folder
2. Update this documentation
3. Update `README.md` if it's a major feature
4. Add usage examples in `docs/README_EXPORT.md`

## Maintenance

### Cleaning Old Reports

**Note:** With fixed filenames, manual cleanup is rarely needed. Scripts automatically delete old reports before creating new ones.

If you need to clean all reports:
```bash
# Windows
del reports\*.json
del reports\*.md

# Linux/Mac
rm reports/*.json
rm reports/*.md
```

# Linux/Mac
rm reports/sonarqube_report_*.json
rm reports/ai_analysis_prompt_*.md
```

### Backup Reports
```bash
# Create backup folder
mkdir reports_backup
copy reports\*.* reports_backup\
```

## Environment Variables

Set in `.env` file (copy from `examples/.env.example`):

```bash
SONARQUBE_URL=http://localhost:9002
SONARQUBE_TOKEN=squ_your_token_here
```

Or set directly in shell:
```bash
# Windows
set SONARQUBE_TOKEN=squ_your_token

# Linux/Mac
export SONARQUBE_TOKEN=squ_your_token
```

## Dependencies

Install Python dependencies:
```bash
pip install -r requirements.txt
```

Current dependencies:
- `requests>=2.31.0` - HTTP library for API calls

## Support

For issues or questions:
1. Check `docs/README_EXPORT.md` for detailed documentation
2. Check `docs/HOW_TO_GET_TOKEN.md` for authentication issues
3. Check `docs/QUICK_START.md` for quick setup guide
