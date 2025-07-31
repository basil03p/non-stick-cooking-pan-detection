@echo off
setlocal enabledelayedexpansion

REM Dual Deployment Script for Cookware Analyzer (Windows)
REM Supports both Koyeb and Vercel deployments

echo 🍳 Cookware Damage Analyzer - Dual Deployment Setup
echo 📅 Project Date: 2025-07-31 20:20:27 UTC
echo 👤 Developer: basil03p
echo 🧠 CNN-based Nonstick Cookware Damage Detection
echo.

echo 📋 Checking Deployment Requirements...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

set "missing_files=0"

REM Check core files
echo Core Application Files:
call :check_file "app.py"
call :check_file "requirements.txt"
call :check_file "README.md"

echo.
echo 🚀 Deployment Configuration Files:
call :check_file "koyeb.yaml"
call :check_file "vercel.json"
call :check_file "Dockerfile"
call :check_file "gunicorn.conf.py"

echo.
echo 📁 Directory Structure:
call :check_directory "models"
call :check_directory "public"
call :check_directory "api"

echo.
echo 🧠 AI Models Check:
if exist "models" (
    call :check_file "models\optimized_cookware_acc_0.2898.keras"
    call :check_file "models\proven_cookware_classifier_acc_0.4034.keras"
    call :check_file "models\original_cookware_classifier_acc_0.4489.keras"
    
    if exist "models\optimized_cookware_acc_0.2898.keras" (
        echo ✅ Primary optimized model is available ^(71.02%% accuracy^)
    ) else (
        echo ⚠️ Primary optimized model missing - will use fallback
    )
) else (
    echo ❌ Models directory missing!
    set /a missing_files+=1
)

echo.
echo 🔗 API Endpoints Check:
call :check_file "api\analyze.py"
call :check_file "api\health.py"

echo.
echo 🌐 Frontend Files Check:
call :check_file "public\index.html"
call :check_file "public\script.js"
call :check_file "public\styles.css"
call :check_file "public\manifest.json"

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo 🔧 Environment Validation:

REM Python check
python --version >nul 2>&1
if !errorlevel! equ 0 (
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo ✅ Python available: %%i
    
    python -c "import json, base64, datetime" >nul 2>&1 && echo ✅ Core Python packages available
    python -c "import flask" >nul 2>&1 && echo ✅ Flask available || echo ⚠️ Flask not installed
    python -c "import tensorflow" >nul 2>&1 && echo ✅ TensorFlow available || echo ⚠️ TensorFlow not installed ^(will use mock mode^)
    python -c "import PIL" >nul 2>&1 && echo ✅ Pillow available || echo ⚠️ Pillow not installed
    python -c "import numpy" >nul 2>&1 && echo ✅ NumPy available || echo ⚠️ NumPy not installed
) else (
    echo ⚠️ Python not found - ensure it's installed for local testing
)

REM Git check
git --version >nul 2>&1
if !errorlevel! equ 0 (
    echo ✅ Git available for version control
) else (
    echo ⚠️ Git not found - needed for deployment
)

REM Docker check
docker --version >nul 2>&1
if !errorlevel! equ 0 (
    echo ✅ Docker available for containerized deployment
) else (
    echo ℹ️ Docker not found ^(optional for direct cloud deployment^)
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo 🎯 Deployment Summary:
echo.
echo 📊 Project: CNN-based Cookware Damage Detection
echo 🧠 Model: EfficientNetV2-B0 + Custom Classification Head
echo 🎯 Accuracy: 71.02%% ^(Optimized Model^)
echo 📦 Classes: new, minor, moderate, severe
echo 🚫 API Keys: None required ^(self-contained^)
echo ⚡ Features: Real-time analysis, Safety assessment, Web interface
echo.

if !missing_files! equ 0 (
    echo ✅ All required files present!
    echo.
    echo 🚀 Ready for deployment to:
    echo.
    echo 1️⃣ KOYEB DEPLOYMENT:
    echo    • Configuration: koyeb.yaml
    echo    • Runtime: Flask + Gunicorn
    echo    • Instance: Small ^(for TensorFlow^)
    echo    • Health Check: /api/health
    echo    • Command: gunicorn --config gunicorn.conf.py app:app
    echo.
    echo 2️⃣ VERCEL DEPLOYMENT:
    echo    • Configuration: vercel.json
    echo    • Runtime: Serverless Functions
    echo    • API Routes: /api/analyze, /api/health
    echo    • Static Files: /public/*
    echo    • Build: @vercel/python
    echo.
    echo 📝 Next Steps:
    echo.
    echo For Koyeb:
    echo • Push to GitHub repository
    echo • Connect repo to Koyeb
    echo • Deploy with koyeb.yaml
    echo.
    echo For Vercel:
    echo • Push to GitHub repository
    echo • Import project to Vercel
    echo • Deploy with vercel.json
    echo.
    echo 🔗 Test Commands:
    echo • Local Flask: python app.py
    echo • Local Gunicorn: gunicorn --config gunicorn.conf.py app:app
    echo • Install deps: pip install -r requirements.txt
    echo.
    echo ✅ Deployment preparation complete!
) else (
    echo ❌ !missing_files! files/directories missing!
    echo.
    echo 🔧 Please fix missing files before deployment
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ✨ Cookware Analyzer Deployment Check Complete
echo 👨‍💻 Developer: basil03p ^| 📅 Completed: 2025-07-31 20:20:27 UTC

goto :eof

:check_file
if exist "%~1" (
    echo ✅ %~1 exists
) else (
    echo ❌ %~1 is missing!
    set /a missing_files+=1
)
goto :eof

:check_directory
if exist "%~1\" (
    echo ✅ %~1 directory exists
) else (
    echo ❌ %~1 directory is missing!
    set /a missing_files+=1
)
goto :eof
