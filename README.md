# SonarQube Local Setup

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