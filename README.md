# 🚀 DSA-X GODMODE++ Real-Time Intelligence System

> **The Ultimate AI-Powered DSA Problem Solver with Real-Time Screen Analysis and Voice Recognition**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

## 🌟 Features

### ✅ 1. SCREEN ANALYSIS (OCR)
- **Real-time screen monitoring** with intelligent OCR using Tesseract
- **Automatic DSA question detection** from LeetCode, GeeksforGeeks, etc.
- **Configurable regions** - monitor full screen or specific areas
- **Smart text preprocessing** for optimal OCR accuracy

### ✅ 2. VOICE INPUT (MICROPHONE)
- **Continuous voice listening** with OpenAI Whisper transcription
- **Real-time speech-to-text** conversion
- **DSA keyword detection** in spoken questions
- **Background processing** without blocking the system

### ✅ 3. QUESTION ROUTING & SOLVING
- **Intelligent question classification** (DSA, DBMS, OOP, System Design)
- **Multi-language code generation** (Python, Java, C++)
- **Optimized + brute-force solutions** for comprehensive coverage
- **Detailed explanations** with step-by-step breakdowns

### ✅ 4. MULTITHREADED ARCHITECTURE
- **Concurrent processing** of screen, voice, and solving
- **Priority-based question queue** for efficient handling
- **Non-blocking operations** for smooth user experience
- **Graceful shutdown** with signal handling

### ✅ 5. COMPREHENSIVE DOCUMENTATION
- **Full setup instructions** for all platforms
- **Detailed usage examples** and API documentation
- **Troubleshooting guide** for common issues
- **Performance optimization** tips

## 🛠️ Installation

### Prerequisites

- **Python 3.8+**
- **Tesseract OCR**
- **FFmpeg** (for Whisper)
- **Audio drivers** (for microphone support)

### 🔧 Platform-Specific Setup

#### 🍎 macOS (with Homebrew)

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install system dependencies
brew install tesseract
brew install portaudio
brew install ffmpeg

# Install Python dependencies
pip install -r requirements.txt
```

#### 🐧 Ubuntu/Debian Linux

```bash
# Update package list
sudo apt update

# Install system dependencies
sudo apt install -y tesseract-ocr
sudo apt install -y portaudio19-dev
sudo apt install -y python3-pyaudio
sudo apt install -y ffmpeg

# Install Python dependencies
pip install -r requirements.txt
```

#### 🪟 Windows (WSL2 Recommended)

```bash
# Install WSL2 if not already installed
wsl --install

# Inside WSL2, follow Ubuntu instructions above
# Or use Windows native installation:

# Download and install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
# Download and install FFmpeg from: https://ffmpeg.org/download.html
# Install Python dependencies
pip install -r requirements.txt
```

### 🚀 Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/DSA-X-GODMODE.git
cd DSA-X-GODMODE
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the system**
```bash
python dsa_godmode.py
```

## 📖 Usage

### 🎯 Basic Usage

```python
from dsa_godmode import DSAGodMode

# Create system instance
godmode = DSAGodMode()

# Set up callbacks for real-time notifications
def on_question_detected(text, source, routing_info):
    print(f"🎯 Question detected from {source}: {text[:100]}...")

def on_solution_ready(solution_result):
    print(f"✅ Solution ready: {solution_result['question'][:50]}...")

def on_error(error, context):
    print(f"❌ Error in {context}: {error}")

godmode.set_callbacks(on_question_detected, on_solution_ready, on_error)

# Start the system
godmode.start()

# The system will now:
# 1. Monitor your screen for DSA questions
# 2. Listen for voice input
# 3. Automatically solve detected questions
# 4. Provide detailed solutions with explanations
```

### ⚙️ Advanced Configuration

```python
# Custom configuration
config = {
    'screen_analysis': {
        'enabled': True,
        'region': (100, 100, 800, 600),  # Monitor specific region
        'interval': 1.5  # Faster scanning
    },
    'voice_listening': {
        'enabled': True,
        'model_size': 'small',  # Faster, less accurate
        'silence_duration': 0.5
    },
    'question_processing': {
        'max_queue_size': 50,
        'priority_voice': True,
        'auto_solve': True
    }
}

