@echo off
REM DSA-X GODMODE++: Build Script for Windows
REM 
REM Implemented by Shwet Raj
REM Debug checkpoint: Windows build automation

setlocal EnableDelayedExpansion

set SCRIPT_DIR=%~dp0
set BUILD_DIR=%SCRIPT_DIR%build
set INSTALL_DIR=%SCRIPT_DIR%dist

echo 🚀 DSA-X GODMODE++ Build Script
echo ================================
echo 🖥️  Platform: Windows

REM Check for required tools
echo 🔍 Checking build tools...

REM Check for CMake
cmake --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ CMake not found. Please install CMake 3.16+
    echo    Download from: https://cmake.org/download/
    pause
    exit /b 1
)

REM Check for Visual Studio or Build Tools
where cl >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ MSVC compiler not found. Please install:
    echo    - Visual Studio 2019+ with C++ workload, or
    echo    - Visual Studio Build Tools
    echo    Download from: https://visualstudio.microsoft.com/downloads/
    pause
    exit /b 1
)

echo ✅ Build tools found

REM Check for dependencies
echo 🔍 Checking dependencies...

REM Check for VB-Audio Cable
echo    🎵 VB-Audio Cable: Please ensure VB-Audio Cable is installed
echo       Download from: https://vb-audio.com/Cable/

REM Check for Whisper.cpp
set WHISPER_FOUND=false
if exist "C:\Program Files\whisper\lib\whisper.lib" (
    echo ✅ Whisper.cpp found
    set WHISPER_FOUND=true
) else if exist "%VCPKG_ROOT%\installed\x64-windows\lib\whisper.lib" (
    echo ✅ Whisper.cpp found ^(vcpkg^)
    set WHISPER_FOUND=true
) else (
    echo ⚠️  Whisper.cpp not found - will build without STT
    echo    To install Whisper.cpp:
    echo    git clone https://github.com/ggerganov/whisper.cpp.git
    echo    cd whisper.cpp ^&^& mkdir build ^&^& cd build
    echo    cmake .. ^&^& cmake --build . --config Release
)

REM Check for OpenCV
set OPENCV_FOUND=false
if exist "%OPENCV_DIR%" (
    echo ✅ OpenCV found ^(OPENCV_DIR set^)
    set OPENCV_FOUND=true
) else if exist "%VCPKG_ROOT%\installed\x64-windows\include\opencv2" (
    echo ✅ OpenCV found ^(vcpkg^)
    set OPENCV_FOUND=true
) else (
    echo ⚠️  OpenCV not found - will build without advanced OCR
    echo    Install with vcpkg: vcpkg install opencv[core,imgproc]:x64-windows
)

REM Check for Python dependencies
echo 🐍 Checking Python dependencies...
python --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo ✅ Python found
    
    REM Check for required packages
    set PYTHON_PACKAGES=pyautogui opencv-python pytesseract easyocr pywin32
    for %%p in (%PYTHON_PACKAGES%) do (
        python -c "import %%p" >nul 2>&1
        if !ERRORLEVEL! equ 0 (
            echo    ✅ %%p found
        ) else (
            echo    ⚠️  %%p not found - installing...
            pip install %%p
        )
    )
) else (
    echo ❌ Python not found - fallback systems will not work
    echo    Download from: https://www.python.org/downloads/
)

REM Parse command line arguments
set BUILD_TYPE=Release
set CLEAN_BUILD=false
set RUN_TESTS=false
set VERBOSE=false
set GENERATOR=auto

:parse_args
if "%~1"=="" goto :args_done
if /i "%~1"=="--debug" (
    set BUILD_TYPE=Debug
    shift
    goto :parse_args
)
if /i "%~1"=="--clean" (
    set CLEAN_BUILD=true
    shift
    goto :parse_args
)
if /i "%~1"=="--test" (
    set RUN_TESTS=true
    shift
    goto :parse_args
)
if /i "%~1"=="--verbose" (
    set VERBOSE=true
    shift
    goto :parse_args
)
if /i "%~1"=="--vs2019" (
    set GENERATOR=Visual Studio 16 2019
    shift
    goto :parse_args
)
if /i "%~1"=="--vs2022" (
    set GENERATOR=Visual Studio 17 2022
    shift
    goto :parse_args
)
if /i "%~1"=="--help" (
    echo Usage: %0 [OPTIONS]
    echo Options:
    echo   --debug      Build in debug mode
    echo   --clean      Clean build directory first
    echo   --test       Run tests after building
    echo   --verbose    Verbose output
    echo   --vs2019     Use Visual Studio 2019 generator
    echo   --vs2022     Use Visual Studio 2022 generator
    echo   --help       Show this help
    exit /b 0
)
echo Unknown option: %~1
echo Use --help for usage information
exit /b 1

