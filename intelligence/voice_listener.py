"""
DSA-X GODMODE++: REAL-TIME INTELLIGENCE MODE
Advanced Voice Listening Engine

Implemented by Shwet Raj
Classification: OMNISCIENT INTELLIGENCE
Debug checkpoint: Real-time voice question detection
"""

import whisper
import pyaudio
import wave
import threading
import time
import queue
import numpy as np
from datetime import datetime
import logging
import io
import tempfile
import os
from typing import Dict, List, Optional
import speech_recognition as sr
from collections import deque
import re

class VoiceListener:
    def __init__(self, model_size: str = "base"):
        self.is_listening = False
        self.listening_thread = None
        self.processing_thread = None
        self.question_queue = queue.Queue()
        self.audio_queue = queue.Queue()
        
        # Audio configuration
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.channels = 1
        self.format = pyaudio.paInt16
        self.record_seconds = 30  # Maximum recording length
        self.silence_threshold = 500  # Silence detection threshold
        self.silence_duration = 2.0  # Seconds of silence before processing
        
        # Whisper model initialization
        self.whisper_model = None
        self.model_size = model_size
        self.confidence_threshold = 0.7
        
        # Speech recognition fallback
        self.sr_recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Voice activity detection
        self.audio_buffer = deque(maxlen=self.sample_rate * 5)  # 5 seconds buffer
        self.is_speaking = False
        self.last_speech_time = 0
        
        # Question detection patterns (same as screen analyzer)
        self.question_patterns = [
            r'(?i)implement\s+(?:a|an|the)?\s*(\w+)',
            r'(?i)write\s+(?:a|an)?\s*(?:function|method|algorithm)',
            r'(?i)given\s+(?:a|an|the)?\s*(?:array|string|tree|graph|list)',
            r'(?i)find\s+(?:the|all)?\s*(?:\w+\s+)*(?:element|node|path|solution)',
            r'(?i)design\s+(?:a|an|the)?\s*(?:system|class|data\s+structure)',
            r'(?i)explain\s+(?:the|how|what|why)',
            r'(?i)what\s+(?:is|are|would|will)',
            r'(?i)how\s+(?:do|does|would|will|can)',
            r'(?i)compare\s+(?:and\s+contrast)?',
            r'(?i)difference\s+between',
            r'(?i)time\s+complexity',
            r'(?i)space\s+complexity',
            r'(?i)optimize\s+(?:the|this)?'
        ]
        
        # Subject classification keywords
        self.subject_keywords = {
            'DSA': [
                'algorithm', 'data structure', 'array', 'string', 'tree', 'graph',
                'linked list', 'stack', 'queue', 'heap', 'hash', 'sorting',
                'searching', 'dynamic programming', 'greedy', 'recursion',
                'backtracking', 'binary search', 'breadth first', 'depth first'
            ],
            'DBMS': [
                'database', 'sql', 'query', 'join', 'index', 'transaction',
                'acid', 'normalization', 'schema', 'table', 'primary key',
                'foreign key', 'stored procedure', 'trigger', 'view'
            ],
            'OOPS': [
                'class', 'object', 'inheritance', 'polymorphism', 'encapsulation',
                'abstraction', 'interface', 'abstract', 'virtual', 'override',
                'constructor', 'destructor', 'static', 'final'
            ],
            'SYSTEM_DESIGN': [
                'system design', 'scalability', 'load balancer', 'microservices',
                'database sharding', 'caching', 'cdn', 'api gateway',
                'message queue', 'pub sub', 'distributed system'
            ],
            'NETWORKS': [
                'tcp', 'udp', 'http', 'https', 'dns', 'firewall', 'router',
                'switch', 'protocol', 'osi model', 'subnet', 'vlan'
            ],
            'OS': [
                'operating system', 'process', 'thread', 'scheduling',
                'memory management', 'virtual memory', 'deadlock',
                'semaphore', 'mutex', 'file system'
            ]
        }
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # PyAudio initialization
        self.pyaudio_instance = pyaudio.PyAudio()
        
    def initialize_whisper(self):
        """Initialize Whisper model"""
        try:
            self.logger.info(f"Loading Whisper model ({self.model_size})...")
            self.whisper_model = whisper.load_model(self.model_size)
            self.logger.info("✅ Whisper model loaded successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to load Whisper model: {e}")
            return False
            
    def start_listening(self):
        """Start continuous voice listening"""
        if self.is_listening:
            self.logger.warning("Voice listening already active")
            return
            
        # Initialize Whisper if not already done
        if self.whisper_model is None:
            if not self.initialize_whisper():
                self.logger.error("Cannot start listening without Whisper model")
                return
                
        self.is_listening = True
        
        # Start listening thread
        self.listening_thread = threading.Thread(target=self._listening_loop, daemon=True)
        self.listening_thread.start()
        
        # Start processing thread
        self.processing_thread = threading.Thread(target=self._processing_loop, daemon=True)
        self.processing_thread.start()
        
        self.logger.info("🎤 Voice listening started")
        
    def stop_listening(self):
        """Stop voice listening"""
        self.is_listening = False
        
        if self.listening_thread:
            self.listening_thread.join()
        if self.processing_thread:
            self.processing_thread.join()
            
        self.logger.info("🛑 Voice listening stopped")
        
    def _listening_loop(self):
        """Main listening loop running in background thread"""
        stream = None
        try:
            # Open audio stream
            stream = self.pyaudio_instance.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            self.logger.info("🎙️ Audio stream opened, listening for speech...")
            
            audio_data = []
            silence_counter = 0
            
            while self.is_listening:
                try:
                    # Read audio chunk
                    data = stream.read(self.chunk_size, exception_on_overflow=False)
                    audio_chunk = np.frombuffer(data, dtype=np.int16)
                    
                    # Add to buffer for VAD
                    self.audio_buffer.extend(audio_chunk)
                    
                    # Voice Activity Detection
                    if self._detect_voice_activity(audio_chunk):
                        if not self.is_speaking:
                            self.logger.info("🗣️ Speech detected, recording...")
                            self.is_speaking = True
                            audio_data = []
                            
                        audio_data.append(data)
                        silence_counter = 0
                        self.last_speech_time = time.time()
                        
                    else:
                        if self.is_speaking:
                            silence_counter += 1
                            audio_data.append(data)
                            
                            # Check if enough silence to stop recording
                            silence_time = silence_counter * self.chunk_size / self.sample_rate
                            if silence_time >= self.silence_duration:
                                self.logger.info("🔇 Silence detected, processing audio...")
                                self._queue_audio_for_processing(audio_data)
                                self.is_speaking = False
                                audio_data = []
                                silence_counter = 0
                                
                    # Prevent buffer overflow
                    if len(audio_data) > self.sample_rate * self.record_seconds:
                        self.logger.info("⏰ Maximum recording time reached, processing...")
                        self._queue_audio_for_processing(audio_data)
                        self.is_speaking = False
                        audio_data = []
                        
                except Exception as e:
                    self.logger.error(f"Error in listening loop: {e}")
                    time.sleep(0.1)
                    
        except Exception as e:
            self.logger.error(f"Failed to open audio stream: {e}")
            
        finally:
            if stream:
                stream.stop_stream()
                stream.close()
                
    def _processing_loop(self):
        """Audio processing loop running in background thread"""
        while self.is_listening:
            try:
                # Get audio data from queue
                audio_data = self.audio_queue.get(timeout=1.0)
                
                # Process the audio
                transcription = self._transcribe_audio(audio_data)
                
                if transcription:
                    # Check if it's a question
                    if self._is_question(transcription):
                        question_data = {
                            'text': transcription,
                            'timestamp': datetime.now(),
                            'source': 'voice',
                            'confidence': self._calculate_confidence(transcription),
                            'subject': self._classify_subject(transcription)
                        }
                        
                        self.question_queue.put(question_data)
                        self.logger.info(f"🎤 Question detected: {transcription[:50]}...")
                        
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"Error in processing loop: {e}")
                
    def _queue_audio_for_processing(self, audio_data: List[bytes]):
        """Queue audio data for processing"""
        if not audio_data:
            return
            
        try:
            self.audio_queue.put(audio_data, block=False)
        except queue.Full:
            self.logger.warning("Audio queue full, dropping audio")
            
    def _detect_voice_activity(self, audio_chunk: np.ndarray) -> bool:
        """Simple voice activity detection based on volume"""
        # Calculate RMS (Root Mean Square) for volume detection
        rms = np.sqrt(np.mean(audio_chunk.astype(np.float32) ** 2))
        
        # Convert to decibels
        if rms > 0:
            db = 20 * np.log10(rms)
            return db > -40  # Threshold in dB
        return False
        
    def _transcribe_audio(self, audio_data: List[bytes]) -> Optional[str]:
        """Transcribe audio data using Whisper"""
        try:
            # Combine audio chunks
            combined_audio = b''.join(audio_data)
            
            # Convert to numpy array
            audio_array = np.frombuffer(combined_audio, dtype=np.int16).astype(np.float32) / 32768.0
            
            # Transcribe using Whisper
            result = self.whisper_model.transcribe(
                audio_array,
                language='en',
                task='transcribe',
                fp16=False
            )
            
            transcription = result['text'].strip()
            
            # Fallback to speech_recognition if Whisper fails or confidence is low
            if not transcription or len(transcription) < 5:
                transcription = self._fallback_transcription(combined_audio)
                
            return transcription if transcription else None
            
        except Exception as e:
            self.logger.error(f"Transcription failed: {e}")
            return None
            
    def _fallback_transcription(self, audio_data: bytes) -> Optional[str]:
        """Fallback transcription using speech_recognition library"""
        try:
            # Create temporary WAV file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                # Write WAV header and data
                with wave.open(temp_file.name, 'wb') as wav_file:
                    wav_file.setnchannels(self.channels)
                    wav_file.setsampwidth(self.pyaudio_instance.get_sample_size(self.format))
                    wav_file.setframerate(self.sample_rate)
                    wav_file.writeframes(audio_data)
                
                # Transcribe using speech_recognition
                with sr.AudioFile(temp_file.name) as source:
                    audio = self.sr_recognizer.record(source)
                    text = self.sr_recognizer.recognize_google(audio)
                    
                # Clean up
                os.unlink(temp_file.name)
                
                return text
                
        except Exception as e:
            self.logger.error(f"Fallback transcription failed: {e}")
            return None
            
    def _is_question(self, text: str) -> bool:
        """Check if transcribed text is a question"""
        # Check for question patterns
        for pattern in self.question_patterns:
            if re.search(pattern, text):
                return True
                
        # Check for question words
        question_words = ['what', 'how', 'why', 'when', 'where', 'which', 'who']
        first_word = text.split()[0].lower() if text.split() else ""
        
        if first_word in question_words:
            return True
            
        # Check if it ends with question mark (unlikely in speech but possible)
        if text.strip().endswith('?'):
            return True
            
        # Check for imperative statements that are questions
        imperative_patterns = [
            r'(?i)^(implement|write|design|explain|find|solve|create)',
            r'(?i)^(tell me|show me|give me)',
            r'(?i)^(can you|could you|would you)'
        ]
        
        for pattern in imperative_patterns:
            if re.search(pattern, text):
                return True
                
        return False
        
    def _calculate_confidence(self, text: str) -> float:
        """Calculate confidence score for detected question"""
        confidence = 0.0
        
        # Base confidence for having question patterns
        for pattern in self.question_patterns:
            if re.search(pattern, text):
                confidence += 0.2
                
        # Bonus for technical keywords
        for subject, keywords in self.subject_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text.lower():
                    confidence += 0.1
                    
        # Penalty for very short questions
        if len(text) < 10:
            confidence -= 0.2
            
        # Bonus for proper question structure
        if any(text.lower().startswith(word) for word in ['what', 'how', 'why', 'when', 'where']):
            confidence += 0.1
            
        return min(1.0, max(0.0, confidence))
        
    def _classify_subject(self, text: str) -> str:
        """Classify the subject area of the question"""
        text_lower = text.lower()
        subject_scores = {}
        
        for subject, keywords in self.subject_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    score += 1
            subject_scores[subject] = score
            
        # Return subject with highest score
        if subject_scores:
            best_subject = max(subject_scores, key=subject_scores.get)
            if subject_scores[best_subject] > 0:
                return best_subject
                
        return 'GENERAL'
        
    def get_detected_questions(self) -> List[Dict]:
        """Get all detected questions from queue"""
        questions = []
        while not self.question_queue.empty():
            try:
                questions.append(self.question_queue.get_nowait())
            except queue.Empty:
                break
        return questions
        
    def get_latest_question(self) -> Optional[Dict]:
        """Get the most recent detected question"""
        try:
            return self.question_queue.get_nowait()
        except queue.Empty:
            return None
            
    def set_confidence_threshold(self, threshold: float):
        """Set minimum confidence threshold for question detection"""
        self.confidence_threshold = max(0.0, min(1.0, threshold))
        self.logger.info(f"Confidence threshold set to {self.confidence_threshold}")
        
    def set_silence_duration(self, duration: float):
        """Set silence duration before processing audio"""
        self.silence_duration = max(0.5, duration)
        self.logger.info(f"Silence duration set to {self.silence_duration} seconds")
        
    def __del__(self):
        """Cleanup on destruction"""
        if hasattr(self, 'pyaudio_instance'):
            self.pyaudio_instance.terminate()

# Example usage and testing
if __name__ == "__main__":
    listener = VoiceListener(model_size="base")
    
    print("🎤 Starting voice listening...")
    listener.start_listening()
    
    try:
        # Run for 60 seconds as a test
        for i in range(60):
            time.sleep(1)
            questions = listener.get_detected_questions()
            
            for question in questions:
                print(f"\n🎤 Detected Question:")
                print(f"   Text: {question['text']}")
                print(f"   Subject: {question['subject']}")
                print(f"   Confidence: {question['confidence']:.2f}")
                print(f"   Timestamp: {question['timestamp']}")
                
    except KeyboardInterrupt:
        print("\n🛑 Stopping listening...")
        
    finally:
        listener.stop_listening()
        print("✅ Listening stopped")