godmode = DSAGodMode(config)
```

### 🎤 Voice Commands

The system automatically detects DSA-related speech:

- **"Solve the two sum problem"**
- **"How to implement binary search?"**
- **"Explain dynamic programming"**
- **"What is the time complexity of quicksort?"**

### 📱 Manual Question Solving

```python
# Solve a question manually
question = "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target."
solution = godmode.solve_question_manually(question)
print(solution['explanation'])
```

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Screen        │    │   Voice         │    │   Manual        │
│   Analyzer      │    │   Listener      │    │   Input         │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │    Question Router        │
                    │  (Classification Engine)  │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │   Priority Queue          │
                    │  (Question Processing)    │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │   Solver Engine           │
                    │  (DSA + Theoretical)      │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │   Commentator             │
                    │  (Code + Explanation)     │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │   Output Handler          │
                    │  (Solutions + Stats)      │
                    └───────────────────────────┘
```

## 📊 Supported Question Types

### 🧮 DSA & Algorithms
- **Array Manipulation** (Two Sum, Kadane's Algorithm)
- **Linked Lists** (Reversal, Cycle Detection)
- **Trees & Graphs** (Traversal, BFS/DFS)
- **Dynamic Programming** (Fibonacci, Knapsack)
- **Sorting & Searching** (Quick Sort, Binary Search)
- **Stacks & Queues** (Implementation, Applications)

### 🗄️ Database & Theory
- **DBMS Concepts** (ACID, Normalization, Indexing)
- **SQL Queries** (JOINs, Subqueries, Optimization)
- **Transaction Management** (Isolation Levels, Deadlocks)

### 🏗️ System Design
- **Scalability** (Horizontal/Vertical Scaling)
- **Microservices** (Architecture, Communication)
- **Caching Strategies** (Redis, CDN, Load Balancing)
- **CAP Theorem** (Consistency, Availability, Partition Tolerance)

### 🎯 Object-Oriented Programming
- **OOP Principles** (Encapsulation, Inheritance, Polymorphism)
- **Design Patterns** (Singleton, Factory, Observer)
- **Language-Specific** (Java, C++, Python implementations)

## 🔧 Troubleshooting

### Common Issues

#### 1. Tesseract Not Found
```bash
# macOS
brew install tesseract

# Ubuntu
sudo apt install tesseract-ocr

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

#### 2. PyAudio Installation Issues
```bash
# macOS
brew install portaudio
pip install pyaudio

# Ubuntu
sudo apt install portaudio19-dev python3-pyaudio
pip install pyaudio

# Windows
pip install pipwin
pipwin install pyaudio
```

#### 3. Whisper Model Download Issues
```bash
# The first run will download the model automatically
# If you have network issues, download manually:
python -c "import whisper; whisper.load_model('base')"
```

#### 4. Screen Capture Permissions
- **macOS**: System Preferences → Security & Privacy → Privacy → Screen Recording
- **Linux**: Usually works out of the box
- **Windows**: May require running as administrator

### Performance Optimization

#### 1. Faster Processing
```python
config = {
    'voice_listening': {
        'model_size': 'tiny'  # Faster, less accurate
    },
    'screen_analysis': {
        'interval': 1.0  # More frequent scanning
    }
}
```

#### 2. GPU Acceleration (Optional)
```bash
# Install PyTorch with CUDA support
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```

#### 3. Memory Optimization
```python
config = {
    'question_processing': {
        'max_queue_size': 20  # Reduce memory usage
    }
}
```

## 📈 Performance Metrics

The system provides real-time statistics:

- **Questions Processed**: Total questions detected and solved
- **Solutions Generated**: Successful solution generations
- **Screen Detections**: OCR-based question detections
- **Voice Detections**: Speech-based question detections
- **Processing Time**: Average time per solution
- **Error Rate**: System reliability metrics

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone with submodules
git clone --recursive https://github.com/yourusername/DSA-X-GODMODE.git

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Format code
black .

# Lint code
flake8 .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI Whisper** for speech recognition
- **Tesseract OCR** for text extraction
- **OpenCV** for image processing
- **PyAudio** for audio capture
- **The DSA community** for inspiration and feedback

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/DSA-X-GODMODE/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/DSA-X-GODMODE/discussions)
- **Email**: support@dsa-godmode.com

## 🚀 Roadmap

- [ ] **Web Interface** - Browser-based control panel
- [ ] **Mobile App** - iOS/Android companion app
- [ ] **Cloud Integration** - Remote processing capabilities
- [ ] **Advanced AI** - GPT-4 integration for complex problems
- [ ] **Video Analysis** - YouTube tutorial processing
- [ ] **Collaborative Features** - Multi-user problem solving

---

**Made with ❤️ for the DSA community**

*Transform your coding interview preparation with AI-powered real-time assistance!*
