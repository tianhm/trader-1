Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-Step([string]$Message) {
    Write-Host "`n==> $Message" -ForegroundColor Cyan
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$bridgeRoot = Split-Path -Parent $scriptDir
$targetApiRoot = Join-Path $bridgeRoot "api"

# 固定源路径：后续只需更新 backend-ctp/api，再执行本脚本即可
$sourceApiRoot = "D:\github\backend-ctp\api"

$srcWin = Join-Path $sourceApiRoot "win"
$srcLinux = Join-Path $sourceApiRoot "linux"

if (-not (Test-Path $srcWin)) {
    throw "Source win dir not found: $srcWin"
}
if (-not (Test-Path $srcLinux)) {
    throw "Source linux dir not found: $srcLinux"
}

Write-Step "Sync Thost API files from fixed source"
New-Item -ItemType Directory -Path $targetApiRoot -Force | Out-Null
Copy-Item -Path $srcWin -Destination $targetApiRoot -Recurse -Force
Copy-Item -Path $srcLinux -Destination $targetApiRoot -Recurse -Force

Write-Step "Done"
Write-Host "Synced to: $targetApiRoot" -ForegroundColor Green
