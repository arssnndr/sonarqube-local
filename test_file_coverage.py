#!/usr/bin/env python3
"""Test file coverage API"""

import requests
import json
import os

# Load token from .env
with open('.env', 'r') as f:
    for line in f:
        if line.startswith('SONARQUBE_TOKEN='):
            token = line.split('=')[1].strip()
            break

base_url = 'http://localhost:9002'
project_key = 'wec-fe-device-bundling'

# Test API call with period parameter
url = f"{base_url}/api/measures/component_tree"
params = {
    'component': project_key,
    'metricKeys': 'new_coverage,new_lines_to_cover,new_uncovered_lines,coverage,lines_to_cover,uncovered_lines',
    'strategy': 'leaves',
    'ps': 500
}

print(f"Testing API: {url}")
print(f"Params: {params}")
print()

# Use basic auth like the exporter does
response = requests.get(url, params=params, auth=(token, ''))
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    components = data.get('components', [])
    print(f"Total components: {len(components)}")
    print()
    
    # Show files that have ANY new code metrics
    files_with_new_metrics = []
    for comp in components:
        measures = {m['metric']: m.get('value', 'N/A') for m in comp.get('measures', [])}
        has_new_data = any(
            measures.get(m) not in ['N/A', None, ''] 
            for m in ['new_coverage', 'new_lines_to_cover', 'new_uncovered_lines']
        )
        if has_new_data:
            files_with_new_metrics.append({
                'path': comp.get('path', comp.get('key')),
                'measures': measures
            })
    
    print(f"Files with new code metrics: {len(files_with_new_metrics)}")
    
    if files_with_new_metrics:
        print("\nFiles with new code:")
        for f in files_with_new_metrics[:10]:
            print(f"  {f['path']}")
            print(f"    new_coverage: {f['measures'].get('new_coverage', 'N/A')}")
            print(f"    new_lines_to_cover: {f['measures'].get('new_lines_to_cover', 'N/A')}")
            print(f"    new_uncovered_lines: {f['measures'].get('new_uncovered_lines', 'N/A')}")
    else:
        print("\nNo files with new code metrics found.")
        print("\nThis could mean:")
        print("  1. No new code was added in the current analysis period")
        print("  2. New Code Period is not configured in SonarQube")
        print("  3. Need to check SonarQube project settings")
        
        # Show overall coverage for reference
        print("\nFiles with overall coverage (first 10):")
        count = 0
        for comp in components:
            measures = {m['metric']: m.get('value', 'N/A') for m in comp.get('measures', [])}
            if measures.get('coverage') not in ['N/A', None, '']:
                print(f"  {comp.get('path', comp.get('key'))}")
                print(f"    coverage: {measures.get('coverage')}%")
                print(f"    lines_to_cover: {measures.get('lines_to_cover')}")
                print(f"    uncovered_lines: {measures.get('uncovered_lines')}")
                count += 1
                if count >= 10:
                    break
else:
    print(f"Error: {response.text}")
