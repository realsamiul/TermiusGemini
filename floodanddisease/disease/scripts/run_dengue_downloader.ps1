# PowerShell Script to Run Comprehensive Dengue Downloader
# This script will download all dengue status reports between 2022-2024 from DGHS Bangladesh

Write-Host "DENGUE DATA DOWNLOADER - DGHS Bangladesh" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Write-Host ""

# Step 1: Check if Python is installed
Write-Host "Step 1: Checking Python installation..." -ForegroundColor Yellow
$pythonCheck = Get-Command python -ErrorAction SilentlyContinue
if ($pythonCheck) {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Python not found. Please install Python first." -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Cyan
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 2: Install required packages
Write-Host ""
Write-Host "Step 2: Installing required Python packages..." -ForegroundColor Yellow
pip install requests beautifulsoup4 lxml pathlib2
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Packages installed successfully" -ForegroundColor Green
} else {
    Write-Host "⚠️ Some packages may not have installed correctly, but continuing..." -ForegroundColor Yellow
}

# Step 3: Run the dengue downloader
Write-Host ""
Write-Host "Step 3: Running the comprehensive dengue downloader..." -ForegroundColor Yellow
Write-Host "This will download all dengue reports from 2022-2024" -ForegroundColor Cyan
Write-Host ""

python comprehensive_dengue_downloader.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Download process completed!" -ForegroundColor Green
    Write-Host "📁 Check the 'dengue_reports_2022_2024' folder for downloaded files" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "❌ Download process encountered errors. Check the log files for details." -ForegroundColor Red
}

Write-Host ""
Write-Host "Press Enter to exit..." -ForegroundColor Gray
Read-Host