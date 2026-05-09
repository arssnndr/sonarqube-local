# SonarQube Data Exporter & AI Analyzer

Script untuk mengekspor data dari SonarQube dan mempersiapkannya untuk analisis AI.

## 📋 Prerequisites

- Python 3.7+
- SonarQube server yang berjalan (default: http://localhost:9002)
- Library: `requests`

## 🚀 Installation

```bash
pip install requests
```

## � Authentication Setup

SonarQube memerlukan authentication token untuk mengakses API.

### Quick Setup:

1. **Generate token di SonarQube:**
   - Login ke http://localhost:9002
   - My Account → Security → Generate Token
   - Copy token (format: `squ_xxxxx...`)

2. **Set token:**

   **Windows (PowerShell):**
   ```powershell
   $env:SONARQUBE_TOKEN="squ_your_token_here"
   ```

   **Windows (CMD):**
   ```cmd
   set SONARQUBE_TOKEN=squ_your_token_here
   ```

   **Linux/Mac:**
   ```bash
   export SONARQUBE_TOKEN="squ_your_token_here"
   ```

3. **Or pass as argument:**
   ```bash
   python export_sonarqube_data.py wec-fe-device-bundling report.json squ_your_token_here
   ```

📖 **Detailed guide:** See [HOW_TO_GET_TOKEN.md](HOW_TO_GET_TOKEN.md)

## 📖 Usage

### 1. Export Data dari SonarQube

```bash
python export_sonarqube_data.py <project_key> [--output OUTPUT_FILE] [token]
```

**Contoh:**
```bash
# With environment variable (recommended)
set SONARQUBE_TOKEN=squ_your_token
python export_sonarqube_data.py wec-fe-device-bundling

# Save to custom location
python export_sonarqube_data.py wec-fe-device-bundling --output /path/to/report.json

# With token as argument
python export_sonarqube_data.py wec-fe-device-bundling report.json squ_your_token

# Quick run with batch script (saves to sonarqube/reports/)
run_analysis.bat wec-fe-device-bundling

# Quick run with project folder output
run_analysis_in_project.bat D:\SALT-Workspace\wec-fe-device-bundling
```

**Output:**
- File JSON berisi semua data analisis SonarQube
- **File-level coverage analysis** - Daftar file yang perlu ditingkatkan coverage-nya
- Summary di console

### 2. Generate AI Analysis Prompt

```bash
python analyze_sonarqube_report.py <report_file.json> [--output OUTPUT_FILE]
```

**Contoh:**
```bash
# Generate prompt dengan nama file otomatis
python analyze_sonarqube_report.py sonarqube_report_wec-fe-device-bundling.json

# Generate prompt dengan nama file custom
python analyze_sonarqube_report.py my_report.json --output analysis_prompt.md
```

**Output:**
- File Markdown berisi prompt lengkap untuk AI
- **File coverage recommendations** - Daftar file yang perlu ditingkatkan coverage-nya
- Detailed statistics di console

### 3. Analyze dengan AI

Copy isi file `.md` yang dihasilkan ke AI assistant (ChatGPT, Claude, Copilot, dll) untuk mendapatkan analisis mendalam.

## 📊 Data yang Diekspor

### Metrics
- Lines of Code (NCLOC)
- Code Coverage
- Duplications
- Technical Debt
- Reliability Rating
- Security Rating
- Maintainability Rating
- Quality Gate Status

### Issues
- **Bugs**: Logic errors yang dapat menyebabkan unexpected behavior
- **Vulnerabilities**: Security issues
- **Code Smells**: Maintainability issues
- **Security Hotspots**: Code yang perlu security review

### File Coverage Analysis (NEW!)
- **Per-file coverage metrics**: Identifikasi file yang perlu ditingkatkan coverage-nya
- **New code coverage**: Coverage untuk code yang baru ditambahkan (jika tersedia)
- **Overall coverage fallback**: Jika new code metrics tidak tersedia, tampilkan overall coverage
- **Sorted by coverage**: File dengan coverage terendah ditampilkan pertama
- **Actionable recommendations**: Berapa banyak lines yang perlu di-test

### Categorization
- By Type (Bug, Vulnerability, Code Smell)
- By Severity (Blocker, Critical, Major, Minor, Info)
- By File
- By Rule

## 🔧 Configuration

**Option 1: Environment Variable (Recommended)**

```bash
# Windows
set SONARQUBE_TOKEN=squ_your_token_here

# Linux/Mac
export SONARQUBE_TOKEN=squ_your_token_here
```

**Option 2: .env File**

```bash
# Copy example file
copy .env.example .env

# Edit .env and set your token
SONARQUBE_TOKEN=squ_your_token_here
```

**Option 3: Pass as Argument**

```bash
python export_sonarqube_data.py project-key report.json squ_your_token_here
```

### Mendapatkan Authentication Token

📖 **See detailed guide:** [HOW_TO_GET_TOKEN.md](HOW_TO_GET_TOKEN.md)

**Quick steps:**
1. Login ke SonarQube (http://localhost:9002)
2. My Account → Security → Generate Token
3. Copy token (format: `squ_xxxxx...`)
4. Set via environment variable atau argument

## 📁 Output Files

### 1. JSON Report (`sonarqube_report_*.json`)

```json
{
  "export_info": {
    "project_key": "wec-fe-device-bundling",
    "export_date": "2026-05-09T03:30:00",
    "sonarqube_url": "http://localhost:9002",
    "dashboard_url": "http://localhost:9002/dashboard?id=wec-fe-device-bundling"
  },
  "summary": {
    "total_issues": 150,
    "bugs": 10,
    "vulnerabilities": 5,
    "code_smells": 135,
    "security_hotspots": 3
  },
  "metrics": { ... },
  "issues": { ... },
  "security_hotspots": [ ... ]
}
```

### 2. AI Prompt (`ai_analysis_prompt_*.md`)

Markdown file berisi:
- Executive summary request
- Quality Gate analysis with detailed conditions
- Detailed issues breakdown
- **File coverage recommendations** - Specific files that need test coverage improvement
- Security assessment request
- Actionable recommendations
- Actionable recommendations request

## 🎯 AI Analysis Output

AI akan memberikan:

1. **Executive Summary**
   - Overall quality assessment
   - Risk level
   - Top priorities

2. **Critical Issues Analysis**
   - Detailed analysis per issue
   - Potential impact
   - Specific fix recommendations

3. **Security Assessment**
   - Vulnerability evaluation
   - Attack vectors
   - Security hardening recommendations

4. **Code Quality Insights**
   - Common patterns
   - Refactoring areas
   - Best practices violations

5. **Technical Debt Analysis**
   - Effort estimation
   - Prioritization roadmap
   - Quick wins vs long-term improvements

6. **Actionable Recommendations**
   - Top 10 urgent fixes
   - Concrete improvement steps
   - Preventive measures

7. **Metrics Improvement Plan**
   - Realistic targets
   - Coverage improvement strategy
   - Duplication reduction plan

## 🔍 Example Workflow

```bash
# Step 1: Export data
python export_sonarqube_data.py wec-fe-device-bundling

# Output:
# ✅ Report berhasil diekspor ke: sonarqube_report_wec-fe-device-bundling_20260509_033000.json
# 
# 📋 RINGKASAN ANALISIS SONARQUBE
# 🔍 Total Issues: 150
#   🐛 Bugs: 10
#   🔒 Vulnerabilities: 5
#   💡 Code Smells: 135

# Step 2: Generate AI prompt
python analyze_sonarqube_report.py sonarqube_report_wec-fe-device-bundling_20260509_033000.json

# Output:
# ✅ AI analysis prompt saved to: ai_analysis_prompt_wec-fe-device-bundling_20260509_033100.md
# 📝 Prompt length: 15234 characters

# Step 3: Copy prompt to AI
# Open ai_analysis_prompt_wec-fe-device-bundling_20260509_033100.md
# Copy all content
# Paste to your AI assistant (ChatGPT, Claude, Copilot, etc.)
```

## 🛠️ Troubleshooting

### Error: Authentication required (401 Unauthorized)

```bash
❌ Error: Authentication required (401 Unauthorized)

📝 How to fix:
   1. Login to SonarQube: http://localhost:9002
   2. Go to: My Account → Security → Generate Token
   3. Run again with token:
      python export_sonarqube_data.py wec-fe-device-bundling report.json YOUR_TOKEN
   Or set environment variable:
      set SONARQUBE_TOKEN=YOUR_TOKEN
```

**Solution:**
1. Generate token di SonarQube (see [HOW_TO_GET_TOKEN.md](HOW_TO_GET_TOKEN.md))
2. Set token via environment variable atau argument
3. Run script lagi

### Error: Tidak dapat terhubung ke SonarQube

```bash
❌ Error: Tidak dapat terhubung ke SonarQube
   Pastikan SonarQube berjalan di http://localhost:9002
```

**Solution:**
- Check apakah SonarQube server berjalan: `docker compose ps`
- Start SonarQube: `docker compose up -d`
- Verify URL di konfigurasi
- Check firewall/network settings

### Error: Project not found (404)

```bash
❌ Error: 404 Not Found
```

**Solution:**
- Verify project key benar (case-sensitive)
- Check project sudah di-scan di SonarQube
- Lihat list project di SonarQube dashboard
- Run sonar-scanner dulu jika project belum ada

### Error: 403 Forbidden

```bash
❌ Error: 403 Forbidden
```

**Solution:**
- User tidak punya permission untuk project
- Minta admin untuk grant access
- Check apakah token masih valid

## 📚 API Endpoints Used

Script menggunakan SonarQube Web API:

- `/api/measures/component` - Get project metrics
- `/api/issues/search` - Get issues
- `/api/hotspots/search` - Get security hotspots

Documentation: https://docs.sonarqube.org/latest/extend/web-api/

## 🔐 Security Notes

- Jangan commit file yang berisi authentication token
- Simpan token di environment variable atau config file terpisah
- Gunakan `.gitignore` untuk exclude report files jika berisi sensitive data

## 📝 License

MIT License - Feel free to use and modify

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 📧 Support

Jika ada pertanyaan atau issues, silakan buat issue di repository.
