# scripts\test.ps1
# Run the full pytest suite with coverage.
#
# Run from the project root:
#   .\scripts\test.ps1
#
# Optional: pass extra pytest args
#   .\scripts\test.ps1 -k test_timeframe -v

#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

param(
    [Parameter(ValueFromRemainingArguments)]
    [string[]]$PytestArgs
)

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "==> Running pytest ..." -ForegroundColor Cyan

if ($PytestArgs) {
    pytest @PytestArgs
} else {
    pytest
}
