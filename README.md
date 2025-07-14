# 🚀 DSA-X GODMODE++: Ultra-Stealth, Offline AI Assistant

> **Elite, compiler-level systems architect with expertise in Apple Silicon, LLMs, and anti-detection techniques**

## 👨‍💻 Overview

DSA-X GODMODE++ is an **offline, RAM-only, zero-trace AI assistant** designed for technical interviews. It can transcribe audio from speaker-only sources (Zoom, Meet) and provide intelligent responses for DSA, OS, DBMS, OOPs, STAR, and HLD/LLD questions in Java, C++, and Python.

## 🎯 Key Features

- 🧠 **Audio Transcription**: Captures speaker audio via BlackHole (macOS) or VB-Audio Cable (Windows)
- 💬 **Multi-Domain Expertise**: DSA, System Design, STAR, OOPs, OS, DBMS
- 👻 **Screen Share Invisible**: GPU-only overlay invisible in screen recordings
- 💾 **RAM-Only Operation**: No disk writes, no logs, no persistence
- 📦 **ZIP-Based**: Runs directly from ZIP archive, no installation required
- 🔐 **Zero-Trace**: Process cloaking, no registry access, no mic permissions

## 🛠️ Technical Architecture

### Platform Support
| Platform | Audio Capture | GPU Overlay | AI Engine |
|----------|---------------|-------------|-----------|
| macOS (M1-M3) | BlackHole | Metal | Whisper.cpp |
| Windows 10/11 | VB-Audio Cable | DirectX | Whisper.cpp |

### Core Components

#### 🔊 Audio Input System
- **macOS**: BlackHole virtual audio device integration
- **Windows**: VB-Audio Cable virtual audio routing
- **Fallback**: Clipboard monitoring → OCR capture → Manual input

#### 🖼️ GPU Overlay System
- **macOS**: Metal API with click-through, screen-share invisible rendering
- **Windows**: DirectX transparent window, no taskbar entry
- **Features**: GPU-drifted text, smooth animations, zero detection

#### 🧠 AI Processing Engine
- **STT**: Whisper.cpp with GGUF models (RAM-only)
- **LLM**: Local inference with prompt classification
- **Code Generation**: Multi-language output with obfuscation
- **Resume Matching**: FAISS-based similarity search

#### 🔐 Stealth System
- **Process Cloaking**: Disguises as `explorer.exe` or system process
- **Zero-Trace**: No logging, no file writes, no registry access
- **Anti-Detection**: Monitors for debugging tools, virtualization
- **Self-Healing**: Automatic fallback mechanisms and recovery

## 📁 Project Structure

```
DSA-X-GODMODE++/
├── boot/                          # Core system components
│   ├── audio_input_mac.cpp        # macOS BlackHole integration
│   ├── audio_input_windows.cpp    # Windows VB-Cable integration
│   ├── whisper_runner.cpp         # Whisper.cpp RAM-only processing
│   ├── self_healing.cpp           # System recovery and fallbacks
│   └── stealth_enforcer.cpp       # Zero-trace operation
├── overlay/                       # GPU overlay system
│   ├── overlay_mac.mm             # macOS Metal overlay
│   └── overlay_windows.cpp        # Windows DirectX overlay
├── stt/                          # Speech-to-text fallbacks
│   ├── fallback_clipboard.py      # Clipboard text capture
│   └── fallback_ocr.py           # Screen OCR capture
├── llm/                          # AI processing engine
│   ├── prompt_classifier.cpp      # Question type detection
│   ├── answer_generator.cpp       # Multi-language code generation
│   └── obfuscator.py             # Code uniqueness generation
├── resume/                       # Resume analysis system
│   ├── resume_parser.py          # Resume parsing and indexing
│   └── resume_index.faiss        # FAISS similarity search
├── test/                         # Testing and validation
│   ├── sample_audio.wav          # Audio test samples
│   └── dummy_resume.txt          # Resume test data
├── run_mac.command               # macOS launch script
├── run_win.bat                   # Windows launch script
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites

#### macOS
```bash
# Install BlackHole
brew install blackhole-2ch
# or download from: https://existential.audio/blackhole/
```

#### Windows
```bash
# Download and install VB-Audio Cable
# https://vb-audio.com/Cable/
```

### Installation

1. **Download**: Extract the ZIP archive
2. **Run**: Execute the appropriate launch script
   - macOS: `./run_mac.command`
   - Windows: `run_win.bat`

### Usage

1. **Launch**: Run the appropriate script for your platform
2. **Audio Setup**: Ensure BlackHole/VB-Cable is configured
3. **Interview**: Start your technical interview
4. **Responses**: AI responses appear as GPU overlay
5. **Exit**: Press Ctrl+C to exit (zero-trace cleanup)

## 🎓 Teaching Modes

### "Mock Me" - HR Simulation
- Behavioral question responses
- STAR method formatting
- HR-style follow-up questions

### "Quiz Me" - Resume Drills
- Technical skill assessment
- Project-based questions
- Experience validation

### "Socratic" - Q&A Bounce
- Progressive question generation
- Learning path guidance
- Knowledge gap identification

## 🔧 Configuration

### Environment Variables
```bash
DSAX_STEALTH_MODE=1      # Enable stealth mode
DSAX_RAM_ONLY=1          # RAM-only operation
DSAX_AUDIO_CAPTURE=blackhole  # Audio capture method
```

### Stealth Settings
- **Process Name**: `explorer.exe` (Windows) / `WindowServer` (macOS)
- **Logging**: Disabled (zero-trace)
- **File Writes**: Blocked (RAM-only)
- **Registry**: No access (registry-free)

## 🛡️ Security Features

### Anti-Detection
- Process cloaking and disguise
- Debugger detection and evasion
- Virtualization environment detection
- Monitoring tool detection

### Zero-Trace Operation
- No persistent file writes
- No system logging
- No registry modifications
- No network communication

### Self-Healing
- Automatic component recovery
- Fallback mechanism chains
- Resource usage optimization
- Memory management (3.2GB limit)

## 🧪 Testing

### Audio Testing
```bash
# Test audio capture
./test/sample_audio.wav

# Validate STT accuracy
# Test fallback mechanisms
```

### Resume Testing
```bash
# Test resume parsing
./test/dummy_resume.txt

# Validate FAISS indexing
# Test similarity search
```

### Stealth Testing
```bash
# Verify screen share invisibility
# Test process cloaking
# Validate zero-trace operation
```

## 🔍 Debug Checkpoints

Each component includes debug checkpoints for development:

```cpp
// Implemented by Shwet Raj
// Debug checkpoint: [component-specific location]
```

## 📋 Requirements

### System Requirements
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 100MB for ZIP archive
- **GPU**: Metal (macOS) / DirectX 11 (Windows)
- **Audio**: BlackHole (macOS) / VB-Audio Cable (Windows)

### Development Requirements
- **C++17**: Core system components
- **Python 3.8+**: AI processing and fallbacks
- **Metal/DirectX**: GPU overlay rendering
- **Whisper.cpp**: Speech-to-text processing

## 🤝 Contributing

This is a research project demonstrating advanced stealth and AI techniques. For educational purposes only.

## ⚖️ Legal Notice

This software is for educational and research purposes. Users are responsible for compliance with applicable laws and regulations. The authors disclaim any liability for misuse.

## 📄 License

Educational/Research Use Only

---

**Implemented by Shwet Raj**  
*Elite Systems Architect & Anti-Detection Specialist*
