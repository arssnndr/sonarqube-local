# 🔐 Cara Mendapatkan SonarQube Token

## Langkah-langkah:

### 1. Login ke SonarQube
Buka browser dan akses: http://localhost:9002

**Default credentials:**
- Username: `admin`
- Password: `admin`

### 2. Buka My Account
- Klik icon user di pojok kanan atas
- Pilih **My Account**

### 3. Generate Token
- Klik tab **Security**
- Di bagian **Generate Tokens**:
  - **Name**: Masukkan nama token (contoh: `local-analysis`)
  - **Type**: Pilih **User Token**
  - **Expires in**: Pilih durasi (contoh: 30 days atau No expiration)
- Klik **Generate**

### 4. Copy Token
- Token akan muncul **HANYA SEKALI**
- Copy token tersebut (format: `squ_xxxxxxxxxxxxxxxxxxxxxxxxxx`)
- Simpan di tempat aman

### 5. Set Token

**Option 1: Environment Variable (Recommended)**

Windows (PowerShell):
```powershell
$env:SONARQUBE_TOKEN="squ_your_token_here"
```

Windows (CMD):
```cmd
set SONARQUBE_TOKEN=squ_your_token_here
```

Linux/Mac:
```bash
export SONARQUBE_TOKEN="squ_your_token_here"
```

**Option 2: .env File**
```bash
# Copy example file
copy .env.example .env

# Edit .env file dan isi token
SONARQUBE_TOKEN=squ_your_token_here
```

**Option 3: Pass as Argument**
```bash
python export_sonarqube_data.py wec-fe-device-bundling report.json squ_your_token_here
```

### 6. Test Connection
```bash
# Windows
.\run_analysis.bat wec-fe-device-bundling

# Linux/Mac
./run_analysis.sh wec-fe-device-bundling
```

## ⚠️ Security Notes

- **JANGAN** commit token ke git
- **JANGAN** share token di public
- `.env` file sudah ada di `.gitignore`
- Revoke token jika tidak digunakan lagi
- Generate token baru jika token lama expired

## 🔄 Revoke Token

Jika token sudah tidak digunakan atau compromised:

1. Login ke SonarQube
2. My Account → Security
3. Cari token yang ingin di-revoke
4. Klik **Revoke**

## 📝 Token Format

Token SonarQube format:
- Prefix: `squ_`
- Length: ~40 characters
- Example: `squ_1234567890abcdef1234567890abcdef12345678`

## ❓ Troubleshooting

### Error: 401 Unauthorized
- Token salah atau expired
- Generate token baru
- Pastikan token di-set dengan benar

### Error: 403 Forbidden
- User tidak punya permission untuk project
- Minta admin untuk grant access

### Token tidak terdeteksi
- Check environment variable: `echo %SONARQUBE_TOKEN%` (Windows) atau `echo $SONARQUBE_TOKEN` (Linux/Mac)
- Pastikan tidak ada spasi atau quotes extra
- Restart terminal setelah set environment variable
