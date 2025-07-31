@echo off
setlocal enabledelayedexpansion

echo 🍳 Cookware Analyzer - Multi-Platform Deployment Script
echo =======================================================

:: Function to check if command exists
where koyeb >nul 2>&1
if %errorlevel% neq 0 (
    set KOYEB_AVAILABLE=false
) else (
    set KOYEB_AVAILABLE=true
)

where vercel >nul 2>&1
if %errorlevel% neq 0 (
    set VERCEL_AVAILABLE=false
) else (
    set VERCEL_AVAILABLE=true
)

where node >nul 2>&1
if %errorlevel% neq 0 (
    set NODE_AVAILABLE=false
) else (
    set NODE_AVAILABLE=true
)

:: Pre-deployment checks
echo 🔍 Running pre-deployment checks...

if not exist "app.py" (
    echo ❌ Required file missing: app.py
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo ❌ Required file missing: requirements.txt
    pause
    exit /b 1
)

if not exist "koyeb.yaml" (
    echo ❌ Required file missing: koyeb.yaml
    pause
    exit /b 1
)

if not exist "vercel.json" (
    echo ❌ Required file missing: vercel.json
    pause
    exit /b 1
)

if not exist "models" (
    echo ❌ Models directory not found!
    pause
    exit /b 1
)

dir /b "models\*.keras" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ No .keras model files found in models directory!
    pause
    exit /b 1
)

echo ✅ All pre-deployment checks passed!

:: Handle command line arguments
if "%1"=="koyeb" goto deploy_koyeb
if "%1"=="vercel" goto deploy_vercel
if "%1"=="both" goto deploy_both
if "%1"=="check" goto check_only

:: Interactive menu
:menu
echo.
echo 📋 Deployment Options:
echo 1. Deploy to Koyeb only
echo 2. Deploy to Vercel only
echo 3. Deploy to both platforms
echo 4. Run pre-deployment checks only
echo 5. Exit
echo.

set /p choice="Select an option (1-5): "

if "%choice%"=="1" goto deploy_koyeb
if "%choice%"=="2" goto deploy_vercel
if "%choice%"=="3" goto deploy_both
if "%choice%"=="4" goto check_only
if "%choice%"=="5" goto exit_script

echo ❌ Invalid option. Please select 1-5.
goto menu

:deploy_koyeb
echo 🚀 Deploying to Koyeb...

if "%KOYEB_AVAILABLE%"=="false" (
    echo ❌ Koyeb CLI not found. Please install it first:
    echo    Visit: https://www.koyeb.com/docs/cli/installation
    pause
    goto menu
)

echo 📦 Deploying with Koyeb configuration...
koyeb app deploy cookware-analyzer --config koyeb.yaml

echo ✅ Koyeb deployment initiated!
echo 🔗 Check status: https://app.koyeb.com/
goto end

:deploy_vercel
echo 🚀 Deploying to Vercel...

if "%NODE_AVAILABLE%"=="false" (
    echo ❌ Node.js not found. Please install Node.js first:
    echo    Visit: https://nodejs.org/
    pause
    goto menu
)

if "%VERCEL_AVAILABLE%"=="false" (
    echo 📦 Installing Vercel CLI...
    npm i -g vercel
    if %errorlevel% neq 0 (
        echo ❌ Failed to install Vercel CLI
        pause
        goto menu
    )
)

echo 📦 Deploying with Vercel configuration...

:: Copy Vercel-specific requirements
copy requirements-vercel.txt requirements.txt >nul

:: Deploy to Vercel
vercel deploy --prod

:: Restore original requirements (if git is available)
git checkout requirements.txt >nul 2>&1

echo ✅ Vercel deployment completed!
echo 🔗 Your app is now live on Vercel
goto end

:deploy_both
echo 🚀 Deploying to both Koyeb and Vercel...

call :deploy_koyeb
echo.
call :deploy_vercel

echo.
echo 🎉 Deployment to both platforms completed!
goto end

:check_only
echo ✅ Pre-deployment checks completed successfully!
goto menu

:exit_script
echo 👋 Goodbye!
exit /b 0

:end
echo.
echo 🎉 Deployment completed!
pause
exit /b 0
