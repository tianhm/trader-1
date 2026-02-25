param(
    [string]$BuildDir = "build",
    [string]$Config = "Release"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-Step([string]$Message) {
    Write-Host "`n==> $Message" -ForegroundColor Cyan
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$bridgeRoot = Split-Path -Parent $scriptDir

Write-Step "Configure CMake"
Set-Location $bridgeRoot
& cmake -S . -B $BuildDir
if ($LASTEXITCODE -ne 0) {
    throw "cmake configure failed with exit code: $LASTEXITCODE"
}

Write-Step "Build module"
& cmake --build $BuildDir --config $Config --parallel
if ($LASTEXITCODE -ne 0) {
    throw "cmake build failed with exit code: $LASTEXITCODE"
}

Write-Step "Done"
Write-Host "Build output: $bridgeRoot/$BuildDir" -ForegroundColor Green
