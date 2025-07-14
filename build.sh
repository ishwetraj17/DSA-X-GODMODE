#!/bin/bash
# DSA-X GODMODE++: Build Script for macOS/Linux
# 
# Implemented by Shwet Raj
# Debug checkpoint: Cross-platform build automation

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="$SCRIPT_DIR/build"
INSTALL_DIR="$SCRIPT_DIR/dist"

echo "🚀 DSA-X GODMODE++ Build Script"
echo "================================"

# Detect platform
if [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macOS"
    echo "📱 Platform: macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PLATFORM="Linux"
    echo "🐧 Platform: Linux"
else
    echo "❌ Unsupported platform: $OSTYPE"
    exit 1
fi

# Check for required tools
echo "🔍 Checking build tools..."

if ! command -v cmake &> /dev/null; then
    echo "❌ CMake not found. Please install CMake 3.16+"
    if [[ "$PLATFORM" == "macOS" ]]; then
        echo "   Install with: brew install cmake"
    else
        echo "   Install with: sudo apt-get install cmake"
    fi
    exit 1
fi

if ! command -v make &> /dev/null; then
    echo "❌ Make not found. Please install build tools"
    if [[ "$PLATFORM" == "macOS" ]]; then
        echo "   Install with: xcode-select --install"
    else
        echo "   Install with: sudo apt-get install build-essential"
    fi
    exit 1
fi

echo "✅ Build tools found"

# Check for dependencies
echo "🔍 Checking dependencies..."

# Check for audio dependencies
if [[ "$PLATFORM" == "macOS" ]]; then
    echo "   🎵 BlackHole: Please ensure BlackHole is installed"
    echo "      Install with: brew install blackhole-2ch"
elif [[ "$PLATFORM" == "Linux" ]]; then
    if ! pkg-config --exists alsa; then
        echo "❌ ALSA not found. Installing..."
        sudo apt-get update
        sudo apt-get install -y libasound2-dev
    fi
    echo "✅ ALSA found"
fi

# Check for Whisper.cpp
WHISPER_FOUND=false
if [[ -f "/usr/local/lib/libwhisper.a" ]] || [[ -f "/opt/homebrew/lib/libwhisper.a" ]]; then
    echo "✅ Whisper.cpp found"
    WHISPER_FOUND=true
else
    echo "⚠️  Whisper.cpp not found - will build without STT"
    echo "   To install Whisper.cpp:"
    echo "   git clone https://github.com/ggerganov/whisper.cpp.git"
    echo "   cd whisper.cpp && make && sudo make install"
fi

# Check for OpenCV
OPENCV_FOUND=false
if pkg-config --exists opencv4 || pkg-config --exists opencv; then
    echo "✅ OpenCV found"
    OPENCV_FOUND=true
else
    echo "⚠️  OpenCV not found - will build without advanced OCR"
    if [[ "$PLATFORM" == "macOS" ]]; then
        echo "   Install with: brew install opencv"
    else
        echo "   Install with: sudo apt-get install libopencv-dev"
    fi
fi

# Check for Python dependencies (for fallbacks)
echo "🐍 Checking Python dependencies..."
if command -v python3 &> /dev/null; then
    echo "✅ Python 3 found"
    
    # Check for required Python packages
    PYTHON_PACKAGES=("pyautogui" "opencv-python" "pytesseract" "easyocr")
    MISSING_PACKAGES=()
    
    for package in "${PYTHON_PACKAGES[@]}"; do
        if python3 -c "import $package" &> /dev/null; then
            echo "   ✅ $package found"
        else
            echo "   ⚠️  $package not found"
            MISSING_PACKAGES+=("$package")
        fi
    done
    
    if [[ ${#MISSING_PACKAGES[@]} -gt 0 ]]; then
        echo "   📦 Installing missing Python packages..."
        pip3 install "${MISSING_PACKAGES[@]}" || {
            echo "   ⚠️  Failed to install some Python packages"
            echo "   You may need to install manually:"
            printf '      pip3 install %s\n' "${MISSING_PACKAGES[@]}"
        }
    fi
else
    echo "❌ Python 3 not found - fallback systems will not work"
fi

# Parse command line arguments
BUILD_TYPE="Release"
CLEAN_BUILD=false
RUN_TESTS=false
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --debug)
            BUILD_TYPE="Debug"
            shift
            ;;
        --clean)
            CLEAN_BUILD=true
            shift
            ;;
        --test)
            RUN_TESTS=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --debug    Build in debug mode"
            echo "  --clean    Clean build directory first"
            echo "  --test     Run tests after building"
            echo "  --verbose  Verbose output"
            echo "  --help     Show this help"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Clean build directory if requested
if [[ "$CLEAN_BUILD" == true ]]; then
    echo "🧹 Cleaning build directory..."
    rm -rf "$BUILD_DIR"
fi

# Create build directory
mkdir -p "$BUILD_DIR"
mkdir -p "$INSTALL_DIR"

echo "🔨 Starting build process..."
echo "   Build type: $BUILD_TYPE"
echo "   Build dir: $BUILD_DIR"
echo "   Install dir: $INSTALL_DIR"

# Configure with CMake
echo "⚙️  Configuring with CMake..."
cd "$BUILD_DIR"

CMAKE_ARGS=(
    -DCMAKE_BUILD_TYPE="$BUILD_TYPE"
    -DCMAKE_INSTALL_PREFIX="$INSTALL_DIR"
)

if [[ "$VERBOSE" == true ]]; then
    CMAKE_ARGS+=(-DCMAKE_VERBOSE_MAKEFILE=ON)
fi

cmake "${CMAKE_ARGS[@]}" "$SCRIPT_DIR"

# Build the project
echo "🔨 Building project..."
if [[ "$VERBOSE" == true ]]; then
    make -j$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4) VERBOSE=1
else
    make -j$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)
fi

# Install the project
echo "📦 Installing project..."
make install

echo "✅ Build complete!"
echo ""
echo "📁 Installation directory: $INSTALL_DIR"
echo "🎯 Executable: $INSTALL_DIR/bin/dsax-godmode"
echo ""

# Show next steps
echo "🚀 Next steps:"
echo "   1. Install audio drivers:"
if [[ "$PLATFORM" == "macOS" ]]; then
    echo "      brew install blackhole-2ch"
else
    echo "      Audio drivers should already be installed"
fi

if [[ "$WHISPER_FOUND" == false ]]; then
    echo "   2. Install Whisper.cpp for STT functionality:"
    echo "      git clone https://github.com/ggerganov/whisper.cpp.git"
    echo "      cd whisper.cpp && make && sudo make install"
fi

echo "   3. Download Whisper model:"
echo "      mkdir -p models"
echo "      wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin -O models/ggml-base.en.bin"

echo "   4. Run the application:"
echo "      $INSTALL_DIR/bin/dsax-godmode --test"
echo ""

# Run tests if requested
if [[ "$RUN_TESTS" == true ]]; then
    echo "🧪 Running tests..."
    if [[ -f "$INSTALL_DIR/bin/dsax-godmode" ]]; then
        cd "$SCRIPT_DIR"
        "$INSTALL_DIR/bin/dsax-godmode" --test &
        TEST_PID=$!
        
        echo "Test mode started (PID: $TEST_PID)"
        echo "Press Ctrl+C to stop test mode"
        
        # Wait a bit then stop
        sleep 5
        kill $TEST_PID 2>/dev/null || true
        echo "Test completed"
    else
        echo "❌ Executable not found for testing"
    fi
fi

echo "🎉 Build script completed successfully!"