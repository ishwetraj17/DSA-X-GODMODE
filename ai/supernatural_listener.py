"""
DSA-X GODMODE++: SUPERNATURAL LISTENER SYSTEM  
Real-Time Audio Monitoring & Question Detection

Implemented by Shwet Raj
Classification: SUPERNATURAL AUDIO INTELLIGENCE
Debug checkpoint: Omniscient audio perception
"""

import pyaudio
import wave
import threading
import time
import queue
import numpy as np
import whisper
import torch
import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import speech_recognition as sr
from collections import deque
import webrtcvad
import io
import warnings
warnings.filterwarnings("ignore")

@dataclass
class AudioQuestion:
    text: str
    question_type: str
    difficulty: str
    confidence: float
    timestamp: datetime
    audio_duration: float
    source: str = "microphone"
    language: str = "english"

class SupernaturalListener:
    def __init__(self):
        self.is_active = False
        self.audio_thread = None
        self.processing_thread = None
        self.question_queue = queue.Queue()
        self.audio_buffer = deque(maxlen=50)  # 5 seconds at 10 chunks/sec
        
        # Audio configuration
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.channels = 1
        self.format = pyaudio.paInt16
        
        # Advanced audio processing
        self.noise_threshold = 0.01
        self.silence_threshold = 0.5  # seconds
        self.max_audio_length = 30.0  # seconds
        
        # Multiple recognition engines for supernatural accuracy
        self.whisper_model = None
        self.speech_recognizer = sr.Recognizer()
        self.vad = webrtcvad.Vad(3)  # Aggressiveness level 3
        
        # Question classification patterns (same as vision system)
        self.question_patterns = {
            'dsa': [
                r'given.*array', r'binary.*tree', r'linked.*list', r'time.*complexity',
                r'implement.*algorithm', r'find.*element', r'sort.*array', r'search.*tree',
                r'dynamic.*programming', r'graph.*traversal', r'sliding.*window',
                r'two.*pointer', r'backtrack', r'recursion', r'iteration', r'leetcode',
                r'write.*function', r'return.*result', r'optimize.*solution'
            ],
            'lld': [
                r'design.*pattern', r'class.*diagram', r'object.*oriented',
                r'inheritance', r'polymorphism', r'encapsulation', r'abstraction',
                r'solid.*principle', r'design.*system', r'low.*level.*design',
                r'uml.*diagram', r'factory.*pattern', r'singleton.*pattern'
            ],
            'hld': [
                r'system.*design', r'high.*level.*design', r'architecture',
                r'microservice', r'database.*design', r'scalability', r'load.*balancer',
                r'distributed.*system', r'caching', r'api.*design', r'design.*uber',
                r'design.*twitter', r'design.*whatsapp', r'design.*youtube'
            ],
            'dbms': [
                r'database', r'sql', r'nosql', r'join', r'normalization',
                r'transaction', r'acid', r'index', r'query.*optimization',
                r'relational.*model', r'primary.*key', r'foreign.*key',
                r'select.*from', r'create.*table', r'alter.*table'
            ],
            'oops': [
                r'class', r'object', r'inheritance', r'polymorphism',
                r'encapsulation', r'abstraction', r'constructor', r'destructor',
                r'virtual.*function', r'overloading', r'overriding', r'interface',
                r'abstract.*class', r'multiple.*inheritance'
            ],
            'theoretical': [
                r'explain', r'describe', r'what.*is', r'difference.*between',
                r'advantages', r'disadvantages', r'pros.*cons', r'compare',
                r'define', r'list.*features', r'characteristics'
            ]
        }
        
        # Audio quality enhancement
        self.enable_noise_reduction = True
        self.enable_echo_cancellation = True
        self.enable_auto_gain = True
        
        print("🎧 SUPERNATURAL LISTENER SYSTEM INITIALIZED")
    
    def activate_listener(self):
        """Activate supernatural audio monitoring"""
        if self.is_active:
            return True
        
        print("🎧 ACTIVATING SUPERNATURAL LISTENER...")
        
        # Initialize Whisper model
        try:
            print("🧠 Loading Whisper model...")
            self.whisper_model = whisper.load_model("base")
            print("✅ Whisper model loaded")
        except Exception as e:
            print(f"⚠️ Whisper loading error: {e}")
            self.whisper_model = None
        
        # Start audio processing
        self.is_active = True
        self.audio_thread = threading.Thread(target=self._audio_capture_loop, daemon=True)
        self.processing_thread = threading.Thread(target=self._audio_processing_loop, daemon=True)
        
        self.audio_thread.start()
        self.processing_thread.start()
        
        print("✅ SUPERNATURAL LISTENER ACTIVE - OMNISCIENT AUDIO PERCEPTION ENABLED")
        return True
    
    def deactivate_listener(self):
        """Deactivate listener system"""
        self.is_active = False
        
        if self.audio_thread:
            self.audio_thread.join(timeout=2)
        if self.processing_thread:
            self.processing_thread.join(timeout=2)
        
        print("🎧 Supernatural listener deactivated")
    
    def _audio_capture_loop(self):
        """Main audio capture loop with supernatural sensitivity"""
        print("🎧 Starting supernatural audio capture...")
        
        try:
            # Initialize PyAudio
            audio = pyaudio.PyAudio()
            
            # Find best input device
            input_device = self._find_best_input_device(audio)
            
            # Open audio stream
            stream = audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                input_device_index=input_device,
                frames_per_buffer=self.chunk_size
            )
            
            print(f"🎤 Audio stream opened (device: {input_device})")
            
            continuous_audio = []
            last_voice_time = time.time()
            
            while self.is_active:
                try:
                    # Capture audio chunk
                    data = stream.read(self.chunk_size, exception_on_overflow=False)
                    audio_chunk = np.frombuffer(data, dtype=np.int16)
                    
                    # Voice activity detection
                    is_speech = self._detect_voice_activity(data)
                    
                    if is_speech:
                        continuous_audio.extend(audio_chunk)
                        last_voice_time = time.time()
                    else:
                        # Check if we have accumulated speech and enough silence
                        silence_duration = time.time() - last_voice_time
                        
                        if continuous_audio and silence_duration > self.silence_threshold:
                            # Process accumulated audio
                            audio_data = np.array(continuous_audio, dtype=np.int16)
                            audio_duration = len(audio_data) / self.sample_rate
                            
                            if 0.5 <= audio_duration <= self.max_audio_length:
                                self.audio_buffer.append({
                                    'data': audio_data,
                                    'duration': audio_duration,
                                    'timestamp': datetime.now()
                                })
                            
                            continuous_audio = []
                    
                except Exception as e:
                    print(f"🎧 Audio capture error: {e}")
                    time.sleep(0.1)
            
            # Cleanup
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
        except Exception as e:
            print(f"❌ Audio capture failed: {e}")
        
        print("🎧 Audio capture stopped")
    
    def _audio_processing_loop(self):
        """Audio processing loop with supernatural intelligence"""
        print("🧠 Starting supernatural audio processing...")
        
        while self.is_active:
            try:
                if self.audio_buffer:
                    # Get audio chunk
                    audio_chunk = self.audio_buffer.popleft()
                    
                    # Process with multiple recognition engines
                    questions = self._process_audio_chunk(audio_chunk)
                    
                    # Add valid questions to queue
                    for question in questions:
                        if self._validate_audio_question(question):
                            self.question_queue.put(question)
                            print(f"🔍 AUDIO QUESTION DETECTED: {question.question_type.upper()} - {question.text[:100]}...")
                
                else:
                    time.sleep(0.1)
                    
            except Exception as e:
                print(f"🧠 Audio processing error: {e}")
                time.sleep(0.5)
        
        print("🧠 Audio processing stopped")
    
    def _find_best_input_device(self, audio: pyaudio.PyAudio) -> Optional[int]:
        """Find the best audio input device"""
        default_device = audio.get_default_input_device_info()
        
        # Look for specific device names that might be better
        preferred_devices = [
            'blackhole', 'vb-audio', 'voicemeeter', 'soundflower',
            'virtual', 'stereo mix', 'what u hear'
        ]
        
        for i in range(audio.get_device_count()):
            try:
                device_info = audio.get_device_info_by_index(i)
                if device_info['maxInputChannels'] > 0:
                    device_name = device_info['name'].lower()
                    
                    for preferred in preferred_devices:
                        if preferred in device_name:
                            print(f"🎯 Found preferred device: {device_info['name']}")
                            return i
            except:
                continue
        
        return default_device['index'] if default_device else None
    
    def _detect_voice_activity(self, audio_data: bytes) -> bool:
        """Advanced voice activity detection"""
        try:
            # Simple energy-based detection
            audio_np = np.frombuffer(audio_data, dtype=np.int16)
            energy = np.sqrt(np.mean(audio_np**2))
            
            # WebRTC VAD (more accurate)
            if len(audio_data) == 320:  # 20ms at 16kHz
                try:
                    is_speech_vad = self.vad.is_speech(audio_data, self.sample_rate)
                    return energy > self.noise_threshold or is_speech_vad
                except:
                    pass
            
            return energy > self.noise_threshold
            
        except Exception as e:
            return False
    
    def _process_audio_chunk(self, audio_chunk: Dict) -> List[AudioQuestion]:
        """Process audio chunk with multiple recognition engines"""
        questions = []
        audio_data = audio_chunk['data']
        duration = audio_chunk['duration']
        timestamp = audio_chunk['timestamp']
        
        # Method 1: Whisper transcription
        if self.whisper_model:
            whisper_text = self._transcribe_with_whisper(audio_data)
            if whisper_text:
                questions.extend(self._create_questions_from_text(
                    whisper_text, duration, timestamp, "whisper", 0.9
                ))
        
        # Method 2: SpeechRecognition library
        sr_text = self._transcribe_with_speech_recognition(audio_data)
        if sr_text:
            questions.extend(self._create_questions_from_text(
                sr_text, duration, timestamp, "speech_recognition", 0.7
            ))
        
        return questions
    
    def _transcribe_with_whisper(self, audio_data: np.ndarray) -> Optional[str]:
        """Transcribe audio using Whisper with supernatural accuracy"""
        try:
            # Convert to float32 and normalize
            audio_float = audio_data.astype(np.float32) / 32768.0
            
            # Transcribe with Whisper
            result = self.whisper_model.transcribe(
                audio_float,
                language='en',
                task='transcribe',
                word_timestamps=False,
                fp16=torch.cuda.is_available()
            )
            
            text = result['text'].strip()
            return text if len(text) > 10 else None
            
        except Exception as e:
            print(f"🎤 Whisper transcription error: {e}")
            return None
    
    def _transcribe_with_speech_recognition(self, audio_data: np.ndarray) -> Optional[str]:
        """Transcribe audio using SpeechRecognition library"""
        try:
            # Convert to wav format in memory
            wav_buffer = io.BytesIO()
            with wave.open(wav_buffer, 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(self.sample_rate)
                wav_file.writeframes(audio_data.tobytes())
            
            wav_buffer.seek(0)
            
            # Use SpeechRecognition
            with sr.AudioFile(wav_buffer) as source:
                audio = self.speech_recognizer.record(source)
            
            # Try multiple services
            methods = [
                ('google', lambda: self.speech_recognizer.recognize_google(audio)),
                ('sphinx', lambda: self.speech_recognizer.recognize_sphinx(audio))
            ]
            
            for method_name, method_func in methods:
                try:
                    text = method_func()
                    if text and len(text.strip()) > 10:
                        return text.strip()
                except:
                    continue
            
            return None
            
        except Exception as e:
            print(f"🎤 SpeechRecognition error: {e}")
            return None
    
    def _create_questions_from_text(self, text: str, duration: float, 
                                  timestamp: datetime, source: str, 
                                  base_confidence: float) -> List[AudioQuestion]:
        """Create AudioQuestion objects from transcribed text"""
        questions = []
        
        if not text or len(text.strip()) < 10:
            return questions
        
        # Clean and normalize text
        text = self._clean_transcribed_text(text)
        
        # Classify question type
        question_type = self._classify_audio_question_type(text)
        
        if question_type != 'unknown':
            # Assess difficulty
            difficulty = self._assess_audio_difficulty(text)
            
            # Calculate confidence based on text quality
            confidence = self._calculate_text_confidence(text, base_confidence)
            
            question = AudioQuestion(
                text=text,
                question_type=question_type,
                difficulty=difficulty,
                confidence=confidence,
                timestamp=timestamp,
                audio_duration=duration,
                source=f"audio_{source}"
            )
            
            questions.append(question)
        
        return questions
    
    def _clean_transcribed_text(self, text: str) -> str:
        """Clean transcribed text for better processing"""
        # Remove filler words and normalize
        filler_words = [
            'um', 'uh', 'ah', 'er', 'like', 'you know', 'basically',
            'actually', 'literally', 'right', 'okay', 'so'
        ]
        
        # Split into words and filter
        words = text.lower().split()
        filtered_words = [word for word in words if word not in filler_words]
        
        # Rejoin and normalize punctuation
        cleaned = ' '.join(filtered_words)
        cleaned = re.sub(r'\s+', ' ', cleaned)  # Multiple spaces
        cleaned = re.sub(r'([.!?])\s*', r'\1 ', cleaned)  # Punctuation spacing
        
        return cleaned.strip()
    
    def _classify_audio_question_type(self, text: str) -> str:
        """Classify audio question type using supernatural pattern recognition"""
        text_lower = text.lower()
        
        # Score each category
        scores = {}
        for category, patterns in self.question_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower))
                score += matches
            
            # Boost score for category-specific keywords
            if category == 'dsa' and any(word in text_lower for word in ['algorithm', 'code', 'function', 'array', 'tree']):
                score += 2
            elif category == 'dbms' and any(word in text_lower for word in ['database', 'sql', 'table', 'query']):
                score += 2
            elif category == 'hld' and any(word in text_lower for word in ['system', 'design', 'architecture', 'scalable']):
                score += 2
            
            scores[category] = score
        
        # Return category with highest score
        if scores:
            best_category = max(scores.items(), key=lambda x: x[1])
            if best_category[1] > 0:
                return best_category[0]
        
        return 'unknown'
    
    def _assess_audio_difficulty(self, text: str) -> str:
        """Assess question difficulty from audio transcription"""
        text_lower = text.lower()
        
        # Difficulty indicators
        easy_indicators = ['basic', 'simple', 'easy', 'beginner', 'introduction', 'first']
        medium_indicators = ['medium', 'intermediate', 'moderate', 'standard', 'typical']
        hard_indicators = ['hard', 'difficult', 'complex', 'advanced', 'expert', 'optimal', 'efficient']
        
        easy_score = sum(1 for indicator in easy_indicators if indicator in text_lower)
        medium_score = sum(1 for indicator in medium_indicators if indicator in text_lower)
        hard_score = sum(1 for indicator in hard_indicators if indicator in text_lower)
        
        # Additional complexity analysis
        complexity_words = ['complexity', 'optimize', 'efficient', 'time', 'space', 'performance']
        hard_score += sum(1 for word in complexity_words if word in text_lower)
        
        if hard_score > medium_score and hard_score > easy_score:
            return 'hard'
        elif medium_score > easy_score:
            return 'medium'
        else:
            return 'easy'
    
    def _calculate_text_confidence(self, text: str, base_confidence: float) -> float:
        """Calculate confidence score based on text quality"""
        confidence = base_confidence
        
        # Boost confidence for clear question indicators
        question_indicators = ['what', 'how', 'why', 'implement', 'design', 'find', 'write']
        if any(indicator in text.lower() for indicator in question_indicators):
            confidence += 0.1
        
        # Reduce confidence for very short or very long text
        if len(text) < 20:
            confidence -= 0.2
        elif len(text) > 500:
            confidence -= 0.1
        
        # Boost confidence for technical terms
        technical_terms = ['algorithm', 'function', 'array', 'tree', 'database', 'system', 'design']
        tech_score = sum(1 for term in technical_terms if term in text.lower())
        confidence += min(tech_score * 0.05, 0.15)
        
        return max(0.0, min(1.0, confidence))
    
    def _validate_audio_question(self, question: AudioQuestion) -> bool:
        """Validate detected audio question"""
        # Basic validation
        if len(question.text) < 15:
            return False
        
        if question.confidence < 0.4:
            return False
        
        # Audio duration validation
        if question.audio_duration < 1.0 or question.audio_duration > 60.0:
            return False
        
        # Must contain question-like structure
        text_lower = question.text.lower()
        question_indicators = [
            '?', 'what', 'how', 'why', 'implement', 'design', 'find', 'write',
            'create', 'build', 'solve', 'explain', 'describe'
        ]
        
        has_question_indicator = any(indicator in text_lower for indicator in question_indicators)
        
        return has_question_indicator
    
    def get_audio_question(self) -> Optional[AudioQuestion]:
        """Get next audio question from queue"""
        try:
            return self.question_queue.get_nowait()
        except queue.Empty:
            return None
    
    def has_audio_questions(self) -> bool:
        """Check if audio questions are available"""
        return not self.question_queue.empty()
    
    def set_noise_threshold(self, threshold: float):
        """Set noise detection threshold"""
        self.noise_threshold = max(0.001, min(0.1, threshold))
        print(f"🔊 Noise threshold set to: {self.noise_threshold}")
    
    def set_silence_threshold(self, threshold: float):
        """Set silence detection threshold"""
        self.silence_threshold = max(0.1, min(5.0, threshold))
        print(f"🔇 Silence threshold set to: {self.silence_threshold}s")
    
    def get_listener_stats(self) -> Dict:
        """Get listener system statistics"""
        return {
            'is_active': self.is_active,
            'questions_pending': self.question_queue.qsize(),
            'audio_buffer_size': len(self.audio_buffer),
            'whisper_loaded': self.whisper_model is not None,
            'noise_threshold': self.noise_threshold,
            'silence_threshold': self.silence_threshold
        }

# Example usage
if __name__ == "__main__":
    listener = SupernaturalListener()
    listener.activate_listener()
    
    print("🔮 Listening for audio questions...")
    
    try:
        while True:
            if listener.has_audio_questions():
                question = listener.get_audio_question()
                print(f"🎧 Audio Question: {question.text}")
                print(f"🏷️ Type: {question.question_type}")
                print(f"⭐ Difficulty: {question.difficulty}")
                print(f"🎯 Confidence: {question.confidence:.2f}")
                print(f"⏱️ Duration: {question.audio_duration:.1f}s")
                print("-" * 80)
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        listener.deactivate_listener()
        print("🎧 Listener system stopped")