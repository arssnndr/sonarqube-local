"""
Example: Automated SonarQube Analysis with AI
Demonstrates how to integrate with AI APIs for automated analysis
"""

import os
import json
import sys
from export_sonarqube_data import SonarQubeExporter
from analyze_sonarqube_report import SonarQubeAnalyzer

def analyze_with_ai_api(prompt: str, api_type: str = "openai"):
    """
    Example function to send prompt to AI API
    
    Args:
        prompt: The analysis prompt
        api_type: Type of AI API (openai, anthropic, etc.)
    
    Returns:
        AI analysis response
    """
    
    if api_type == "openai":
        # Example with OpenAI API
        try:
            import openai
            
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are an expert software quality analyst specializing in code review and security assessment."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            return response.choices[0].message.content
            
        except ImportError:
            print("⚠️  OpenAI library not installed. Install with: pip install openai")
            return None
        except Exception as e:
            print(f"❌ Error calling OpenAI API: {e}")
            return None
    
    elif api_type == "anthropic":
        # Example with Anthropic Claude API
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            
            message = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return message.content[0].text
            
        except ImportError:
            print("⚠️  Anthropic library not installed. Install with: pip install anthropic")
            return None
        except Exception as e:
            print(f"❌ Error calling Anthropic API: {e}")
            return None
    
    else:
        print(f"❌ Unsupported API type: {api_type}")
        return None


def full_automated_analysis(project_key: str, sonarqube_url: str, ai_api: str = "openai"):
    """
    Complete automated workflow: Export → Analyze → Get AI insights
    
    Args:
        project_key: SonarQube project key
        sonarqube_url: SonarQube server URL
        ai_api: AI API to use (openai, anthropic)
    """
    
    print("="*70)
    print("🤖 AUTOMATED SONARQUBE ANALYSIS WITH AI")
    print("="*70)
    print(f"Project: {project_key}")
    print(f"SonarQube: {sonarqube_url}")
    print(f"AI API: {ai_api}")
    print()
    
    # Step 1: Export data from SonarQube
    print("[1/3] 📊 Exporting data from SonarQube...")
    try:
        exporter = SonarQubeExporter(sonarqube_url)
        report = exporter.export_full_report(project_key)
        report_file = f"sonarqube_report_{project_key}_automated.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Data exported successfully")
    except Exception as e:
        print(f"❌ Export failed: {e}")
        return
    
    # Step 2: Generate AI prompt
    print("\n[2/3] 🔍 Generating AI analysis prompt...")
    try:
        analyzer = SonarQubeAnalyzer(report_file)
        prompt = analyzer.generate_ai_prompt()
        print(f"✅ Prompt generated ({len(prompt)} characters)")
    except Exception as e:
        print(f"❌ Prompt generation failed: {e}")
        return
    
    # Step 3: Get AI analysis
    print(f"\n[3/3] 🤖 Getting AI analysis from {ai_api}...")
    analysis = analyze_with_ai_api(prompt, ai_api)
    
    if analysis:
        # Save analysis result
        output_file = f"ai_analysis_{project_key}_automated.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# AI Analysis Report - {project_key}\n\n")
            f.write(f"**Generated**: {analyzer.report['export_info']['export_date']}\n\n")
            f.write(f"**AI Model**: {ai_api}\n\n")
            f.write("---\n\n")
            f.write(analysis)
        
        print(f"✅ AI analysis completed and saved to: {output_file}")
        print("\n" + "="*70)
        print("📋 ANALYSIS PREVIEW")
        print("="*70)
        print(analysis[:1000] + "...\n")
        print(f"Full analysis saved in: {output_file}")
    else:
        print("❌ AI analysis failed")
        print("\n💡 Alternative: Use the generated prompt manually")
        prompt_file = f"ai_analysis_prompt_{project_key}_manual.md"
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(prompt)
        print(f"   Prompt saved to: {prompt_file}")


def main():
    """Main function for automated analysis"""
    
    if len(sys.argv) < 2:
        print("Usage: python automated_analysis.py <project_key> [sonarqube_url] [ai_api]")
        print("\nArguments:")
        print("  project_key    : SonarQube project key (required)")
        print("  sonarqube_url  : SonarQube server URL (default: http://localhost:9002)")
        print("  ai_api         : AI API to use - openai or anthropic (default: openai)")
        print("\nExamples:")
        print("  python automated_analysis.py wec-fe-device-bundling")
        print("  python automated_analysis.py wec-fe-device-bundling http://localhost:9002 openai")
        print("  python automated_analysis.py my-project http://sonar.company.com anthropic")
        print("\nEnvironment Variables:")
        print("  OPENAI_API_KEY     : Required for OpenAI API")
        print("  ANTHROPIC_API_KEY  : Required for Anthropic API")
        sys.exit(1)
    
    project_key = sys.argv[1]
    sonarqube_url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:9002"
    ai_api = sys.argv[3] if len(sys.argv) > 3 else "openai"
    
    # Validate API key
    if ai_api == "openai" and not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("   Set it with: export OPENAI_API_KEY='your-api-key'")
        sys.exit(1)
    elif ai_api == "anthropic" and not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        print("   Set it with: export ANTHROPIC_API_KEY='your-api-key'")
        sys.exit(1)
    
    # Run automated analysis
    full_automated_analysis(project_key, sonarqube_url, ai_api)


if __name__ == "__main__":
    main()
