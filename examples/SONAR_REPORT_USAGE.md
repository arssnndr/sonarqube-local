# 🚀 SonarQube Report Shortcut

Quick command untuk menjalankan SonarQube analysis dari project folder.

## 📋 Prerequisites

1. **SonarQube tools** harus sudah terinstall di folder `sonarqube/`
2. **Authentication** sudah dikonfigurasi di `sonarqube/.env`
3. **sonar-project.properties** ada di root project folder

## 🔧 Setup

### Step 1: Copy File

Copy `sonar-report.bat.example` ke root project folder Anda:

```bash
# Dari folder wec-fe-device-bundling
copy sonar-report.bat.example D:\path\to\your-project\sonar-report.bat
```

### Step 2: Edit Project Name (Optional)

Buka `sonar-report.bat` dan ubah line 8:

```batch
echo Running SonarQube analysis for YOUR-PROJECT-NAME...
```

Ganti `YOUR-PROJECT-NAME` dengan nama project Anda (hanya untuk display).

### Step 3: Setup PowerShell Alias (Optional)

Agar bisa run `sonar-report` tanpa prefix `.\`, tambahkan ke PowerShell profile:

```powershell
# Buka PowerShell profile
notepad $PROFILE

# Tambahkan function ini:
function sonar-report {
    if (Test-Path .\sonar-report.bat) {
        .\sonar-report.bat
    } else {
        Write-Host "Error: sonar-report.bat not found in current directory" -ForegroundColor Red
        Write-Host "Please run this command from a project folder that has sonar-report.bat" -ForegroundColor Yellow
    }
}

# Reload profile
. $PROFILE
```

## 🎯 Usage

### Option 1: Direct Command (PowerShell)

```powershell
cd D:\path\to\your-project
.\sonar-report
```

### Option 2: With PowerShell Alias

```powershell
cd D:\path\to\your-project
sonar-report
```

### Option 3: Via npm (if added to package.json)

```powershell
npm run sonar-report
```

## 📂 Output Location

Reports akan disimpan di:

```
your-project/
├── sonarqube-reports/
│   ├── sonarqube_report_<project-key>.json
│   └── ai_analysis_prompt_<project-key>.md
└── sonar-report.bat
```

## 🔍 What It Does

1. ✅ Auto-detect sonarqube tools directory (parent or grandparent folder)
2. ✅ Auto-load authentication dari `sonarqube/.env`
3. ✅ Read project key dari `sonar-project.properties`
4. ✅ Export data dari SonarQube API
5. ✅ Generate AI analysis prompt
6. ✅ Save reports ke `sonarqube-reports/` folder

## 📊 Example Output

```
Running SonarQube analysis for your-project...

Loading authentication from .env file...
========================================
SonarQube Analysis Pipeline
========================================
Project: your-project
Project Dir: D:\path\to\your-project
SonarQube Tools: D:\path\to\sonarqube
Timestamp: 20260509_133210

[1/2] Exporting data from SonarQube...
📊 Mengekspor data dari project: your-project
  ⏳ Mengambil metrics...
  ⏳ Mengambil issues...
  ⏳ Mengambil security hotspots...
  ⏳ Mengambil duplications...
  ⏳ Mengambil coverage per file...

✅ Report berhasil diekspor ke: sonarqube-reports\sonarqube_report_your-project.json

[2/2] Generating AI analysis prompt...
✅ AI analysis prompt saved to: sonarqube-reports\ai_analysis_prompt_your-project.md

========================================
Analysis Complete
========================================
```

## 🐛 Troubleshooting

### Error: "Cannot find sonarqube tools directory"

**Cause:** Script tidak menemukan folder `sonarqube/` di parent atau grandparent directory.

**Solution:**
- Pastikan struktur folder seperti ini:
  ```
  workspace/
  ├── sonarqube/           # Tools folder
  └── your-project/        # Project folder
      └── sonar-report.bat
  ```
- Atau:
  ```
  workspace/
  ├── sonarqube/           # Tools folder
  └── projects/
      └── your-project/    # Project folder
          └── sonar-report.bat
  ```

### Error: "Authentication required (401 Unauthorized)"

**Cause:** Token tidak ditemukan atau tidak valid.

**Solution:**
1. Check file `sonarqube/.env` ada dan berisi:
   ```
   SONARQUBE_URL=http://localhost:9002
   SONARQUBE_TOKEN=squ_your_token_here
   ```
2. Generate token baru di SonarQube: My Account → Security → Generate Token

### Error: "sonar-project.properties not found"

**Cause:** File konfigurasi project tidak ada.

**Solution:**
Create file `sonar-project.properties` di root project:
```properties
sonar.projectKey=your-project-key
sonar.sources=.
sonar.exclusions=**/node_modules/**,**/dist/**
```

## 💡 Tips

1. **Add to .gitignore** untuk exclude reports:
   ```gitignore
   # SonarQube reports
   sonarqube-reports/
   ```

2. **Commit sonar-report.bat** agar team members bisa langsung pakai

3. **Use PowerShell alias** untuk command yang lebih cepat

4. **Run after tests** untuk update coverage data:
   ```powershell
   npm test
   sonar-report
   ```

## 📚 Related Documentation

- [QUICK_START.md](../sonarqube/docs/QUICK_START.md) - Setup guide
- [PROJECT_FOLDER_ANALYSIS.md](../sonarqube/docs/PROJECT_FOLDER_ANALYSIS.md) - Detailed documentation
- [AUTHENTICATION.md](../sonarqube/docs/AUTHENTICATION.md) - Authentication methods
- [README_EXPORT.md](../sonarqube/docs/README_EXPORT.md) - Export tool documentation

## 🆘 Need Help?

Check dokumentasi lengkap di folder `sonarqube/docs/` atau hubungi team DevOps.
