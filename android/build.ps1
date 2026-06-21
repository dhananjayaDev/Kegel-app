# Build Android APK (requires JDK 17 + Android SDK)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$PythonSrc = Join-Path $PSScriptRoot "app\src\main\python"
$AppDest = Join-Path $PythonSrc "application"
$DataDest = Join-Path $PythonSrc "data"
$WrapperJar = Join-Path $PSScriptRoot "gradle\wrapper\gradle-wrapper.jar"

function Ensure-GradleWrapper {
    if (Test-Path $WrapperJar) { return }

    Write-Host "Downloading Gradle wrapper jar …"
    $url = "https://github.com/gradle/gradle/raw/v8.7.0/gradle/wrapper/gradle-wrapper.jar"
    New-Item -ItemType Directory -Force -Path (Split-Path $WrapperJar) | Out-Null
    Invoke-WebRequest -Uri $url -OutFile $WrapperJar -UseBasicParsing
}

function Find-JavaHome {
    if ($env:JAVA_HOME -and (Test-Path (Join-Path $env:JAVA_HOME "bin\java.exe"))) {
        return $env:JAVA_HOME
    }

    $studioJbr = "${env:ProgramFiles}\Android\Android Studio\jbr"
    if (Test-Path (Join-Path $studioJbr "bin\java.exe")) {
        return $studioJbr
    }

    $studioJbrX86 = "${env:ProgramFiles(x86)}\Android\Android Studio\jbr"
    if (Test-Path (Join-Path $studioJbrX86 "bin\java.exe")) {
        return $studioJbrX86
    }

    return $null
}

function Find-AndroidSdk {
    if ($env:ANDROID_HOME -and (Test-Path $env:ANDROID_HOME)) {
        return $env:ANDROID_HOME
    }
    if ($env:ANDROID_SDK_ROOT -and (Test-Path $env:ANDROID_SDK_ROOT)) {
        return $env:ANDROID_SDK_ROOT
    }

    $localSdk = Join-Path $env:LOCALAPPDATA "Android\Sdk"
    if (Test-Path $localSdk) {
        return $localSdk
    }

    return $null
}

Write-Host "Syncing Python app into android/app/src/main/python …"

if (Test-Path $AppDest) { Remove-Item $AppDest -Recurse -Force }
if (Test-Path $DataDest) { Remove-Item $DataDest -Recurse -Force }

Copy-Item (Join-Path $Root "application") $AppDest -Recurse
Copy-Item (Join-Path $Root "data") $DataDest -Recurse

Ensure-GradleWrapper

$javaHome = Find-JavaHome
if (-not $javaHome) {
    Write-Error "JDK not found. Install Android Studio or set JAVA_HOME to JDK 17+."
}

$pythonCandidates = @(
    (Join-Path $Root "venv\Scripts\python.exe"),
    "${env:LOCALAPPDATA}\Programs\Python\Python311\python.exe",
    (Get-Command py -ErrorAction SilentlyContinue | ForEach-Object { "py -3.11" })
)
$pythonExe = $null
foreach ($candidate in $pythonCandidates) {
    if ($candidate -eq "py -3.11") {
        try {
            $ver = & py -3.11 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>$null
            if ($ver -eq "3.11") { $pythonExe = "py -3.11"; break }
        } catch { continue }
    } elseif ($candidate -and (Test-Path $candidate)) {
        $ver = & $candidate -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>$null
        if ($ver -eq "3.11") { $pythonExe = $candidate; break }
    }
}
if (-not $pythonExe) {
    Write-Error "Python 3.11 is required for the Android build. Install it from python.org."
}
if ($pythonExe -eq "py -3.11") {
    $env:CHAQUO_PYTHON = "py"
    $env:CHAQUO_PYTHON_ARGS = "-3.11"
} else {
    $env:CHAQUO_PYTHON = $pythonExe
}

$sdk = Find-AndroidSdk
if (-not $sdk) {
    Write-Error "Android SDK not found. Install Android Studio and the Android SDK, or set ANDROID_HOME."
}

$localProps = Join-Path $PSScriptRoot "local.properties"
"sdk.dir=$($sdk -replace '\\', '\\')" | Set-Content -Path $localProps -Encoding ASCII

$env:JAVA_HOME = $javaHome
$env:ANDROID_HOME = $sdk

Set-Location $PSScriptRoot
& .\gradlew.bat assembleRelease

Write-Host ""
Write-Host "APK: android\app\build\outputs\apk\release\app-release-unsigned.apk"
Write-Host "Sign with Android Studio or apksigner before distribution."
