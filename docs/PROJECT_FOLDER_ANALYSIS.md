# 📁 Project Folder Analysis

Guide untuk menjalankan analisis SonarQube dan menyimpan report langsung di folder project.

## 🎯 Overview

Script `run_analysis_in_project.bat` memungkinkan Anda untuk:
- Menjalankan analisis dari dalam folder project
- Menyimpan report langsung di folder project (`sonarqube-reports/`)
- Otomatis membaca `sonar.projectKey` dari `sonar-project.properties`

## 🚀 Usage

### Option 1: Run dari Sonarqube Folder

```bash
cd D:\SALT-Workspace\sonarqube
.\run_analysis_in_project.bat D:\SALT-Workspace\wec-fe-device-bundling
```

### Option 2: Copy Script ke Project Folder

```bash
# 1. Copy script ke project folder
copy D:\SALT-Workspace\sonarqube\run_analysis_in_project.bat D:\SALT-Workspace\wec-fe-device-bundling\

# 2. Run dari project folder
cd D:\SALT-Workspace\wec-fe-device-bundling
.\run_analysis_in_project.bat
```

## 📂 Output Location

Reports akan disimpan di folder project:

```
wec-fe-device-bundling/
├── sonarqube-reports/
│   ├── sonarqube_report_wec-fe-device-bundling.json
│   └── ai_analysis_prompt_wec-fe-device-bundling.md
├── src/
├── sonar-project.properties
└── ...
```

## ⚙️ Requirements

1. **sonar-project.properties** harus ada di root project folder:
   ```properties
   sonar.projectKey=wec-fe-device-bundling
   sonar.sources=.
   # ... other properties
   ```

2. **SonarQube tools** harus ada di salah satu lokasi:
   - `../sonarqube/` (parent folder)
   - `../../sonarqube/` (grandparent folder)

3. **Authentication** via `.env` file di sonarqube folder:
   ```bash
   SONARQUBE_URL=http://localhost:9002
   SONARQUBE_TOKEN=squ_your_token_here
   ```

## 🔄 Workflow

Script akan:
1. Detect apakah running dari project folder atau sonarqube folder
2. Read `sonar.projectKey` dari `sonar-project.properties`
3. Find sonarqube tools directory
4. Create `sonarqube-reports/` folder di project directory
5. Export data dari SonarQube
6. Generate AI analysis prompt
7. Save kedua file di `project/sonarqube-reports/`

## 📊 Output Files

### 1. `sonarqube_report_<project-key>.json`
- Full data export dari SonarQube
- Metrics, issues, hotspots, duplications
- **File-level coverage analysis**

### 2. `ai_analysis_prompt_<project-key>.md`
- AI-ready analysis prompt
- Quality Gate details
- **File coverage recommendations**
- Actionable insights

## 🎯 Benefits

✅ **Organized**: Reports tersimpan di project folder, tidak tercampur dengan project lain  
✅ **Portable**: Bisa di-commit ke git atau di-share dengan team  
✅ **Convenient**: Tidak perlu specify project key, otomatis baca dari sonar-project.properties  
✅ **Flexible**: Bisa run dari sonarqube folder atau project folder  

## 🔒 .gitignore

Tambahkan ke `.gitignore` project Anda jika tidak ingin commit reports:

```gitignore
# SonarQube reports
sonarqube-reports/
```

Atau jika ingin commit untuk tracking:

```gitignore
# Ignore reports but keep folder structure
sonarqube-reports/*.json
sonarqube-reports/*.md
!sonarqube-reports/.gitkeep
```

## 🆚 Comparison: Default vs Project Folder

| Feature | `run_analysis.bat` | `run_analysis_in_project.bat` |
|---------|-------------------|-------------------------------|
| Output location | `sonarqube/reports/` | `project/sonarqube-reports/` |
| Project key | Manual argument | Auto from sonar-project.properties |
| Use case | Centralized reports | Per-project reports |
| Best for | Quick analysis | Team collaboration |

## 💡 Tips

1. **Add to .gitignore** jika reports tidak perlu di-commit
2. **Use Option 2** (copy to project) jika sering analyze project tersebut
3. **Commit .md file** untuk share AI analysis dengan team
4. **Keep .json file local** karena ukurannya besar

## 🐛 Troubleshooting

**Error: "sonar-project.properties not found"**
- Pastikan file `sonar-project.properties` ada di root project folder
- Check path yang diberikan sudah benar

**Error: "Cannot find sonarqube tools directory"**
- Pastikan folder `sonarqube` ada di parent atau grandparent directory
- Atau run dari sonarqube folder dengan memberikan project path

**Error: "Could not read sonar.projectKey"**
- Check format `sonar-project.properties`
- Pastikan ada line: `sonar.projectKey=your-project-key`

## 📚 Related Documentation

- [QUICK_START.md](QUICK_START.md) - Basic setup guide
- [AUTHENTICATION.md](AUTHENTICATION.md) - Authentication methods
- [README_EXPORT.md](README_EXPORT.md) - Export tool documentation
- [STRUCTURE.md](../STRUCTURE.md) - Project structure
