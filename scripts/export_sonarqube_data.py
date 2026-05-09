#!/usr/bin/env python3
"""
SonarQube Data Exporter
Mengekspor data analisis dari SonarQube untuk analisis AI
"""

import requests
import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

def load_env_file(env_path: str = '.env'):
    """Load environment variables from .env file"""
    env_file = Path(env_path)
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        # Only set if not already in environment
                        if key not in os.environ:
                            os.environ[key] = value

class SonarQubeExporter:
    def __init__(self, base_url: str, token: str = None):
        """
        Initialize SonarQube exporter
        
        Args:
            base_url: SonarQube server URL (e.g., http://localhost:9002)
            token: Authentication token (optional untuk server lokal)
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        if token:
            self.session.auth = (token, '')
        
    def get_project_metrics(self, project_key: str) -> Dict[str, Any]:
        """Ambil metrics utama project"""
        metrics = [
            'bugs', 'vulnerabilities', 'code_smells', 'security_hotspots',
            'coverage', 'duplicated_lines_density', 'ncloc', 'sqale_index',
            'reliability_rating', 'security_rating', 'sqale_rating',
            'alert_status', 'quality_gate_details'
        ]
        
        url = f"{self.base_url}/api/measures/component"
        params = {
            'component': project_key,
            'metricKeys': ','.join(metrics)
        }
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_issues(self, project_key: str, page_size: int = 500) -> List[Dict[str, Any]]:
        """Ambil semua issues (bugs, vulnerabilities, code smells)"""
        url = f"{self.base_url}/api/issues/search"
        all_issues = []
        page = 1
        
        while True:
            params = {
                'componentKeys': project_key,
                'ps': page_size,
                'p': page,
                'resolved': 'false'
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            all_issues.extend(data.get('issues', []))
            
            # Check if there are more pages
            total = data.get('total', 0)
            if page * page_size >= total:
                break
            page += 1
        
        return all_issues
    
    def get_hotspots(self, project_key: str) -> List[Dict[str, Any]]:
        """Ambil security hotspots"""
        url = f"{self.base_url}/api/hotspots/search"
        params = {
            'projectKey': project_key,
            'ps': 500
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('hotspots', [])
        except:
            return []
            raise
    
    def get_duplications(self, project_key: str) -> Dict[str, Any]:
        """Ambil informasi code duplications"""
        url = f"{self.base_url}/api/measures/component"
        params = {
            'component': project_key,
            'metricKeys': 'duplicated_lines,duplicated_blocks,duplicated_files,duplicated_lines_density'
        }
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def categorize_issues(self, issues: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Kategorikan issues berdasarkan type dan severity"""
        categorized = {
            'bugs': [],
            'vulnerabilities': [],
            'code_smells': [],
            'by_severity': {
                'BLOCKER': [],
                'CRITICAL': [],
                'MAJOR': [],
                'MINOR': [],
                'INFO': []
            }
        }
        
        for issue in issues:
            issue_type = issue.get('type', '').lower()
            severity = issue.get('severity', 'INFO')
            
            if issue_type == 'bug':
                categorized['bugs'].append(issue)
            elif issue_type == 'vulnerability':
                categorized['vulnerabilities'].append(issue)
            elif issue_type == 'code_smell':
                categorized['code_smells'].append(issue)
            
            categorized['by_severity'][severity].append(issue)
        
        return categorized
    
    def get_file_coverage(self, project_key: str) -> List[Dict[str, Any]]:
        """Ambil coverage per file untuk new code, fallback ke overall coverage jika new code tidak tersedia"""
        url = f"{self.base_url}/api/measures/component_tree"
        
        # Get files with coverage metrics
        params = {
            'component': project_key,
            'metricKeys': 'new_coverage,new_lines_to_cover,new_uncovered_lines,coverage,lines_to_cover,uncovered_lines',
            'strategy': 'leaves',
            'ps': 500
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            components = data.get('components', [])
            files_with_coverage = []
            has_new_code_data = False
            
            for component in components:
                measures = {}
                for measure in component.get('measures', []):
                    value = measure.get('value')
                    # Skip if value is None or empty string
                    if value is not None and value != '':
                        measures[measure['metric']] = value
                
                # Check if this file has new code metrics
                has_new_lines = 'new_lines_to_cover' in measures
                if has_new_lines:
                    has_new_code_data = True
                    new_lines = float(measures.get('new_lines_to_cover', 0))
                    if new_lines > 0:
                        file_info = {
                            'path': component.get('path', component.get('key', '')),
                            'name': component.get('name', ''),
                            'new_coverage': float(measures.get('new_coverage', 0)),
                            'new_lines_to_cover': int(new_lines),
                            'new_uncovered_lines': int(float(measures.get('new_uncovered_lines', 0))),
                            'overall_coverage': float(measures.get('coverage', 0)) if 'coverage' in measures else 0,
                            'lines_to_cover': int(float(measures.get('lines_to_cover', 0))) if 'lines_to_cover' in measures else 0,
                            'uncovered_lines': int(float(measures.get('uncovered_lines', 0))) if 'uncovered_lines' in measures else 0
                        }
                        files_with_coverage.append(file_info)
            
            # If no new code data found, use overall coverage for files with lowest coverage
            if not has_new_code_data or len(files_with_coverage) == 0:
                print("  ℹ️  No new code metrics available, showing files with lowest overall coverage instead")
                for component in components:
                    measures = {}
                    for measure in component.get('measures', []):
                        value = measure.get('value')
                        if value is not None and value != '':
                            measures[measure['metric']] = value
                    
                    # Only include files that have coverage data
                    if 'coverage' in measures and 'lines_to_cover' in measures:
                        lines_to_cover = int(float(measures.get('lines_to_cover', 0)))
                        if lines_to_cover > 0:  # Only files with code to cover
                            file_info = {
                                'path': component.get('path', component.get('key', '')),
                                'name': component.get('name', ''),
                                'new_coverage': None,  # Not available
                                'new_lines_to_cover': None,
                                'new_uncovered_lines': None,
                                'overall_coverage': float(measures.get('coverage', 0)),
                                'lines_to_cover': lines_to_cover,
                                'uncovered_lines': int(float(measures.get('uncovered_lines', 0)))
                            }
                            files_with_coverage.append(file_info)
                
                # Sort by overall coverage ascending (worst first)
                files_with_coverage.sort(key=lambda x: x['overall_coverage'])
            else:
                # Sort by new_coverage ascending (worst first)
                files_with_coverage.sort(key=lambda x: x['new_coverage'])
            
            return files_with_coverage
        except Exception as e:
            print(f"  ⚠️  Warning: Could not fetch file coverage data: {e}")
            return []
    
    def export_full_report(self, project_key: str, output_file: str = None):
        """Export full analysis report"""
        print(f"📊 Mengekspor data dari project: {project_key}")
        
        # Collect all data
        print("  ⏳ Mengambil metrics...")
        metrics = self.get_project_metrics(project_key)
        
        print("  ⏳ Mengambil issues...")
        issues = self.get_issues(project_key)
        
        print("  ⏳ Mengambil security hotspots...")
        hotspots = self.get_hotspots(project_key)
        
        print("  ⏳ Mengambil duplications...")
        duplications = self.get_duplications(project_key)
        
        print("  ⏳ Mengambil coverage per file...")
        file_coverage = self.get_file_coverage(project_key)
        
        # Categorize issues
        categorized_issues = self.categorize_issues(issues)
        
        # Build report
        report = {
            'export_info': {
                'project_key': project_key,
                'export_date': datetime.now().isoformat(),
                'sonarqube_url': self.base_url,
                'dashboard_url': f"{self.base_url}/dashboard?id={project_key}"
            },
            'summary': {
                'total_issues': len(issues),
                'bugs': len(categorized_issues['bugs']),
                'vulnerabilities': len(categorized_issues['vulnerabilities']),
                'code_smells': len(categorized_issues['code_smells']),
                'security_hotspots': len(hotspots),
                'by_severity': {
                    severity: len(issues_list) 
                    for severity, issues_list in categorized_issues['by_severity'].items()
                }
            },
            'metrics': self._format_metrics(metrics),
            'issues': {
                'all': issues,
                'categorized': categorized_issues
            },
            'security_hotspots': hotspots,
            'duplications': duplications,
            'file_coverage': file_coverage
        }
        
        # Save to file
        if output_file is None:
            output_file = f"reports/sonarqube_report_{project_key}.json"
        
        # Ensure parent directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Delete old report if exists
        if os.path.exists(output_file):
            os.remove(output_file)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Report berhasil diekspor ke: {output_file}")
        self._print_summary(report)
        
        return report
    
    def _format_metrics(self, metrics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format metrics data untuk readability"""
        formatted = {}
        measures = metrics_data.get('component', {}).get('measures', [])
        
        for measure in measures:
            metric = measure.get('metric')
            value = measure.get('value')
            formatted[metric] = value
        
        return formatted
    
    def _print_summary(self, report: Dict[str, Any]):
        """Print summary ke console"""
        summary = report['summary']
        metrics = report['metrics']
        
        print("\n" + "="*60)
        print("📋 RINGKASAN ANALISIS SONARQUBE")
        print("="*60)
        
        print(f"\n🔍 Total Issues: {summary['total_issues']}")
        print(f"  🐛 Bugs: {summary['bugs']}")
        print(f"  🔒 Vulnerabilities: {summary['vulnerabilities']}")
        print(f"  💡 Code Smells: {summary['code_smells']}")
        print(f"  🔥 Security Hotspots: {summary['security_hotspots']}")
        
        print(f"\n📊 Severity Breakdown:")
        for severity, count in summary['by_severity'].items():
            if count > 0:
                print(f"  {severity}: {count}")
        
        print(f"\n📈 Key Metrics:")
        if 'ncloc' in metrics:
            print(f"  Lines of Code: {metrics['ncloc']}")
        if 'coverage' in metrics:
            print(f"  Coverage: {metrics['coverage']}%")
        if 'duplicated_lines_density' in metrics:
            print(f"  Duplications: {metrics['duplicated_lines_density']}%")
        if 'sqale_index' in metrics:
            print(f"  Technical Debt: {metrics['sqale_index']} min")
        
        print("\n" + "="*60)


def main():
    """Main function"""
    # Load .env file if exists
    load_env_file('.env')
    
    # Configuration - bisa diambil dari environment variable atau langsung di set
    SONARQUBE_URL = os.getenv("SONARQUBE_URL", "http://localhost:9002")
    SONARQUBE_TOKEN = os.getenv("SONARQUBE_TOKEN", None)
    
    # Parse arguments
    if len(sys.argv) < 2:
        print("Usage: python export_sonarqube_data.py <project_key> [--output OUTPUT_FILE] [token]")
        print("\nExample:")
        print("  python export_sonarqube_data.py wec-fe-device-bundling")
        print("  python export_sonarqube_data.py wec-fe-device-bundling --output report.json")
        print("  python export_sonarqube_data.py wec-fe-device-bundling report.json your-token")
        print("\nOr set environment variable:")
        print("  export SONARQUBE_TOKEN='your-token'")
        print("  set SONARQUBE_TOKEN=your-token  (Windows)")
        sys.exit(1)
    
    project_key = sys.argv[1]
    output_file = None
    
    # Parse arguments - handle --output flag, output_file, and token
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg == '--output' and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]
            i += 2
        elif arg.startswith('squ_'):
            SONARQUBE_TOKEN = arg
            i += 1
        elif not output_file and not arg.startswith('-'):
            # Backward compatibility: positional output_file
            output_file = arg
            i += 1
        else:
            i += 1
    
    # Check if token is needed
    if not SONARQUBE_TOKEN:
        print("⚠️  Warning: No authentication token provided")
        print("   If SonarQube requires authentication, set SONARQUBE_TOKEN")
        print("   Example: set SONARQUBE_TOKEN=squ_your_token_here")
        print("\n   Trying without authentication...\n")
    
    # Export data
    try:
        exporter = SonarQubeExporter(SONARQUBE_URL, SONARQUBE_TOKEN)
        exporter.export_full_report(project_key, output_file)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print(f"\n❌ Error: Authentication required (401 Unauthorized)")
            print(f"\n📝 How to fix:")
            print(f"   1. Login to SonarQube: {SONARQUBE_URL}")
            print(f"   2. Go to: My Account → Security → Generate Token")
            print(f"   3. Run again with token:")
            print(f"      python export_sonarqube_data.py {project_key} report.json YOUR_TOKEN")
            print(f"   Or set environment variable:")
            print(f"      set SONARQUBE_TOKEN=YOUR_TOKEN")
        else:
            print(f"\n❌ Error: HTTP {e.response.status_code}")
            print(f"   Detail: {e}")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error: Tidak dapat terhubung ke SonarQube")
        print(f"   Pastikan SonarQube berjalan di {SONARQUBE_URL}")
        print(f"   Detail: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
