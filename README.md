# 🚀 DSA-X GODMODE++: Ultra-Stealth AI Assistant

> **Elite Technical Interview Assistant with Advanced AI and Stealth Capabilities**

## 🎯 Overview

DSA-X GODMODE++ is a **production-ready, ultra-stealth AI assistant** designed for technical interviews. It provides real-time audio transcription, intelligent question classification, and multi-language code generation with complete stealth operation.

### ✨ Key Features

- 🎧 **Real-time Audio Capture**: BlackHole (macOS) / VB-Audio Cable (Windows)
- 🧠 **Advanced AI Processing**: Question classification and intelligent responses
- 💻 **Multi-language Support**: Java, C++, Python, JavaScript code generation
- 🎯 **Comprehensive Coverage**: DSA, System Design, STAR, OOP, OS, DBMS, Networking
- 👻 **Screen-Share Invisible**: GPU-only overlay that bypasses screen recording
- 💾 **Zero-Trace Operation**: RAM-only, no disk writes, no persistence
- 🔐 **Advanced Stealth**: Process cloaking, anti-detection, self-healing
- 🛡️ **Fallback Systems**: Clipboard monitoring, OCR capture, manual input

## 🏗️ Architecture

```
┌─ Audio Input ──┬─ STT Processing ──┬─ AI Engine ──┬─ GPU Overlay ─┐
│ BlackHole/VBC  │ Whisper.cpp      │ Classifier  │ Metal/DirectX │
├─ Clipboard ────┤ Text Processing  ├─ Generator  ├─ Stealth Mode ┤
└─ OCR Fallback ─┴─ Queue Management┴─ Templates  └─ Self-Healing ┘
```

## 🛠️ System Requirements

### Hardware
- **RAM**: 4GB minimum (8GB recommended for optimal performance)
- **Storage**: 500MB for application + 1GB for Whisper models
- **GPU**: Metal (macOS) / DirectX 11+ (Windows) for overlay
- **CPU**: Multi-core processor (4+ cores recommended)

### Operating System
- **macOS**: 10.15+ (Catalina or later)
- **Windows**: 10/11 (x64)
- **Linux**: Ubuntu 20.04+ / Debian 11+ (experimental)

## 📦 Quick Installation

### 🍎 macOS Installation

```bash
# 1. Install dependencies
brew install cmake blackhole-2ch

# 2. Clone and build
git clone https://github.com/ishwetraj17/DSA-X-GODMODE.git
cd DSA-X-GODMODE
chmod +x build.sh
./build.sh

# 3. Download Whisper model
mkdir -p models
wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin -O models/ggml-base.en.bin

# 4. Run test
./dist/bin/dsax-godmode --test
```

### 🖥️ Windows Installation

```cmd
REM 1. Install dependencies (download and install):
REM    - Visual Studio 2019+ with C++ workload
REM    - CMake 3.16+
REM    - VB-Audio Cable

REM 2. Clone and build
git clone https://github.com/ishwetraj17/DSA-X-GODMODE.git
cd DSA-X-GODMODE
build.bat

REM 3. Download Whisper model
mkdir models
powershell -Command "Invoke-WebRequest -Uri 'https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin' -OutFile 'models\ggml-base.en.bin'"

REM 4. Run test
dist\bin\dsax-godmode.exe --test
```

## 🔧 Detailed Setup

### Step 1: Audio Driver Installation

#### macOS - BlackHole
```bash
# Option 1: Homebrew (recommended)
brew install blackhole-2ch

# Option 2: Manual download
# Download from: https://existential.audio/blackhole/
```

#### Windows - VB-Audio Cable
```cmd
# Download and install VB-Audio Cable
# https://vb-audio.com/Cable/
```

### Step 2: Build Dependencies

#### Required Tools
- **CMake**: 3.16 or later
- **C++17 Compiler**: GCC 8+, Clang 10+, MSVC 2019+
- **Python 3.8+**: For fallback systems
- **Git**: For cloning repositories

