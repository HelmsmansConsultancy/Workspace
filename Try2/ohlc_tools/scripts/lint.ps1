# scripts\lint.ps1
# Run ruff, black (check mode), and mypy.
#
# Run from the project root:
#   .\scripts\lint.ps1

#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "==> ruff ..." -ForegroundColor Cyan
ruff check ohlc_tools tests

Write-Host "==> black (check) ..." -ForegroundColor Cyan
black --check ohlc_tools tests

Write-Host "==> mypy ..." -ForegroundColor Cyan
mypy ohlc_tools

Write-Host ""
Write-Host "All checks passed." -ForegroundColor Green
