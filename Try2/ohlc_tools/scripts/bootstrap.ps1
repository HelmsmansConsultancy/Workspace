# scripts\bootstrap.ps1
# Create a virtual environment and install the project with all dev extras.
#
# Run from the project root:
#   .\scripts\bootstrap.ps1
#
# If you get an execution-policy error, run once in an elevated shell:
#   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "==> Creating virtual environment (.venv) ..." -ForegroundColor Cyan
python -m venv .venv

Write-Host "==> Activating .venv ..." -ForegroundColor Cyan
& .\.venv\Scripts\Activate.ps1

Write-Host "==> Upgrading pip ..." -ForegroundColor Cyan
python -m pip install --quiet --upgrade pip

Write-Host "==> Installing ohlc-tools in editable mode with dev extras ..." -ForegroundColor Cyan
pip install --quiet -e ".[dev]"

Write-Host ""
Write-Host "Done!" -ForegroundColor Green
Write-Host "Activate with:  .\.venv\Scripts\Activate.ps1"
Write-Host "Then run:       ohlc --help"
