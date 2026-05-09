# 🚀 Quick Start Guide

## Setup dalam 3 Langkah

### 1️⃣ Install Dependencies
```bash
pip install requests
```

### 2️⃣ Setup Authentication

**Option A: Using .env file (Recommended)**
```bash
# 1. Copy example file
copy examples\.env.example .env

# 2. Edit .env and add your token
SONARQUBE_URL=http://localhost:9002
SONARQUBE_TOKEN=squ_your_token_here
```

**Option B: Using environment variable**
```bash
# Windows
set SONARQUBE_TOKEN=squ_your_token_here

# Linux/Mac
export SONARQUBE_TOKEN=squ_your_token_here
```

**Option C: Pass token as argument**
```bash
.\run_analysis.bat project-key squ_your_token_here
```

**How to get token:**
1. Login to SonarQube: http://localhost:9002
2. Go to: My Account → Security → Generate Token
3. Copy the token (starts with `squ_`)

### 3️⃣ Run Analysis

**Option 1: Save to sonarqube/reports/ (default)**
```bash
# Windows
.\run_analysis.bat wec-fe-device-bundling

# Linux/Mac
./run_analysis.sh wec-fe-device-bundling
```

**Option 2: Save to project folder**
```bash
# From sonarqube folder
.\run_analysis_in_project.bat D:\SALT-Workspace\wec-fe-device-bundling

# Or copy script to project folder and run from there
copy run_analysis_in_project.bat D:\SALT-Workspace\wec-fe-device-bundling\
cd D:\SALT-Workspace\wec-fe-device-bundling
.\run_analysis_in_project.bat
```

**Output locations:**
- Option 1: `sonarqube/reports/sonarqube_report_*.json` and `ai_analysis_prompt_*.md`
- Option 2: `your-project/sonarqube-reports/sonarqube_report_*.json` and `ai_analysis_prompt_*.md`

**Note:** Script akan otomatis menghapus report lama dan hanya menyimpan report terbaru untuk setiap project. File yang disimpan:
- `reports/sonarqube_report_<project-key>.json`
- `reports/ai_analysis_prompt_<project-key>.md`

## ✅ Done!

Output files:
- `sonarqube_report_*.json` - Full data export
- `ai_analysis_prompt_*.md` - AI-ready prompt

Copy prompt ke AI assistant (ChatGPT, Claude, Copilot) untuk analisis mendalam.

---

## 📖 Detailed Documentation

- [README_EXPORT.md](README_EXPORT.md) - Complete documentation
- [HOW_TO_GET_TOKEN.md](HOW_TO_GET_TOKEN.md) - Token setup guide
- [README.md](README.md) - SonarQube setup

## 🆘 Need Help?

**Error 401?** → See [HOW_TO_GET_TOKEN.md](HOW_TO_GET_TOKEN.md)

**Other issues?** → See [README_EXPORT.md](README_EXPORT.md) Troubleshooting section
