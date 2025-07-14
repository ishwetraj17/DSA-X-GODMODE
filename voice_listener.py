#!/usr/bin/env python3
"""
DSA-X GODMODE++ Voice Listener
Real-time voice transcription using OpenAI Whisper
"""

import pyaudio
import wave
import threading
import time
import numpy as np
import whisper
import tempfile
import os
from typing import Optional, Callable
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VoiceListener:
    def __init__(self, callback: Optional[Callable] = None, model_size: str = "base"):
        """
        Initialize the voice listener
        
        Args:
            callback: Function to call when speech is transcribed
            model_size: Whisper model size (tiny, base, small, medium, large)
        """
        self.callback = callback
        self.running = False
        self.thread = None
        self.last_transcription = ""
        
        # Audio settings
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.silence_threshold = 0.01
        self.silence_duration = 1.0  # seconds of silence to trigger processing
        
        # Initialize Whisper model
        try:
            logger.info(f"Loading Whisper model: {model_size}")
            self.whisper_model = whisper.load_model(model_size)
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            logger.info("Please install whisper: pip install openai-whisper")
            self.whisper_model = None
        
        # Initialize PyAudio
        try:
            self.audio = pyaudio.PyAudio()
            logger.info("PyAudio initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize PyAudio: {e}")
            logger.info("Please install PyAudio: pip install pyaudio")
            self.audio = None
    
    def record_audio(self, duration: float = 5.0) -> Optional[np.ndarray]:
        """Record audio for a specified duration"""
        if not self.audio:
            return None
        
        try:
            stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            
            frames = []
            for _ in range(0, int(self.rate / self.chunk * duration)):
                data = stream.read(self.chunk)
                frames.append(data)
            
            stream.stop_stream()
            stream.close()
            
            # Convert to numpy array
            audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
            return audio_data
            
        except Exception as e:
            logger.error(f"Audio recording failed: {e}")
            return None
    
    def detect_speech(self, duration: float = 10.0) -> Optional[np.ndarray]:
        """Detect speech and return audio when speech ends"""
        if not self.audio:
            return None
        
        try:
            stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            
            frames = []
            silence_counter = 0
            silence_threshold_samples = int(self.silence_duration * self.rate / self.chunk)
            
            logger.info("Listening for speech...")
            
            while self.running:
                data = stream.read(self.chunk)
                frames.append(data)
                
                # Check audio level
                audio_data = np.frombuffer(data, dtype=np.int16)
                audio_level = np.abs(audio_data).mean() / 32768.0
                
                if audio_level < self.silence_threshold:
                    silence_counter += 1
                else:
                    silence_counter = 0
                
                # If we have enough audio and silence, process it
                if len(frames) > 50 and silence_counter > silence_threshold_samples:
                    break
                
                # Maximum recording time
                if len(frames) > int(self.rate / self.chunk * duration):
                    break
            
            stream.stop_stream()
            stream.close()
            
            if len(frames) > 10:  # Minimum audio length
                audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
                return audio_data
            
            return None
            
        except Exception as e:
            logger.error(f"Speech detection failed: {e}")
            return None
    
    def transcribe_audio(self, audio_data: np.ndarray) -> str:
        """Transcribe audio using Whisper"""
        if not self.whisper_model or audio_data is None:
            return ""
        
        try:
            # Save audio to temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_filename = temp_file.name
            
            # Save as WAV file
            with wave.open(temp_filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.format))
                wf.setframerate(self.rate)
                wf.writeframes(audio_data.tobytes())
            
            # Transcribe with Whisper
            result = self.whisper_model.transcribe(temp_filename)
            transcription = result["text"].strip()
            
            # Clean up temporary file
            os.unlink(temp_filename)
            
            return transcription
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            return ""
    
    def is_dsa_question(self, text: str) -> bool:
        """Check if transcribed text contains a DSA question"""
        if not text or len(text) < 10:
            return False
        
        # Convert to lowercase for pattern matching
        text_lower = text.lower()
        
        # DSA-related keywords
        dsa_keywords = [
            'leetcode', 'geeksforgeeks', 'coding problem', 'algorithm',
            'data structure', 'array', 'linked list', 'tree', 'graph',
            'stack', 'queue', 'heap', 'sort', 'search', 'binary',
            'dynamic programming', 'recursion', 'backtracking',
            'two pointers', 'sliding window', 'hash map', 'hash set',
            'time complexity', 'space complexity', 'optimize',
            'given an array', 'find the', 'return the', 'maximum',
            'minimum', 'sum', 'count', 'reverse', 'merge', 'sort'
        ]
        
        # Check for DSA keywords
        keyword_count = sum(1 for keyword in dsa_keywords if keyword in text_lower)
        
        # Also check for question patterns
        question_patterns = ['how to', 'what is', 'find', 'solve', 'implement']
        question_count = sum(1 for pattern in question_patterns if pattern in text_lower)
        
        return keyword_count >= 2 or question_count >= 1
    
    def listen_continuously(self):
        """Main listening loop"""
        logger.info("Starting voice listener...")
        
        while self.running:
            try:
                # Detect speech
                audio_data = self.detect_speech()
                
                if audio_data is not None and len(audio_data) > 0:
                    # Transcribe the audio
                    transcription = self.transcribe_audio(audio_data)
                    
                    if transcription and transcription != self.last_transcription:
                        logger.info(f"Transcribed: {transcription}")
                        
                        # Check if it's a DSA question
                        if self.is_dsa_question(transcription):
                            logger.info("DSA question detected in voice input!")
                            
                            # Call callback if provided
                            if self.callback:
                                self.callback(transcription, "voice")
                            
                            self.last_transcription = transcription
                
                time.sleep(0.1)  # Small delay to prevent excessive CPU usage
                
            except Exception as e:
                logger.error(f"Voice listening error: {e}")
                time.sleep(1)
    
    def start(self):
        """Start the voice listener in a separate thread"""
        if not self.running and self.audio and self.whisper_model:
            self.running = True
            self.thread = threading.Thread(target=self.listen_continuously, daemon=True)
            self.thread.start()
            logger.info("Voice listener started")
        else:
            logger.error("Cannot start voice listener - missing dependencies")
    
    def stop(self):
        """Stop the voice listener"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        
        if self.audio:
            self.audio.terminate()
        
        logger.info("Voice listener stopped")
    
    def test_microphone(self):
        """Test microphone functionality"""
        if not self.audio:
            logger.error("PyAudio not available")
            return False
        
        try:
            # Get available input devices
            info = self.audio.get_host_api_info_by_index(0)
            numdevices = info.get('deviceCount')
            
            logger.info("Available audio input devices:")
            for i in range(0, numdevices):
                device_info = self.audio.get_device_info_by_host_api_device_index(0, i)
                if device_info.get('maxInputChannels') > 0:
                    logger.info(f"Input Device id {i} - {device_info.get('name')}")
            
            return True
        except Exception as e:
            logger.error(f"Microphone test failed: {e}")
            return False

def test_voice_listener():
    """Test function for the voice listener"""
    def on_speech_detected(text, source):
        print(f"Detected from {source}: {text}")
    
    listener = VoiceListener(callback=on_speech_detected)
    
    # Test microphone
    if not listener.test_microphone():
        print("Microphone test failed. Please check your audio setup.")
        return
    
    try:
        listener.start()
        print("Voice listener running. Speak a DSA question. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        listener.stop()
        print("Voice listener stopped.")

if __name__ == "__main__":
    test_voice_listener()