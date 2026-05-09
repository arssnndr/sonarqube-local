# SonarQube Local Setup

## 📁 Project Structure

```
sonarqube/
├── scripts/              # Python scripts untuk export dan analysis
│   ├── export_sonarqube_data.py
│   ├── analyze_sonarqube_report.py
│   ├── automated_analysis.py
│   └── check_quality_gate.py
├── reports/              # Generated reports (gitignored)
│   ├── sonarqube_report_*.json
│   └── ai_analysis_prompt_*.md
├── docs/                 # Documentation
│   ├── QUICK_START.md       - Quick setup guide
│   ├── AUTHENTICATION.md    - Authentication methods
│   ├── README_EXPORT.md     - Export tool documentation
│   └── HOW_TO_GET_TOKEN.md  - Token generation guide
├── examples/             # Example configurations
│   ├── .env.example
│   ├── sonar-report.bat.example
│   └── SONAR_REPORT_USAGE.md
├── .env                  # Your local config (create from .env.example)
├── sonar-scanner-*/      # SonarQube scanner CLI
├── docker-compose.yml    # SonarQube server setup
├── run_analysis.bat      # Quick run script (Windows)
├── run_analysis.sh       # Quick run script (Linux/Mac)
├── run_analysis_in_project.bat  # Run from/for project folder
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🚀 Quick Start

**3 Steps to analyze your project:**

1. **Install dependencies:**
   ```bash
   pip install requests
   ```

2. **Setup authentication:**
   ```bash
   # Copy example file
   copy examples\.env.example .env
   
   # Edit .env and add your SonarQube token
   # Get token from: http://localhost:9002 → My Account → Security
   ```

3. **Run analysis:**
   ```bash
   # Option 1: Save reports to sonarqube/reports/
   .\run_analysis.bat your-project-key
   
   # Option 2: Save reports to project folder
   .\run_analysis_in_project.bat D:\path\to\your-project
   ```

📖 **Detailed guide:** [docs/QUICK_START.md](docs/QUICK_START.md)  
🔐 **Authentication help:** [docs/AUTHENTICATION.md](docs/AUTHENTICATION.md)  
📂 **Project structure:** [STRUCTURE.md](STRUCTURE.md)

---

## 1. Start SonarQube

Run the local stack:

```bash
docker compose up -d --build
```

Open the UI at [http://localhost:9002](http://localhost:9002), then go to your profile, open **My Account**, select **Security**, and generate a new token.

## 2. Install SonarScanner CLI

Download SonarScanner from the official documentation:

https://docs.sonarsource.com/sonarqube/latest/analyzing-source-code/scanners/sonarscanner/

Extract the archive and place it in a stable location on your machine.

### Linux

Add this alias to your shell profile:

```bash
alias sonar-scanner='~/sonar-scanner/bin/sonar-scanner'
```

### Windows

Add the SonarScanner bin directory to your PATH:

- Open Run with Win+R, enter `sysdm.cpl`
- Go to **Advanced** > **Environment Variables**
- Edit **Path** and add the full path to the SonarScanner `bin` folder

You can also set it temporarily in PowerShell:

```powershell
$env:PATH = "D:\SALT-Workspace\sonarqube\sonar-scanner-8.0.1.6346-windows-x64\bin;$env:PATH"
```

## 3. Configure SonarScanner

Edit the SonarScanner config file in `sonar-scanner/conf/sonar-scanner.properties`:

```properties
sonar.host.url=http://localhost:9002
sonar.login=YOUR_TOKEN_HERE
```

## 4. Configure Your Project

Add a `sonar-project.properties` file to the project root:

```properties
sonar.projectKey=YOUR_PROJECT_NAME
sonar.sources=.
sonar.tests=.
sonar.tests.inclusions=**/*.spec.ts
sonar.exclusions=**/node_modules/**,Dockerfile*,*.js,server.ts,src/index.html,src/@core/**
sonar.typescript.lcov.reportPaths=coverage/voting/lcov.info
```

Adjust the project key and coverage path to match your project structure.

## 5. Run the Analysis

From the project directory, run:

```bash
sonar-scanner
```

## Troubleshooting

If you see this error:

> bootstrap check failure [1] of [1]: max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]

Fix it on Linux by updating `/etc/sysctl.conf`:

```conf
vm.max_map_count=262144
```

Then apply the change:

```bash
sudo sysctl -p
```

---

## 📊 SonarQube Data Export & AI Analysis

### Overview

Tools untuk mengekspor data analisis dari SonarQube dan mempersiapkannya untuk analisis AI yang mendalam.

### Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Export data dari SonarQube:**
```bash
python export_sonarqube_data.py wec-fe-device-bundling
```

3. **Generate AI analysis prompt:**
```bash
python analyze_sonarqube_report.py sonarqube_report_wec-fe-device-bundling_*.json
```

4. **Copy prompt ke AI assistant** (ChatGPT, Claude, Copilot) untuk analisis mendalam

### Quick Run (Windows)

```bash
run_analysis.bat wec-fe-device-bundling
```

### Quick Run (Linux/Mac)

```bash
chmod +x run_analysis.sh
./run_analysis.sh wec-fe-device-bundling
```

### Automated Analysis with AI API

```bash
# With OpenAI
export OPENAI_API_KEY="your-key"
python automated_analysis.py wec-fe-device-bundling

# With Anthropic Claude
export ANTHROPIC_API_KEY="your-key"
python automated_analysis.py wec-fe-device-bundling http://localhost:9002 anthropic
```

### What You Get

- **Comprehensive JSON report** dengan semua metrics, issues, dan security hotspots
- **AI-ready prompt** yang terstruktur untuk analisis mendalam
- **Detailed statistics** tentang code quality
- **Actionable recommendations** dari AI

### Features

✅ Export semua data dari SonarQube (metrics, issues, hotspots)  
✅ Kategorisasi issues by type dan severity  
✅ **File-level coverage analysis** - Identifikasi file yang perlu ditingkatkan coverage-nya  
✅ Generate AI analysis prompt yang comprehensive  
✅ Support untuk automated analysis via AI APIs  
✅ Detailed statistics dan insights  
✅ Top violated rules dan problematic files  
✅ **Flexible output location** - Save reports to sonarqube/reports/ or project folder  

### Documentation

📖 **Complete guides:**
- [QUICK_START.md](docs/QUICK_START.md) - Quick setup guide
- [README_EXPORT.md](docs/README_EXPORT.md) - Export tool documentation
- [PROJECT_FOLDER_ANALYSIS.md](docs/PROJECT_FOLDER_ANALYSIS.md) - Project folder analysis guide
- [AUTHENTICATION.md](docs/AUTHENTICATION.md) - Authentication methods
- [STRUCTURE.md](STRUCTURE.md) - Project structure

🚀 **Quick shortcuts:**
- [sonar-report.bat.example](examples/sonar-report.bat.example) - Shortcut command for projects
- [SONAR_REPORT_USAGE.md](examples/SONAR_REPORT_USAGE.md) - How to use sonar-report shortcut

### Files

- `export_sonarqube_data.py` - Export data dari SonarQube
- `analyze_sonarqube_report.py` - Generate AI analysis prompt
- `automated_analysis.py` - Automated analysis dengan AI API
- `run_analysis.bat` - Quick run script (Windows)
- `run_analysis.sh` - Quick run script (Linux/Mac)
- `requirements.txt` - Python dependencies