import json

# Load report
with open('sonarqube_report_wec-fe-device-bundling_20260509_105246.json', 'r') as f:
    data = json.load(f)

# Parse quality gate details
qg_details = json.loads(data['metrics']['quality_gate_details'])

print("="*70)
print("🚦 QUALITY GATE ANALYSIS")
print("="*70)
print(f"\nStatus: {qg_details['level']}")
print(f"\nConditions:")
print("-"*70)

for condition in qg_details['conditions']:
    metric = condition['metric']
    level = condition['level']
    actual = condition.get('actual', 'N/A')
    threshold = condition.get('error', 'N/A')
    operator = condition.get('op', '')
    
    status_icon = "✅" if level == "OK" else "❌"
    
    print(f"\n{status_icon} {metric}")
    print(f"   Status: {level}")
    print(f"   Actual: {actual}")
    print(f"   Threshold: {operator} {threshold}")
    
    if level == "ERROR":
        print(f"   ⚠️  FAILED: Coverage untuk new code terlalu rendah!")

print("\n" + "="*70)
print("\n📋 SUMMARY:")
print("-"*70)

failed = [c for c in qg_details['conditions'] if c['level'] == 'ERROR']
passed = [c for c in qg_details['conditions'] if c['level'] == 'OK']

print(f"✅ Passed: {len(passed)}/{len(qg_details['conditions'])}")
print(f"❌ Failed: {len(failed)}/{len(qg_details['conditions'])}")

if failed:
    print(f"\n🔴 Failed Conditions:")
    for c in failed:
        print(f"   - {c['metric']}: {c.get('actual')} (required: {c.get('op')} {c.get('error')})")

print("\n" + "="*70)
