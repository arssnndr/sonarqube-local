# 🔐 Authentication Guide

## Overview

SonarQube API requires authentication token to access project data. This guide explains 3 methods to provide authentication.

## Method 1: Using .env file (Recommended) ⭐

This is the easiest and most secure method for local development.

### Steps:

1. **Copy the example file:**
   ```bash
   copy examples\.env.example .env
   ```

2. **Edit .env file with your token:**
   ```env
   # SonarQube Configuration
   SONARQUBE_URL=http://localhost:9002
   SONARQUBE_TOKEN=squ_02fc2ed94378a0983e360218efe66f04e7a95a54
   ```

3. **Run scripts (token loaded automatically):**
   ```bash
   # No need to pass token!
   python scripts\export_sonarqube_data.py wec-fe-device-bundling
   
   # Or use batch script
   .\run_analysis.bat wec-fe-device-bundling
   ```

### Benefits:
- ✅ Token stored securely in one place
- ✅ No need to pass token every time
- ✅ .env file is gitignored (won't be committed)
- ✅ Easy to update token

---

## Method 2: Environment Variable

Set token as environment variable in your shell session.

### Windows (PowerShell):
```powershell
$env:SONARQUBE_TOKEN="squ_your_token_here"
python scripts\export_sonarqube_data.py wec-fe-device-bundling
```

### Windows (CMD):
```cmd
set SONARQUBE_TOKEN=squ_your_token_here
python scripts\export_sonarqube_data.py wec-fe-device-bundling
```

### Linux/Mac:
```bash
export SONARQUBE_TOKEN="squ_your_token_here"
python scripts/export_sonarqube_data.py wec-fe-device-bundling
```

### Benefits:
- ✅ Works for current session
- ✅ No files to manage

### Drawbacks:
- ❌ Need to set every time you open new terminal
- ❌ Token visible in shell history

---

## Method 3: Command Line Argument

Pass token directly as command argument.

### Usage:
```bash
# Direct script call
python scripts\export_sonarqube_data.py wec-fe-device-bundling report.json squ_your_token

# With batch script
.\run_analysis.bat wec-fe-device-bundling squ_your_token
```

### Benefits:
- ✅ Quick for one-time use
- ✅ No setup needed

### Drawbacks:
- ❌ Token visible in command history
- ❌ Need to type/paste token every time
- ❌ Less secure

---

## How to Generate SonarQube Token

1. **Login to SonarQube:**
   - Open http://localhost:9002
   - Login with your credentials

2. **Navigate to Security:**
   - Click your profile icon (top right)
   - Select "My Account"
   - Go to "Security" tab

3. **Generate Token:**
   - Enter token name (e.g., "analysis-script")
   - Click "Generate"
   - Copy the token (starts with `squ_`)

4. **Save Token:**
   - Token format: `squ_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - ⚠️ **Important:** Save it immediately! You can't see it again.

📖 **Detailed guide with screenshots:** See [HOW_TO_GET_TOKEN.md](HOW_TO_GET_TOKEN.md)

---

## Priority Order

Scripts check for token in this order:

1. **Command line argument** (highest priority)
2. **Environment variable** (`SONARQUBE_TOKEN`)
3. **.env file** (loaded automatically)

If no token found, script will show warning and try without authentication (will fail if server requires auth).

---

## Security Best Practices

✅ **DO:**
- Use .env file for local development
- Add .env to .gitignore (already done)
- Rotate tokens periodically
- Use different tokens for different purposes

❌ **DON'T:**
- Commit tokens to git
- Share tokens in chat/email
- Use same token for production and development
- Store tokens in code files

---

## Troubleshooting

### Error: "Authentication required (401 Unauthorized)"

**Cause:** No token provided or invalid token.

**Solution:**
1. Check if .env file exists and contains valid token
2. Verify token format starts with `squ_`
3. Generate new token if expired
4. Check SONARQUBE_URL is correct

### Error: "Token not found in .env"

**Cause:** .env file doesn't exist or is empty.

**Solution:**
```bash
# Copy example file
copy examples\.env.example .env

# Edit .env and add your token
notepad .env
```

### Token works in browser but not in script

**Cause:** Token might be session-based (not API token).

**Solution:**
- Generate new token from "My Account → Security"
- Make sure it's a "User Token", not session cookie

---

## Examples

### Example 1: First time setup
```bash
# 1. Copy example
copy examples\.env.example .env

# 2. Edit .env (add your token)
notepad .env

# 3. Run analysis
.\run_analysis.bat wec-fe-device-bundling
```

### Example 2: Quick one-time analysis
```bash
.\run_analysis.bat wec-fe-device-bundling squ_your_token_here
```

### Example 3: CI/CD pipeline
```bash
# Set token from secret
set SONARQUBE_TOKEN=%CI_SONARQUBE_TOKEN%

# Run analysis
python scripts\export_sonarqube_data.py %PROJECT_KEY%
```

---

## Related Documentation

- [Quick Start Guide](QUICK_START.md) - Get started in 3 steps
- [How to Get Token](HOW_TO_GET_TOKEN.md) - Detailed token generation guide
- [README Export](README_EXPORT.md) - Complete usage documentation
