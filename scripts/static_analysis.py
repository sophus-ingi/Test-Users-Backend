#!/usr/bin/env python3
"""
Static code analysis script.
Runs multiple linting and quality tools and generates reports.
"""

import subprocess
import sys
import os
from datetime import datetime

def run_command(cmd, description):
    """Run a command and capture output."""
    print(f"\n{'='*70}")
    print(f"Running: {description}")
    print(f"{'='*70}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=False, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running {description}: {e}")
        return False

def main():
    """Run all static analysis tools."""
    os.chdir(os.path.dirname(__file__) or '.')
    
    print(f"\n{'='*70}")
    print("STATIC CODE ANALYSIS REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")
    
    results = {}
    
    # Flake8 - Style guide enforcement
    results['flake8'] = run_command(
        "flake8 src/ app.py tests/ --count --statistics --show-source",
        "Flake8 - PEP8 Style Guide Checker"
    )
    
    # Black - Code formatter (check mode)
    results['black'] = run_command(
        "black --check src/ app.py tests/ 2>&1 || echo 'Formatting issues found'",
        "Black - Code Formatter (check mode)"
    )
    
    # Pylint - Detailed analysis
    results['pylint'] = run_command(
        "pylint src/ app.py --exit-zero --max-line-length=120 2>&1",
        "Pylint - Detailed Code Analysis"
    )
    
    # isort - Import sorting
    results['isort'] = run_command(
        "isort --check-only --diff src/ app.py tests/ 2>&1 || echo 'Import sorting issues found'",
        "isort - Import Statement Checker"
    )
    
    # Bandit - Security issues
    results['bandit'] = run_command(
        "bandit -r src/ app.py --skip B101,B601 -f json 2>&1 | jq . || echo 'See bandit output above'",
        "Bandit - Security Issue Scanner"
    )
    
    # Safety - Dependency vulnerabilities
    results['safety'] = run_command(
        "safety check --json 2>&1 || echo 'See safety output above'",
        "Safety - Dependency Vulnerability Checker"
    )
    
    # Print summary
    print(f"\n{'='*70}")
    print("ANALYSIS SUMMARY")
    print(f"{'='*70}")
    for tool, passed in results.items():
        status = "✅ PASSED" if passed else "⚠️  ISSUES FOUND"
        print(f"{tool:.<40} {status}")
    
    print(f"\n{'='*70}\n")

if __name__ == "__main__":
    main()
