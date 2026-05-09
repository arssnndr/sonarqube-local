#!/usr/bin/env python3
"""Check New Code Period settings"""

import requests
import json

# Load token from .env
with open('.env', 'r') as f:
    for line in f:
        if line.startswith('SONARQUBE_TOKEN='):
            token = line.split('=')[1].strip()
            break

base_url = 'http://localhost:9002'
project_key = 'wec-fe-device-bundling'

# Check New Code Period settings
url = f"{base_url}/api/new_code_periods/show"
params = {'project': project_key}

print(f"Checking New Code Period settings...")
print(f"URL: {url}")
print()

response = requests.get(url, params=params, auth=(token, ''))
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"New Code Period: {json.dumps(data, indent=2)}")
else:
    print(f"Error: {response.text}")

print("\n" + "="*60)

# Also check project metrics to see if new code metrics exist at project level
url2 = f"{base_url}/api/measures/component"
params2 = {
    'component': project_key,
    'metricKeys': 'new_coverage,new_lines_to_cover,new_uncovered_lines'
}

print(f"\nChecking project-level new code metrics...")
print(f"URL: {url2}")

response2 = requests.get(url2, params=params2, auth=(token, ''))
print(f"Status: {response2.status_code}")

if response2.status_code == 200:
    data2 = response2.json()
    component = data2.get('component', {})
    measures = component.get('measures', [])
    
    print(f"\nProject: {component.get('key')}")
    print(f"Measures:")
    for measure in measures:
        print(f"  {measure['metric']}: {measure.get('value', 'N/A')}")
    
    if not measures:
        print("  No new code metrics found at project level")
else:
    print(f"Error: {response2.text}")
