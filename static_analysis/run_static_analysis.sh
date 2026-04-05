#!/bin/bash
echo "Running Bandit security analysis..."
bandit -r . -x ./__pycache__,./db,./apache,./data --format txt -o static_analysis/bandit_report.txt
echo "Bandit done."

echo ""
echo "Running Radon complexity analysis..."
radon cc . -s -a --exclude "__pycache__" > static_analysis/radon_report.txt
echo "Radon done."

echo ""
echo "Both reports saved in static_analysis/"