#### Optional Dependencies
- **Whisper.cpp**: For speech-to-text functionality
- **OpenCV**: For advanced OCR preprocessing
- **EasyOCR**: For enhanced text recognition

### Step 3: Build Process

#### Using Build Scripts (Recommended)
```bash
# macOS/Linux
./build.sh --help           # Show options
./build.sh                  # Default build
./build.sh --debug --test   # Debug build with tests

# Windows
build.bat --help            # Show options
build.bat                   # Default build
build.bat --debug --test    # Debug build with tests
```

#### Manual CMake Build
```bash
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
cmake --build . --parallel
cmake --install . --prefix ../dist
```

### Step 4: Model Setup

```bash
# Create models directory
mkdir -p models

# Download Whisper base model (recommended)
wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin -O models/ggml-base.en.bin

# Alternative: Smaller model for lower-end hardware
wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.en.bin -O models/ggml-tiny.en.bin
```

## 🚀 Usage

### Command Line Options

```bash
dsax-godmode [OPTIONS]

Options:
  --help, -h           Show help message
  --version, -v        Show version information
  --test, -t           Run in test mode with manual input
  --no-audio           Disable audio capture (use fallbacks only)
  --no-overlay         Disable GPU overlay (console output only)
  --no-stealth         Disable stealth mode (for debugging)
  --confidence N       Set confidence threshold (0.0-1.0, default 0.7)
  --language LANG      Set preferred language (java, cpp, python, auto)
  --verbose            Enable verbose output
```

### Modes of Operation

#### 🧪 Test Mode
```bash
# Interactive testing with manual input
dsax-godmode --test

# Example questions to try:
# - "Implement binary search in Java"
# - "Design a scalable chat system"
# - "Tell me about a challenging project"
# - "Explain the difference between stack and queue"
```

#### 🎯 Production Mode
```bash
# Full stealth operation for interviews
dsax-godmode

# With custom settings
dsax-godmode --confidence 0.8 --language python
```

#### 🔍 Debug Mode
```bash
# Visible operation for testing and debugging
dsax-godmode --no-stealth --verbose
```

### Audio Setup

#### macOS Configuration
1. **System Preferences** → **Sound** → **Output**
2. Select **BlackHole 2ch** as output device
3. Applications will now route audio through BlackHole
4. DSA-X GODMODE++ will capture this audio stream

#### Windows Configuration
1. **Settings** → **System** → **Sound**
2. Set **CABLE Input** as default playback device
3. Applications will route audio through VB-Cable
4. DSA-X GODMODE++ will capture from CABLE Output

### Question Types Supported

| Category | Subcategories | Languages |
|----------|---------------|-----------|
| **DSA** | Algorithms, Data Structures, Complexity Analysis | Java, C++, Python |
| **System Design** | HLD, LLD, Scalability, Architecture | All |
| **Behavioral** | STAR Method, Leadership, Projects | All |
| **OOP** | Design Patterns, SOLID Principles | Java, C++, Python |
| **OS** | Processes, Threads, Memory, Synchronization | All |
| **DBMS** | SQL, NoSQL, Transactions, Indexing | All |
| **Networking** | Protocols, APIs, Security | All |

## 🔐 Stealth Features

### Zero-Trace Operation
- **No file writes**: Everything operates in RAM
- **No registry access**: No persistent configuration
- **No network calls**: Completely offline operation
- **No logging**: No traces left on system

### Anti-Detection
- **Process cloaking**: Appears as system process
- **GPU-only overlay**: Invisible to screen capture
- **Anti-debugging**: Detects and evades analysis tools
- **Self-healing**: Automatic recovery from failures

### Screen-Share Invisibility
- Uses GPU rendering that bypasses most screen capture
- DirectX/Metal exclusive contexts
- Click-through transparent windows
- Zero taskbar/dock presence

## 🧪 Testing & Validation