:args_done

REM Auto-detect Visual Studio version if not specified
if "%GENERATOR%"=="auto" (
    where devenv >nul 2>&1
    if !ERRORLEVEL! equ 0 (
        for /f "tokens=*" %%i in ('devenv /?') do (
            echo %%i | findstr "17\." >nul
            if !ERRORLEVEL! equ 0 (
                set GENERATOR=Visual Studio 17 2022
                goto :generator_set
            )
            echo %%i | findstr "16\." >nul
            if !ERRORLEVEL! equ 0 (
                set GENERATOR=Visual Studio 16 2019
                goto :generator_set
            )
        )
    )
    REM Default fallback
    set GENERATOR=Visual Studio 16 2019
)

:generator_set

REM Clean build directory if requested
if "%CLEAN_BUILD%"=="true" (
    echo 🧹 Cleaning build directory...
    if exist "%BUILD_DIR%" rmdir /s /q "%BUILD_DIR%"
)

REM Create build directories
if not exist "%BUILD_DIR%" mkdir "%BUILD_DIR%"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo 🔨 Starting build process...
echo    Build type: %BUILD_TYPE%
echo    Generator: %GENERATOR%
echo    Build dir: %BUILD_DIR%
echo    Install dir: %INSTALL_DIR%

REM Configure with CMake
echo ⚙️  Configuring with CMake...
cd /d "%BUILD_DIR%"

set CMAKE_ARGS=-G "%GENERATOR%" -A x64 -DCMAKE_BUILD_TYPE=%BUILD_TYPE% -DCMAKE_INSTALL_PREFIX="%INSTALL_DIR%"

if "%VERBOSE%"=="true" (
    set CMAKE_ARGS=%CMAKE_ARGS% -DCMAKE_VERBOSE_MAKEFILE=ON
)

REM Add vcpkg integration if available
if exist "%VCPKG_ROOT%\scripts\buildsystems\vcpkg.cmake" (
    set CMAKE_ARGS=%CMAKE_ARGS% -DCMAKE_TOOLCHAIN_FILE="%VCPKG_ROOT%\scripts\buildsystems\vcpkg.cmake"
    echo    📦 Using vcpkg toolchain
)

cmake %CMAKE_ARGS% "%SCRIPT_DIR%"
if %ERRORLEVEL% neq 0 (
    echo ❌ CMake configuration failed
    pause
    exit /b 1
)

REM Build the project
echo 🔨 Building project...
if "%VERBOSE%"=="true" (
    cmake --build . --config %BUILD_TYPE% --parallel --verbose
) else (
    cmake --build . --config %BUILD_TYPE% --parallel
)

if %ERRORLEVEL% neq 0 (
    echo ❌ Build failed
    pause
    exit /b 1
)

REM Install the project
echo 📦 Installing project...
cmake --build . --config %BUILD_TYPE% --target install

if %ERRORLEVEL% neq 0 (
    echo ❌ Installation failed
    pause
    exit /b 1
)

echo ✅ Build complete!
echo.
echo 📁 Installation directory: %INSTALL_DIR%
echo 🎯 Executable: %INSTALL_DIR%\bin\dsax-godmode.exe
echo.

REM Show next steps
echo 🚀 Next steps:
echo    1. Install VB-Audio Cable:
echo       Download from: https://vb-audio.com/Cable/

if "%WHISPER_FOUND%"=="false" (
    echo    2. Install Whisper.cpp for STT functionality:
    echo       git clone https://github.com/ggerganov/whisper.cpp.git
    echo       cd whisper.cpp ^&^& mkdir build ^&^& cd build
    echo       cmake .. ^&^& cmake --build . --config Release
)

echo    3. Download Whisper model:
echo       mkdir models
echo       powershell -Command "Invoke-WebRequest -Uri 'https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin' -OutFile 'models\ggml-base.en.bin'"

echo    4. Run the application:
echo       %INSTALL_DIR%\bin\dsax-godmode.exe --test
echo.

REM Run tests if requested
if "%RUN_TESTS%"=="true" (
    echo 🧪 Running tests...
    if exist "%INSTALL_DIR%\bin\dsax-godmode.exe" (
        cd /d "%SCRIPT_DIR%"
        start "DSA-X Test" /B "%INSTALL_DIR%\bin\dsax-godmode.exe" --test
        echo Test mode started in background
        echo Press any key to continue...
        pause >nul
        taskkill /f /im dsax-godmode.exe >nul 2>&1
        echo Test completed
    ) else (
        echo ❌ Executable not found for testing
    )
)

echo 🎉 Build script completed successfully!
echo.
echo 📖 For more information, see README.md
pause