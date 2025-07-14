#!/usr/bin/env python3
"""
DSA-X GODMODE++: Ultra-Stealth AI Assistant
Setup and Installation Script

This script automates the installation and configuration of DSA-X GODMODE++
for technical interview assistance.

Implemented by Shwet Raj
Debug checkpoint: Automated setup and dependency management
"""

import os
import sys
import subprocess
import platform
import json
import urllib.request
import zipfile
import tarfile
import shutil
import tempfile
from pathlib import Path
import argparse
import logging

class DSAXSetup:
    def __init__(self):
        self.platform = platform.system().lower()
        self.arch = platform.machine().lower()
        self.python_version = sys.version_info
        self.setup_dir = Path(__file__).parent.absolute()
        self.models_dir = self.setup_dir / "models"
        self.dependencies_dir = self.setup_dir / "dependencies"
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(self.setup_dir / "setup.log")
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Dependencies and download URLs
        self.dependencies = {
            "whisper_model": {
                "base.en": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin",
                "small.en": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.en.bin"
            },
            "audio_drivers": {
                "macos": {
                    "blackhole": "https://github.com/ExistentialAudio/BlackHole/releases/download/v0.4.0/BlackHole.2ch.pkg"
                },
                "windows": {
                    "vb_cable": "https://download.vb-audio.com/Download_CABLE/VBCABLE_Driver_Pack43.zip"
                }
            },
            "build_tools": {
                "cmake": "https://cmake.org/download/",
                "vcpkg": "https://github.com/Microsoft/vcpkg.git"
            }
        }
        
    def print_banner(self):
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                    DSA-X GODMODE++                          ║
║               Ultra-Stealth AI Assistant                    ║
║                                                              ║
║  🎯 Technical Interview Assistant                           ║
║  🔊 Real-time Audio Capture                                 ║
║  🧠 AI-Powered Question Analysis                            ║
║  👁️  Screen-Share Invisible Overlay                         ║
║  🛡️  Advanced Stealth Features                              ║
║                                                              ║
║  Implemented by Shwet Raj                                   ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
        
    def check_system_requirements(self):
        """Check if the system meets minimum requirements"""
        self.logger.info("🔍 Checking system requirements...")
        
        requirements_met = True
        
        # Check Python version
        if self.python_version < (3, 8):
            self.logger.error(f"❌ Python 3.8+ required, found {self.python_version}")
            requirements_met = False
        else:
            self.logger.info(f"✅ Python {self.python_version.major}.{self.python_version.minor}")
            
        # Check platform support
        supported_platforms = ["windows", "darwin", "linux"]
        if self.platform not in supported_platforms:
            self.logger.error(f"❌ Unsupported platform: {self.platform}")
            requirements_met = False
        else:
            self.logger.info(f"✅ Platform: {self.platform}")
            
        # Check available disk space (at least 2GB)
        try:
            free_space = shutil.disk_usage(self.setup_dir)[2]
            required_space = 2 * 1024 * 1024 * 1024  # 2GB
            if free_space < required_space:
                self.logger.error(f"❌ Insufficient disk space: {free_space // (1024**3)}GB available, 2GB required")
                requirements_met = False
            else:
                self.logger.info(f"✅ Disk space: {free_space // (1024**3)}GB available")
        except Exception as e:
            self.logger.warning(f"⚠️  Could not check disk space: {e}")
            
        return requirements_met
        
    def create_directories(self):
        """Create necessary directory structure"""
        self.logger.info("📁 Creating directory structure...")
        
        directories = [
            "models/whisper",
            "dependencies/audio",
            "dependencies/build",
            "config",
            "logs",
            "build",
            "bin",
            "lib",
            "temp"
        ]
        
        for directory in directories:
            dir_path = self.setup_dir / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"  Created: {directory}")
            
    def install_python_dependencies(self):
        """Install Python dependencies"""
        self.logger.info("🐍 Installing Python dependencies...")
        
        try:
            # Upgrade pip first
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                         check=True, capture_output=True)
            
            # Install requirements
            requirements_file = self.setup_dir / "requirements.txt"
            if requirements_file.exists():
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)], 
                             check=True, capture_output=True)
                self.logger.info("✅ Python dependencies installed")
            else:
                self.logger.warning("⚠️  requirements.txt not found, installing core dependencies")
                core_deps = [
                    "numpy>=1.21.0",
                    "opencv-python>=4.5.0",
                    "pyaudio>=0.2.11",
                    "psutil>=5.8.0",
                    "requests>=2.25.0"
                ]
                for dep in core_deps:
                    subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                                 check=True, capture_output=True)
                    
        except subprocess.CalledProcessError as e:
            self.logger.error(f"❌ Failed to install Python dependencies: {e}")
            return False
            
        return True
        
    def download_file(self, url, destination, description="file"):
        """Download a file with progress indication"""
        self.logger.info(f"⬇️  Downloading {description}...")
        
        try:
            with urllib.request.urlopen(url) as response:
                total_size = int(response.headers.get('Content-Length', 0))
                
                with open(destination, 'wb') as f:
                    downloaded = 0
                    while True:
                        chunk = response.read(8192)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"\r  Progress: {progress:.1f}%", end="", flush=True)
                            
                print()  # New line after progress
                self.logger.info(f"✅ Downloaded {description}")
                return True
                
        except Exception as e:
            self.logger.error(f"❌ Failed to download {description}: {e}")
            return False
            
    def download_whisper_models(self):
        """Download Whisper models"""
        self.logger.info("🧠 Downloading Whisper models...")
        
        whisper_dir = self.models_dir / "whisper"
        
        # Download base.en model (required)
        base_model_path = whisper_dir / "ggml-base.en.bin"
        if not base_model_path.exists():
            success = self.download_file(
                self.dependencies["whisper_model"]["base.en"],
                base_model_path,
                "Whisper base.en model"
            )
            if not success:
                return False
        else:
            self.logger.info("✅ Whisper base.en model already exists")
            
        return True
        
    def setup_audio_drivers(self):
        """Setup platform-specific audio drivers"""
        self.logger.info("🔊 Setting up audio drivers...")
        
        if self.platform == "darwin":  # macOS
            return self.setup_macos_audio()
        elif self.platform == "windows":
            return self.setup_windows_audio()
        elif self.platform == "linux":
            return self.setup_linux_audio()
        else:
            self.logger.warning("⚠️  Platform-specific audio setup not implemented")
            return True
            
    def setup_macos_audio(self):
        """Setup BlackHole audio driver for macOS"""
        self.logger.info("🍎 Setting up macOS audio (BlackHole)...")
        
        # Check if BlackHole is already installed
        try:
            result = subprocess.run(["system_profiler", "SPAudioDataType"], 
                                  capture_output=True, text=True)
            if "BlackHole" in result.stdout:
                self.logger.info("✅ BlackHole already installed")
                return True
        except:
            pass
            
        self.logger.info("📥 BlackHole not found. Please install manually:")
        self.logger.info("  1. Download from: https://github.com/ExistentialAudio/BlackHole")
        self.logger.info("  2. Install the BlackHole.2ch.pkg")
        self.logger.info("  3. Configure as system audio input device")
        
        return True
        
    def setup_windows_audio(self):
        """Setup VB-Cable audio driver for Windows"""
        self.logger.info("🪟 Setting up Windows audio (VB-Cable)...")
        
        # Check if VB-Cable is installed
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                               r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
            for i in range(winreg.QueryInfoKey(key)[0]):
                subkey_name = winreg.EnumKey(key, i)
                try:
                    subkey = winreg.OpenKey(key, subkey_name)
                    display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                    if "VB-Audio Virtual Cable" in display_name:
                        self.logger.info("✅ VB-Cable already installed")
                        return True
                except:
                    continue
        except:
            pass
            
        self.logger.info("📥 VB-Cable not found. Please install manually:")
        self.logger.info("  1. Download from: https://vb-audio.com/Cable/")
        self.logger.info("  2. Install VBCABLE_Driver_Pack")
        self.logger.info("  3. Restart your computer")
        
        return True
        
    def setup_linux_audio(self):
        """Setup audio for Linux"""
        self.logger.info("🐧 Setting up Linux audio...")
        
        # Check for PulseAudio/ALSA
        try:
            subprocess.run(["pulseaudio", "--version"], 
                         check=True, capture_output=True)
            self.logger.info("✅ PulseAudio detected")
        except:
            self.logger.warning("⚠️  PulseAudio not found, checking ALSA...")
            try:
                subprocess.run(["aplay", "--version"], 
                             check=True, capture_output=True)
                self.logger.info("✅ ALSA detected")
            except:
                self.logger.error("❌ No audio system detected")
                return False
                
        return True
        
    def compile_cpp_components(self):
        """Compile C++ components using CMake"""
        self.logger.info("🔨 Compiling C++ components...")
        
        build_dir = self.setup_dir / "build"
        
        try:
            # Check for CMake
            subprocess.run(["cmake", "--version"], check=True, capture_output=True)
            
            # Configure
            configure_cmd = [
                "cmake",
                "-S", str(self.setup_dir),
                "-B", str(build_dir),
                "-DCMAKE_BUILD_TYPE=Release"
            ]
            
            if self.platform == "windows":
                configure_cmd.extend(["-G", "Visual Studio 16 2019"])
                
            subprocess.run(configure_cmd, check=True)
            
            # Build
            subprocess.run([
                "cmake", 
                "--build", str(build_dir),
                "--config", "Release"
            ], check=True)
            
            self.logger.info("✅ C++ components compiled successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"❌ Failed to compile C++ components: {e}")
            return False
        except FileNotFoundError:
            self.logger.error("❌ CMake not found. Please install CMake first.")
            return False
            
    def create_launch_scripts(self):
        """Create platform-specific launch scripts"""
        self.logger.info("📜 Creating launch scripts...")
        
        if self.platform == "windows":
            script_content = """@echo off
echo Starting DSA-X GODMODE++...
cd /d "%~dp0"
if exist "bin\\dsax.exe" (
    bin\\dsax.exe %*
) else (
    echo Error: dsax.exe not found. Please run setup.py first.
    pause
)
"""
            script_path = self.setup_dir / "start.bat"
            with open(script_path, 'w') as f:
                f.write(script_content)
                
        else:  # macOS/Linux
            script_content = """#!/bin/bash
echo "Starting DSA-X GODMODE++..."
cd "$(dirname "$0")"
if [ -f "bin/dsax" ]; then
    ./bin/dsax "$@"
else
    echo "Error: dsax not found. Please run setup.py first."
    exit 1
fi
"""
            script_path = self.setup_dir / "start.sh"
            with open(script_path, 'w') as f:
                f.write(script_content)
            os.chmod(script_path, 0o755)
            
        self.logger.info(f"✅ Launch script created: {script_path.name}")
        
    def verify_installation(self):
        """Verify that all components are properly installed"""
        self.logger.info("🔍 Verifying installation...")
        
        success = True
        
        # Check for executable
        exe_name = "dsax.exe" if self.platform == "windows" else "dsax"
        exe_path = self.setup_dir / "bin" / exe_name
        
        if exe_path.exists():
            self.logger.info("✅ Main executable found")
        else:
            self.logger.error("❌ Main executable not found")
            success = False
            
        # Check for Whisper model
        model_path = self.models_dir / "whisper" / "ggml-base.en.bin"
        if model_path.exists():
            self.logger.info("✅ Whisper model found")
        else:
            self.logger.error("❌ Whisper model not found")
            success = False
            
        # Check Python dependencies
        try:
            import numpy
            import cv2
            self.logger.info("✅ Core Python dependencies available")
        except ImportError as e:
            self.logger.error(f"❌ Missing Python dependency: {e}")
            success = False
            
        return success
        
    def show_next_steps(self):
        """Show next steps after installation"""
        self.logger.info("\n🎉 Installation completed!")
        
        print("\n" + "="*60)
        print("NEXT STEPS:")
        print("="*60)
        
        if self.platform == "windows":
            print("1. Run 'start.bat' to launch DSA-X GODMODE++")
        else:
            print("1. Run './start.sh' to launch DSA-X GODMODE++")
            
        print("2. Configure audio input:")
        if self.platform == "darwin":
            print("   - Set BlackHole 2ch as system audio output")
            print("   - Applications will route audio through BlackHole")
        elif self.platform == "windows":
            print("   - Set 'CABLE Input' as system default playback device")
            print("   - Applications will route audio through VB-Cable")
        else:
            print("   - Configure audio loopback or virtual audio cable")
            
        print("3. Test the system:")
        print("   - Join a test video call")
        print("   - Ask a technical question")
        print("   - Verify overlay appears with AI response")
        
        print("\n4. Stealth features are enabled by default")
        print("5. Check 'config/dsax_config.json' for customization")
        
        print("\n" + "="*60)
        print("IMPORTANT SECURITY NOTES:")
        print("="*60)
        print("- Use only for educational/practice purposes")
        print("- Respect interview policies and guidelines")
        print("- Ensure legal compliance in your jurisdiction")
        print("="*60)
        
    def run_setup(self, skip_compile=False):
        """Run the complete setup process"""
        self.print_banner()
        
        self.logger.info("🚀 Starting DSA-X GODMODE++ setup...")
        
        # Check system requirements
        if not self.check_system_requirements():
            self.logger.error("❌ System requirements not met")
            return False
            
        # Create directories
        self.create_directories()
        
        # Install Python dependencies
        if not self.install_python_dependencies():
            self.logger.error("❌ Failed to install Python dependencies")
            return False
            
        # Download Whisper models
        if not self.download_whisper_models():
            self.logger.error("❌ Failed to download Whisper models")
            return False
            
        # Setup audio drivers
        if not self.setup_audio_drivers():
            self.logger.error("❌ Failed to setup audio drivers")
            return False
            
        # Compile C++ components
        if not skip_compile:
            if not self.compile_cpp_components():
                self.logger.error("❌ Failed to compile C++ components")
                return False
        else:
            self.logger.info("⏭️  Skipping C++ compilation")
            
        # Create launch scripts
        self.create_launch_scripts()
        
        # Verify installation
        if not skip_compile:
            if not self.verify_installation():
                self.logger.warning("⚠️  Installation verification failed")
                
        # Show next steps
        self.show_next_steps()
        
        return True

def main():
    parser = argparse.ArgumentParser(description="DSA-X GODMODE++ Setup Script")
    parser.add_argument("--skip-compile", action="store_true", 
                       help="Skip C++ compilation step")
    parser.add_argument("--verbose", action="store_true",
                       help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        
    setup = DSAXSetup()
    
    try:
        success = setup.run_setup(skip_compile=args.skip_compile)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        setup.logger.error(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()