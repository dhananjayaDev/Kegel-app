# Build Kegel Health Windows desktop app + Inno Setup installer
# Prerequisites: Python venv, Inno Setup 6 (https://jrsoftware.org/isinfo.php)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Error "Create venv first: python -m venv venv"
}

Write-Host "Installing build dependencies..."
& "venv\Scripts\pip.exe" install -r requirements.txt -r desktop\requirements-desktop.txt | Out-Null

Write-Host "Generating app icon from application/static/icons/kegel.png..."
& "venv\Scripts\python.exe" "desktop\make_icon.py"

Write-Host "Building KegelHealth.exe with PyInstaller..."
& "venv\Scripts\pyinstaller.exe" "desktop\kegelhealth.spec" --noconfirm --distpath "dist" --workpath "build\kegelhealth"

$PortableExe = Join-Path $Root "dist\KegelHealth.exe"
if (-not (Test-Path $PortableExe)) {
    Write-Error "PyInstaller did not produce dist\KegelHealth.exe"
}

$InnoCandidates = @(
    "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
    "${env:ProgramFiles}\Inno Setup 6\ISCC.exe",
    "${env:LocalAppData}\Programs\Inno Setup 6\ISCC.exe"
)
$Inno = $InnoCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1

if ($Inno) {
    Write-Host "Building installer with Inno Setup..."
    & $Inno "desktop\installer.iss"
    $SetupExe = Join-Path $Root "dist\installer\KegelHealth-Setup.exe"
    if (Test-Path $SetupExe) {
        Write-Host ""
        Write-Host "Done."
        Write-Host "  Portable:  dist\KegelHealth.exe"
        Write-Host "  Installer: dist\installer\KegelHealth-Setup.exe"
    } else {
        Write-Error "Inno Setup finished but dist\installer\KegelHealth-Setup.exe was not created."
    }
} else {
    Write-Host ""
    Write-Host "Portable exe ready: dist\KegelHealth.exe"
    Write-Host ""
    Write-Host "Inno Setup 6 is not installed - the setup wizard was NOT built."
    Write-Host "Install from https://jrsoftware.org/isinfo.php then re-run:"
    Write-Host '  .\desktop\build.ps1'
}
