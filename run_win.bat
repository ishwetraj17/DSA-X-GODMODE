@echo off
REM DSA-X GODMODE++: Ultra-Stealth AI Assistant
REM Windows Launch Script with VB-Audio Cable Integration
REM 
REM Implemented by Shwet Raj
REM Debug checkpoint: Windows launch and VB-Cable setup

echo 🚀 DSA-X GODMODE++: Ultra-Stealth AI Assistant
echo Initializing for Windows with VB-Audio Cable capture...

REM Check if running from ZIP
set SCRIPT_DIR=%~dp0
echo %SCRIPT_DIR% | findstr /i ".zip" >nul
if %errorlevel% equ 0 (
    echo 📦 Running from ZIP archive - RAM-only mode enabled
)

REM Set up environment variables
set DSAX_STEALTH_MODE=1
set DSAX_RAM_ONLY=1
set DSAX_AUDIO_CAPTURE=vb_cable

REM Check system requirements
echo 🔍 Checking system requirements...

REM Check Windows version
for /f "tokens=4-5 delims=. " %%i in ('ver') do set VERSION=%%i.%%j
echo    Windows Version: %VERSION%

REM Check available memory
wmic computersystem get TotalPhysicalMemory /value | find "=" >nul
if %errorlevel% equ 0 (
    for /f "tokens=2 delims==" %%a in ('wmic computersystem get TotalPhysicalMemory /value ^| find "="') do set TOTAL_MEM=%%a
    set /a TOTAL_MEM_GB=%TOTAL_MEM%/1024/1024/1024
    echo    Total Memory: %TOTAL_MEM_GB% GB
)

REM Check if DirectX is available
dxdiag /t dxdiag_output.txt >nul 2>&1
findstr /i "DirectX" dxdiag_output.txt >nul
if %errorlevel% equ 0 (
    echo    ✅ DirectX support available
) else (
    echo    ⚠️  DirectX support not detected
)
del dxdiag_output.txt >nul 2>&1

REM Check if VB-Audio Cable is installed
echo 🎵 Checking VB-Audio Cable installation...

REM Check registry for VB-Audio Cable
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\VB-Audio Virtual Cable" >nul 2>&1
if %errorlevel% equ 0 (
    echo    ✅ VB-Audio Cable found
) else (
    echo    ❌ VB-Audio Cable not found. Please install VB-Audio Cable first:
    echo       Download from: https://vb-audio.com/Cable/
    echo       Install and restart your computer
    pause
    exit /b 1
)

REM Initialize VB-Audio Cable routing
echo 🎵 Setting up VB-Audio Cable capture...

REM Create audio routing script
echo @echo off > "%TEMP%\dsax_audio_setup.bat"
echo REM Set up VB-Audio Cable audio routing >> "%TEMP%\dsax_audio_setup.bat"
echo REM Route system audio to VB-Audio Cable >> "%TEMP%\dsax_audio_setup.bat"
echo start /min "" "C:\Program Files\VB\Cable\CableControl.exe" >> "%TEMP%\dsax_audio_setup.bat"

REM Launch the main application
echo 🚀 Launching DSA-X GODMODE++...

REM Check if executable exists
if exist "%SCRIPT_DIR%dsax_godmode.exe" (
    echo    ✅ Found main executable
    cd /d "%SCRIPT_DIR%"
    start "" "dsax_godmode.exe"
) else if exist "%SCRIPT_DIR%dsax_godmode\dsax_godmode.exe" (
    echo    ✅ Found application folder
    cd /d "%SCRIPT_DIR%dsax_godmode"
    start "" "dsax_godmode.exe"
) else (
    echo    ❌ Main executable not found
    echo    Please ensure dsax_godmode.exe is in the same directory as this script
    pause
    exit /b 1
)

REM Cleanup on exit
echo ✅ DSA-X GODMODE++ launched successfully
echo    🎵 Audio capture: VB-Audio Cable
echo    🖥️  Overlay: DirectX GPU
echo    🧠 AI: RAM-only whisper.cpp
echo    👻 Stealth: Zero-trace mode
echo.
echo Press any key to exit...
pause >nul

REM Cleanup temporary files
if exist "%TEMP%\dsax_audio_setup.bat" del "%TEMP%\dsax_audio_setup.bat" >nul 2>&1