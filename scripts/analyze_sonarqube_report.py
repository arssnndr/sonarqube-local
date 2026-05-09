#!/usr/bin/env python3
"""
SonarQube Report Analyzer with AI
Menganalisis report SonarQube menggunakan AI untuk memberikan insights dan rekomendasi
"""

import json
import sys
import os
from typing import Dict, List, Any
from datetime import datetime

class SonarQubeAnalyzer:
    def __init__(self, report_file: str):
        """Load SonarQube report"""
        with open(report_file, 'r', encoding='utf-8') as f:
            self.report = json.load(f)
        
        self.project_key = self.report['export_info']['project_key']
        self.summary = self.report['summary']
        self.metrics = self.report['metrics']
        self.issues = self.report['issues']
        self.hotspots = self.report['security_hotspots']
        self.quality_gate = self._parse_quality_gate()
    
    def generate_ai_prompt(self) -> str:
        """Generate comprehensive prompt untuk AI analysis"""
        
        # Prepare issue samples
        top_bugs = self._get_top_issues(self.issues['categorized']['bugs'], 10)
        top_vulnerabilities = self._get_top_issues(self.issues['categorized']['vulnerabilities'], 10)
        top_code_smells = self._get_top_issues(self.issues['categorized']['code_smells'], 20)
        critical_issues = self._get_critical_issues(10)
        
        # Quality Gate status icon
        qg_status = self.metrics.get('alert_status', 'N/A')
        qg_icon = '✅' if qg_status == 'OK' else '❌'
        
        prompt = f"""# Analisis SonarQube Report - {self.project_key}

## 📊 Overview
- **Project**: {self.project_key}
- **Scan Date**: {self.report['export_info']['export_date']}
- **Dashboard**: {self.report['export_info']['dashboard_url']}

## 📈 Metrics Summary
- **Lines of Code**: {self.metrics.get('ncloc', 'N/A')}
- **Code Coverage**: {self.metrics.get('coverage', 'N/A')}%
- **Duplications**: {self.metrics.get('duplicated_lines_density', 'N/A')}%
- **Technical Debt**: {self.metrics.get('sqale_index', 'N/A')} minutes
- **Reliability Rating**: {self.metrics.get('reliability_rating', 'N/A')}
- **Security Rating**: {self.metrics.get('security_rating', 'N/A')}
- **Maintainability Rating**: {self.metrics.get('sqale_rating', 'N/A')}
- **Quality Gate Status**: {qg_icon} {qg_status}

{self._format_quality_gate_details()}

## 🐛 Issues Summary
- **Total Issues**: {self.summary['total_issues']}
  - Bugs: {self.summary['bugs']}
  - Vulnerabilities: {self.summary['vulnerabilities']}
  - Code Smells: {self.summary['code_smells']}
  - Security Hotspots: {self.summary['security_hotspots']}

### Severity Breakdown:
{self._format_severity_breakdown()}

## 🔴 Critical & Blocker Issues
{self._format_issues_for_prompt(critical_issues, "Critical/Blocker")}

## 🐛 Top Bugs
{self._format_issues_for_prompt(top_bugs, "Bugs")}

## 🔒 Top Vulnerabilities
{self._format_issues_for_prompt(top_vulnerabilities, "Vulnerabilities")}

## 💡 Top Code Smells
{self._format_issues_for_prompt(top_code_smells, "Code Smells")}

## 🔥 Security Hotspots
{self._format_hotspots_for_prompt()}

{self._format_file_coverage()}

## 📋 Analisis yang Dibutuhkan

Sebagai expert software quality analyst, tolong analisis report SonarQube di atas dan berikan:

1. **Executive Summary**
   - Overall code quality assessment
   - Tingkat risiko (Low/Medium/High/Critical)
   - Prioritas utama yang harus ditangani
   - Penjelasan mengapa Quality Gate {qg_status} dan dampaknya

2. **Quality Gate Analysis**
   - Analisis detail untuk setiap failed condition
   - Root cause dari Quality Gate failure
   - Impact terhadap production readiness
   - Rekomendasi spesifik untuk pass Quality Gate

3. **Critical Issues Analysis**
   - Analisis detail untuk setiap critical/blocker issue
   - Dampak potensial terhadap aplikasi
   - Rekomendasi fix yang spesifik

4. **Security Assessment**
   - Evaluasi security vulnerabilities dan hotspots
   - Potensi attack vectors
   - Rekomendasi security hardening

5. **Code Quality Insights**
   - Pattern issues yang sering muncul
   - Area kode yang perlu refactoring
   - Best practices yang dilanggar

6. **Technical Debt Analysis**
   - Estimasi effort untuk menyelesaikan issues
   - Prioritization roadmap
   - Quick wins vs long-term improvements

7. **Actionable Recommendations**
   - Top priority fixes (terutama untuk Quality Gate)
   - Langkah-langkah konkret untuk improvement
   - Preventive measures untuk ke depannya

8. **Metrics Improvement Plan**
   - Target metrics yang realistis untuk pass Quality Gate
   - Strategi untuk meningkatkan coverage (especially new code coverage)
   - Cara mengurangi duplications dan technical debt
   - Timeline dan milestones yang achievable

Berikan analisis yang mendalam, actionable, dan prioritized berdasarkan impact dan effort.
"""
        
        return prompt
    
    def _get_top_issues(self, issues: List[Dict], limit: int) -> List[Dict]:
        """Get top issues sorted by severity"""
        severity_order = {'BLOCKER': 0, 'CRITICAL': 1, 'MAJOR': 2, 'MINOR': 3, 'INFO': 4}
        sorted_issues = sorted(issues, key=lambda x: severity_order.get(x.get('severity', 'INFO'), 5))
        return sorted_issues[:limit]
    
    def _get_critical_issues(self, limit: int) -> List[Dict]:
        """Get critical and blocker issues"""
        critical = self.issues['categorized']['by_severity'].get('CRITICAL', [])
        blocker = self.issues['categorized']['by_severity'].get('BLOCKER', [])
        return (blocker + critical)[:limit]
    
    def _format_severity_breakdown(self) -> str:
        """Format severity breakdown"""
        lines = []
        for severity, count in self.summary['by_severity'].items():
            if count > 0:
                lines.append(f"- {severity}: {count}")
        return '\n'.join(lines) if lines else "- No issues"
    
    def _format_issues_for_prompt(self, issues: List[Dict], category: str) -> str:
        """Format issues for AI prompt"""
        if not issues:
            return f"No {category} found."
        
        lines = []
        for i, issue in enumerate(issues, 1):
            lines.append(f"\n### {i}. [{issue.get('severity')}] {issue.get('message', 'No message')}")
            lines.append(f"- **Type**: {issue.get('type')}")
            lines.append(f"- **Rule**: {issue.get('rule')}")
            lines.append(f"- **Component**: {issue.get('component', 'N/A').split(':')[-1]}")
            
            if 'line' in issue:
                lines.append(f"- **Line**: {issue.get('line')}")
            
            if 'effort' in issue:
                lines.append(f"- **Effort**: {issue.get('effort')}")
            
            # Add tags if available
            if issue.get('tags'):
                lines.append(f"- **Tags**: {', '.join(issue.get('tags'))}")
        
        return '\n'.join(lines)
    
    def _format_hotspots_for_prompt(self) -> str:
        """Format security hotspots"""
        if not self.hotspots:
            return "No security hotspots found."
        
        lines = []
        for i, hotspot in enumerate(self.hotspots[:10], 1):
            lines.append(f"\n### {i}. {hotspot.get('message', 'No message')}")
            lines.append(f"- **Security Category**: {hotspot.get('securityCategory')}")
            lines.append(f"- **Vulnerability Probability**: {hotspot.get('vulnerabilityProbability')}")
            lines.append(f"- **Component**: {hotspot.get('component', 'N/A').split(':')[-1]}")
            
            if 'line' in hotspot:
                lines.append(f"- **Line**: {hotspot.get('line')}")
        
        return '\n'.join(lines)
    
    def _parse_quality_gate(self) -> Dict[str, Any]:
        """Parse quality gate details from metrics"""
        qg_details_str = self.metrics.get('quality_gate_details')
        if qg_details_str:
            try:
                return json.loads(qg_details_str)
            except:
                return None
        return None
    
    def _format_quality_gate_details(self) -> str:
        """Format quality gate details for prompt"""
        if not self.quality_gate:
            return ""
        
        lines = ["\n## 🚦 Quality Gate Details\n"]
        
        status = self.quality_gate.get('level', 'UNKNOWN')
        status_icon = "✅" if status == "OK" else "❌"
        
        lines.append(f"**Status**: {status_icon} {status}\n")
        
        conditions = self.quality_gate.get('conditions', [])
        if conditions:
            lines.append("### Conditions:\n")
            
            passed = [c for c in conditions if c.get('level') == 'OK']
            failed = [c for c in conditions if c.get('level') == 'ERROR']
            
            lines.append(f"- ✅ Passed: {len(passed)}/{len(conditions)}")
            lines.append(f"- ❌ Failed: {len(failed)}/{len(conditions)}\n")
            
            if failed:
                lines.append("### ❌ Failed Conditions:\n")
                for condition in failed:
                    metric = condition.get('metric', 'unknown')
                    actual = condition.get('actual', 'N/A')
                    threshold = condition.get('error', 'N/A')
                    op = condition.get('op', '')
                    
                    # Format metric name
                    metric_name = metric.replace('_', ' ').title()
                    
                    # Determine operator symbol
                    op_symbol = {
                        'LT': '<',
                        'GT': '>',
                        'EQ': '=',
                        'NE': '≠'
                    }.get(op, op)
                    
                    lines.append(f"- **{metric_name}**")
                    lines.append(f"  - Actual: {actual}")
                    lines.append(f"  - Required: {op_symbol} {threshold}")
                    
                    # Add specific warning for coverage issues
                    if 'coverage' in metric.lower():
                        lines.append(f"  - ⚠️ **ACTION REQUIRED**: Need to increase test coverage!")
                    
                    lines.append("")
        
        return '\n'.join(lines)
    
    def _format_file_coverage(self) -> str:
        """Format file coverage details for files that need improvement"""
        file_coverage = self.report.get('file_coverage', [])
        
        if not file_coverage:
            return ""
        
        # Check if we have new code data or overall coverage data
        has_new_code = file_coverage[0].get('new_coverage') is not None if file_coverage else False
        
        lines = ["\n## 📁 Files Needing Coverage Improvement\n"]
        
        if has_new_code:
            lines.append("Files with new code that have low coverage:\n")
            
            # Filter files with low new coverage (below 80%)
            low_coverage_files = [f for f in file_coverage if f['new_coverage'] < 80]
            
            if not low_coverage_files:
                lines.append("✅ All files with new code have adequate coverage (≥80%)!\n")
                return '\n'.join(lines)
            
            lines.append(f"Found {len(low_coverage_files)} file(s) with new coverage below 80%:\n")
            
            # Show top 20 files that need most improvement
            for i, file_info in enumerate(low_coverage_files[:20], 1):
                lines.append(f"### {i}. {file_info['path']}")
                lines.append(f"- **New Coverage**: {file_info['new_coverage']:.1f}% ❌")
                lines.append(f"- **New Lines to Cover**: {file_info['new_lines_to_cover']}")
                lines.append(f"- **New Uncovered Lines**: {file_info['new_uncovered_lines']}")
                lines.append(f"- **Overall Coverage**: {file_info['overall_coverage']:.1f}%")
                
                # Calculate how many lines need tests
                lines_need_tests = file_info['new_uncovered_lines']
                target_coverage = 80
                current_coverage = file_info['new_coverage']
                improvement_needed = target_coverage - current_coverage
                
                lines.append(f"- **Improvement Needed**: +{improvement_needed:.1f}% (≈{lines_need_tests} lines need tests)")
                lines.append("")
            
            if len(low_coverage_files) > 20:
                lines.append(f"\n... and {len(low_coverage_files) - 20} more files.\n")
            
            # Summary statistics
            total_new_lines = sum(f['new_lines_to_cover'] for f in low_coverage_files)
            total_uncovered = sum(f['new_uncovered_lines'] for f in low_coverage_files)
            avg_coverage = sum(f['new_coverage'] for f in low_coverage_files) / len(low_coverage_files)
            
            lines.append("### 📊 Summary:")
            lines.append(f"- Total new lines to cover: {total_new_lines}")
            lines.append(f"- Total uncovered new lines: {total_uncovered}")
            lines.append(f"- Average new coverage: {avg_coverage:.1f}%")
            lines.append(f"- **To pass Quality Gate**: Need to add tests for approximately {total_uncovered} lines of new code")
        else:
            # Show files with lowest overall coverage
            lines.append("⚠️ **Note**: New code metrics not available. Showing files with lowest overall coverage instead.\n")
            lines.append("Files with lowest overall coverage (candidates for improvement):\n")
            
            # Show top 20 files with lowest coverage
            for i, file_info in enumerate(file_coverage[:20], 1):
                coverage = file_info['overall_coverage']
                uncovered = file_info['uncovered_lines']
                total_lines = file_info['lines_to_cover']
                
                status = "✅" if coverage >= 80 else "⚠️" if coverage >= 60 else "❌"
                
                lines.append(f"### {i}. {file_info['path']}")
                lines.append(f"- **Coverage**: {coverage:.1f}% {status}")
                lines.append(f"- **Lines to Cover**: {total_lines}")
                lines.append(f"- **Uncovered Lines**: {uncovered}")
                
                if coverage < 80:
                    target = 80
                    improvement = target - coverage
                    lines.append(f"- **To reach 80%**: Need to cover ≈{int(uncovered * improvement / (100 - coverage))} more lines")
                
                lines.append("")
            
            if len(file_coverage) > 20:
                lines.append(f"\n... and {len(file_coverage) - 20} more files.\n")
            
            # Summary statistics
            avg_coverage = sum(f['overall_coverage'] for f in file_coverage) / len(file_coverage)
            total_uncovered = sum(f['uncovered_lines'] for f in file_coverage)
            files_below_80 = len([f for f in file_coverage if f['overall_coverage'] < 80])
            
            lines.append("### 📊 Summary:")
            lines.append(f"- Total files analyzed: {len(file_coverage)}")
            lines.append(f"- Files below 80% coverage: {files_below_80}")
            lines.append(f"- Average coverage: {avg_coverage:.1f}%")
            lines.append(f"- Total uncovered lines: {total_uncovered}")
            lines.append(f"\n💡 **Recommendation**: Focus on adding tests to files with coverage below 80% to improve overall quality.")
        
        return '\n'.join(lines)
    
    def print_statistics(self):
        """Print statistics summary"""
        print("\n" + "="*60)
        print("📋 RINGKASAN ANALISIS SONARQUBE")
        print("="*60)
        print(f"\n🔍 Total Issues: {self.summary['total_issues']}")
        print(f"  🐛 Bugs: {self.summary['bugs']}")
        print(f"  🔒 Vulnerabilities: {self.summary['vulnerabilities']}")
        print(f"  💡 Code Smells: {self.summary['code_smells']}")
        print(f"  🔥 Security Hotspots: {self.summary['security_hotspots']}")
        
        print(f"\n📊 Severity Breakdown:")
        for severity, count in self.summary['by_severity'].items():
            if count > 0:
                print(f"  {severity}: {count}")
        
        print(f"\n📈 Key Metrics:")
        print(f"  Lines of Code: {self.metrics.get('ncloc', 'N/A')}")
        print(f"  Coverage: {self.metrics.get('coverage', 'N/A')}%")
        print(f"  Duplications: {self.metrics.get('duplicated_lines_density', 'N/A')}%")
        print(f"  Technical Debt: {self.metrics.get('sqale_index', 'N/A')} min")
        
        print("\n" + "="*60 + "\n")
    
    def save_ai_prompt(self, output_file: str = None):
        """Save AI prompt to file"""
        if output_file is None:
            output_file = f"reports/ai_analysis_prompt_{self.project_key}.md"
        
        # Ensure parent directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Delete old prompt if exists
        if os.path.exists(output_file):
            os.remove(output_file)
        
        prompt = self.generate_ai_prompt()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        print(f"✅ AI analysis prompt saved to: {output_file}")
        print(f"\n📝 Prompt length: {len(prompt)} characters")
        print(f"📊 Issues included:")
        print(f"   - Critical/Blocker: {len(self._get_critical_issues(10))}")
        print(f"   - Bugs: {min(len(self.issues['categorized']['bugs']), 10)}")
        print(f"   - Vulnerabilities: {min(len(self.issues['categorized']['vulnerabilities']), 10)}")
        print(f"   - Code Smells: {min(len(self.issues['categorized']['code_smells']), 20)}")
        print(f"   - Security Hotspots: {min(len(self.hotspots), 10)}")
        
        return output_file
    
    def generate_statistics(self) -> Dict[str, Any]:
        """Generate detailed statistics"""
        stats = {
            'overview': {
                'project': self.project_key,
                'total_issues': self.summary['total_issues'],
                'lines_of_code': self.metrics.get('ncloc', 0),
                'technical_debt_minutes': self.metrics.get('sqale_index', 0)
            },
            'issue_distribution': {
                'by_type': {
                    'bugs': self.summary['bugs'],
                    'vulnerabilities': self.summary['vulnerabilities'],
                    'code_smells': self.summary['code_smells']
                },
                'by_severity': self.summary['by_severity']
            },
            'quality_metrics': {
                'coverage': float(self.metrics.get('coverage', 0)),
                'duplications': float(self.metrics.get('duplicated_lines_density', 0)),
                'reliability_rating': self.metrics.get('reliability_rating', 'N/A'),
                'security_rating': self.metrics.get('security_rating', 'N/A'),
                'maintainability_rating': self.metrics.get('sqale_rating', 'N/A')
            },
            'top_rules_violated': self._get_top_rules_violated(),
            'files_with_most_issues': self._get_files_with_most_issues()
        }
        
        return stats
    
    def _get_top_rules_violated(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most violated rules"""
        rule_counts = {}
        
        for issue in self.issues['all']:
            rule = issue.get('rule')
            if rule:
                if rule not in rule_counts:
                    rule_counts[rule] = {
                        'rule': rule,
                        'count': 0,
                        'message': issue.get('message', ''),
                        'type': issue.get('type', '')
                    }
                rule_counts[rule]['count'] += 1
        
        sorted_rules = sorted(rule_counts.values(), key=lambda x: x['count'], reverse=True)
        return sorted_rules[:limit]
    
    def _get_files_with_most_issues(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get files with most issues"""
        file_counts = {}
        
        for issue in self.issues['all']:
            component = issue.get('component', '')
            if component:
                # Extract filename from component
                filename = component.split(':')[-1]
                if filename not in file_counts:
                    file_counts[filename] = {
                        'file': filename,
                        'count': 0,
                        'bugs': 0,
                        'vulnerabilities': 0,
                        'code_smells': 0
                    }
                
                file_counts[filename]['count'] += 1
                issue_type = issue.get('type', '').lower()
                if issue_type == 'bug':
                    file_counts[filename]['bugs'] += 1
                elif issue_type == 'vulnerability':
                    file_counts[filename]['vulnerabilities'] += 1
                elif issue_type == 'code_smell':
                    file_counts[filename]['code_smells'] += 1
        
        sorted_files = sorted(file_counts.values(), key=lambda x: x['count'], reverse=True)
        return sorted_files[:limit]
    
    def print_statistics(self):
        """Print detailed statistics"""
        stats = self.generate_statistics()
        
        print("\n" + "="*70)
        print("📊 DETAILED STATISTICS")
        print("="*70)
        
        print(f"\n🎯 Overview:")
        print(f"  Project: {stats['overview']['project']}")
        print(f"  Total Issues: {stats['overview']['total_issues']}")
        print(f"  Lines of Code: {stats['overview']['lines_of_code']}")
        print(f"  Technical Debt: {stats['overview']['technical_debt_minutes']} minutes")
        
        print(f"\n📈 Quality Metrics:")
        print(f"  Coverage: {stats['quality_metrics']['coverage']}%")
        print(f"  Duplications: {stats['quality_metrics']['duplications']}%")
        print(f"  Reliability: {stats['quality_metrics']['reliability_rating']}")
        print(f"  Security: {stats['quality_metrics']['security_rating']}")
        print(f"  Maintainability: {stats['quality_metrics']['maintainability_rating']}")
        
        print(f"\n🔝 Top Rules Violated:")
        for i, rule in enumerate(stats['top_rules_violated'][:5], 1):
            print(f"  {i}. {rule['rule']} ({rule['count']} times)")
            print(f"     {rule['message'][:80]}...")
        
        print(f"\n📁 Files with Most Issues:")
        for i, file_info in enumerate(stats['files_with_most_issues'][:5], 1):
            print(f"  {i}. {file_info['file']} ({file_info['count']} issues)")
            print(f"     Bugs: {file_info['bugs']}, Vulnerabilities: {file_info['vulnerabilities']}, Code Smells: {file_info['code_smells']}")
        
        print("\n" + "="*70)


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python analyze_sonarqube_report.py <report_file> [--output OUTPUT_FILE]")
        print("\nExample:")
        print("  python analyze_sonarqube_report.py report.json")
        print("  python analyze_sonarqube_report.py report.json --output prompt.md")
        print("  python analyze_sonarqube_report.py report.json prompt.md")
        sys.exit(1)
    
    report_file = sys.argv[1]
    output_file = None
    
    # Parse arguments - handle --output flag
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg == '--output' and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]
            i += 2
        elif not output_file and not arg.startswith('-'):
            # Backward compatibility: positional output_file
            output_file = arg
            i += 1
        else:
            i += 1
    
    try:
        print(f"📖 Loading report: {report_file}")
        analyzer = SonarQubeAnalyzer(report_file)
        
        print(f"🔍 Analyzing project: {analyzer.project_key}")
        
        # Print statistics
        analyzer.print_statistics()
        
        # Generate AI prompt
        print(f"\n🤖 Generating AI analysis prompt...")
        prompt_file = analyzer.save_ai_prompt(output_file)
        
        print(f"\n✨ Done! You can now:")
        print(f"   1. Copy the content of '{prompt_file}' to your AI assistant")
        print(f"   2. Or use it with AI API for automated analysis")
        
    except FileNotFoundError:
        print(f"❌ Error: File '{report_file}' not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON file")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
