Write-Host "Running Bandit security analysis..."
bandit -r . -x ./__pycache__,./db,./apache,./data --format txt -o static_analysis/bandit_report.txt
Write-Host "Bandit done. Report saved to static_analysis/bandit_report.txt"

Write-Host ""
Write-Host "Running Radon complexity analysis..."
radon cc . -s -a --exclude "__pycache__" > static_analysis/radon_report.txt
Write-Host "Radon done. Report saved to static_analysis/radon_report.txt"

Write-Host ""
Write-Host "Both reports saved in static_analysis/"