### Unit Tests
```bash
# Run integrated test suite
dsax-godmode --test

# Test individual components
python3 stt/fallback_clipboard.py
python3 stt/fallback_ocr.py
```

### Performance Testing
```bash
# Audio latency test
dsax-godmode --test --verbose

# Memory usage monitoring
top -p $(pgrep dsax-godmode)

# STT accuracy validation
# Use provided test audio samples
```

### Stealth Validation
```bash
# Process visibility test
ps aux | grep dsax-godmode

# Screen capture test
# Record screen while overlay is active

# Network traffic monitoring
netstat -an | grep dsax-godmode
```

## 📊 Performance Metrics

### Latency Targets
- **Audio Capture**: <10ms
- **STT Processing**: 200-500ms
- **AI Generation**: 100-300ms
- **Overlay Update**: <16ms (60fps)
- **Total Response**: <800ms

### Resource Usage
- **Memory**: 1-3GB (depends on model size)
- **CPU**: 15-30% (during processing)
- **GPU**: Minimal (overlay rendering only)
- **Disk**: 0 bytes (RAM-only operation)

## 🔧 Troubleshooting

### Common Issues

#### Audio Not Captured
```bash
# macOS: Check BlackHole installation
system_profiler SPAudioDataType | grep BlackHole

# Windows: Check VB-Cable installation
# Look for "CABLE Input/Output" in Sound settings
```

#### STT Not Working
```bash
# Check Whisper model
ls -la models/
file models/ggml-base.en.bin

# Test Whisper directly
# whisper --model models/ggml-base.en.bin test_audio.wav
```

#### Build Errors
```bash
# Check dependencies
cmake --version
python3 --version

# Clean rebuild
./build.sh --clean --verbose
```

#### Overlay Not Visible
```bash
# Check GPU support
# macOS: Check Metal support
# Windows: Check DirectX support

# Test without stealth
dsax-godmode --no-stealth --test
```

### Debug Mode
```bash
# Full debug output
dsax-godmode --no-stealth --verbose --test

# Check system status
dsax-godmode --version
```

## 🛡️ Security & Ethics

### Intended Use
- **Educational purposes**: Learning interview techniques
- **Research**: AI and speech processing research
- **Skill development**: Improving technical communication

### Responsible Usage
- Respect interview policies and guidelines
- Use for learning and preparation, not deception
- Understand the ethical implications
- Follow applicable laws and regulations

### Legal Notice
This software is provided for educational and research purposes only. Users are responsible for compliance with applicable laws, regulations, and policies. The authors disclaim any liability for misuse.

## 🤝 Contributing

### Development Setup
```bash
# Fork and clone
git clone https://github.com/yourusername/DSA-X-GODMODE.git
cd DSA-X-GODMODE

# Create development build
./build.sh --debug

# Run tests
dsax-godmode --test
```

### Code Standards
- **C++17** for core components
- **Python 3.8+** for fallback systems
- **CMake** for build configuration
- **Comprehensive testing** for all features

### Pull Request Process
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

**Educational/Research Use Only**

This project is licensed for educational and research purposes. Commercial use is prohibited without explicit permission.

## 🔗 Resources

### Documentation
- [Project Overview](PROJECT_OVERVIEW.md)
- [Implementation Status](IMPLEMENTATION_STATUS.md)
- [Architecture Deep Dive](docs/ARCHITECTURE.md)

### External Dependencies
- [Whisper.cpp](https://github.com/ggerganov/whisper.cpp) - Speech-to-text
- [BlackHole](https://existential.audio/blackhole/) - macOS audio routing
- [VB-Audio Cable](https://vb-audio.com/Cable/) - Windows audio routing

### Community
- [GitHub Issues](https://github.com/ishwetraj17/DSA-X-GODMODE/issues)
- [Discussions](https://github.com/ishwetraj17/DSA-X-GODMODE/discussions)

---

**Implemented by Shwet Raj**  
*Elite Systems Architect & Anti-Detection Specialist*

**For Educational and Research Purposes Only** ⚖️
