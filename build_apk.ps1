Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Kingdom Defense APK Build" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set environment
$env:JAVA_HOME = "d:\12\jdk-17.0.2"
$env:ANDROID_HOME = "d:\12\android-sdk"
$env:ANDROID_NDK_HOME = "d:\12\android-ndk-r25b"
$env:ANDROID_SDK_ROOT = "d:\12\android-sdk"
$env:PATH = "$env:JAVA_HOME\bin;$env:ANDROID_HOME\platform-tools;$env:PATH"

Write-Host "[1/5] Environment configured" -ForegroundColor Green

# Verify Java
Write-Host "[2/5] Verifying Java..." -ForegroundColor Cyan
& "$env:JAVA_HOME\bin\java.exe" -version 2>&1 | Out-Null
Write-Host "  Java OK" -ForegroundColor Green

# Install dependencies
Write-Host "[3/5] Installing dependencies..." -ForegroundColor Cyan
Write-Host "  This may take 5-10 minutes..." -ForegroundColor Yellow

py -3.13 -m pip install --upgrade pip wheel setuptools
py -3.13 -m pip install "cython>=3.0,<4.0"
py -3.13 -m pip install colorama appdirs jinja2 toml pexpect requests
py -3.13 -m pip install buildozer==1.4.0
py -3.13 -m pip install python-for-android==2023.5.21

Write-Host "  Dependencies installed!" -ForegroundColor Green

# Verify buildozer
Write-Host "[4/5] Verifying buildozer..." -ForegroundColor Cyan
py -3.13 -m buildozer --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ERROR: buildozer not working!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "  buildozer OK!" -ForegroundColor Green

# Start build
Write-Host "[5/5] Starting APK build..." -ForegroundColor Magenta
Write-Host ""
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  THIS TAKES 30-60 MINUTES!" -ForegroundColor Yellow
Write-Host "  Please wait and be patient..." -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""

py -3.13 -m buildozer android debug

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  BUILD SUCCESSFUL!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    
    if (Test-Path "bin\*.apk") {
        Write-Host ""
        Write-Host "APK files:" -ForegroundColor Cyan
        Get-ChildItem "bin\*.apk" | ForEach-Object {
            Write-Host "  $($_.Name) ($([math]::Round($_.Length / 1MB, 2)) MB)" -ForegroundColor White
        }
        Write-Host ""
        Write-Host "Opening bin folder..." -ForegroundColor Cyan
        Start-Process explorer -ArgumentList "bin\"
    }
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  BUILD FAILED!" -ForegroundColor Red
    Write-Host "  Error code: $LASTEXITCODE" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"
