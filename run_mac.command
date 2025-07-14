#!/bin/bash
# DSA-X GODMODE++: Ultra-Stealth AI Assistant
# macOS Launch Script with BlackHole Integration
# 
# Implemented by Shwet Raj
# Debug checkpoint: macOS launch and BlackHole setup

echo "🚀 DSA-X GODMODE++: Ultra-Stealth AI Assistant"
echo "Initializing for macOS with BlackHole audio capture..."

# Check if BlackHole is installed
if ! system_profiler SPAudioDataType | grep -q "BlackHole"; then
    echo "❌ BlackHole not found. Please install BlackHole first:"
    echo "   brew install blackhole-2ch"
    echo "   or download from: https://existential.audio/blackhole/"
    exit 1
fi

# Check if running from ZIP
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ "$SCRIPT_DIR" == *".zip"* ]]; then
    echo "📦 Running from ZIP archive - RAM-only mode enabled"
fi

# Set up environment
export DSAX_STEALTH_MODE=1
export DSAX_RAM_ONLY=1
export DSAX_AUDIO_CAPTURE=blackhole

# Check system requirements
echo "🔍 Checking system requirements..."

# Check macOS version
MACOS_VERSION=$(sw_vers -productVersion)
echo "   macOS Version: $MACOS_VERSION"

# Check available memory
TOTAL_MEM=$(sysctl -n hw.memsize | awk '{print $0/1024/1024/1024 " GB"}')
echo "   Total Memory: $TOTAL_MEM"

# Check if Metal is available
if system_profiler SPDisplaysDataType | grep -q "Metal"; then
    echo "   ✅ Metal GPU support available"
else
    echo "   ⚠️  Metal GPU support not detected"
fi

# Initialize BlackHole audio routing
echo "🎵 Setting up BlackHole audio capture..."

# Create audio routing script
cat > /tmp/dsax_audio_setup.sh << 'EOF'
#!/bin/bash
# Set up BlackHole audio routing
# Route system audio to BlackHole
osascript -e '
tell application "System Preferences"
    activate
    set current pane to pane "com.apple.preference.sound"
end tell

tell application "System Events"
    tell process "System Preferences"
        click tab group 1 of window "Sound"
        select row 2 of table 1 of scroll area 1 of tab group 1 of window "Sound"
        click button "Set Default" of tab group 1 of window "Sound"
    end tell
end tell
'
EOF

chmod +x /tmp/dsax_audio_setup.sh

# Launch the main application
echo "🚀 Launching DSA-X GODMODE++..."

# Check if executable exists
if [ -f "$SCRIPT_DIR/dsax_godmode" ]; then
    echo "   ✅ Found main executable"
    cd "$SCRIPT_DIR"
    ./dsax_godmode
elif [ -f "$SCRIPT_DIR/dsax_godmode.app/Contents/MacOS/dsax_godmode" ]; then
    echo "   ✅ Found app bundle"
    open "$SCRIPT_DIR/dsax_godmode.app"
else
    echo "   ❌ Main executable not found"
    echo "   Please ensure dsax_godmode is in the same directory as this script"
    exit 1
fi

# Cleanup on exit
trap 'echo "🧹 Cleaning up..."; rm -f /tmp/dsax_audio_setup.sh; exit' EXIT

echo "✅ DSA-X GODMODE++ launched successfully"
echo "   🎵 Audio capture: BlackHole"
echo "   🖥️  Overlay: Metal GPU"
echo "   🧠 AI: RAM-only whisper.cpp"
echo "   👻 Stealth: Zero-trace mode"
echo ""
echo "Press Ctrl+C to exit"