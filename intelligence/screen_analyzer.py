"""
DSA-X GODMODE++: REAL-TIME INTELLIGENCE MODE
Advanced Screen Analysis Engine

Implemented by Shwet Raj
Classification: OMNISCIENT INTELLIGENCE
Debug checkpoint: Real-time screen question detection
"""

import cv2
import numpy as np
import pytesseract
import threading
import time
import re
from PIL import Image, ImageGrab
from datetime import datetime
import hashlib
import logging
from typing import Dict, List, Tuple, Optional
import mss
import queue

class ScreenAnalyzer:
    def __init__(self):
        self.is_running = False
        self.analysis_thread = None
        self.question_queue = queue.Queue()
        self.last_detected_hash = None
        self.scan_interval = 2.0  # seconds
        self.roi_coordinates = None  # Region of Interest
        self.confidence_threshold = 0.7
        
        # OCR configuration
        self.ocr_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,?!()[]{}:;-+*/%=<>@#$&'
        
        # Question detection patterns
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
            r'(?i)optimize\s+(?:the|this)?',
            r'leetcode|geeksforgeeks|hackerrank|codechef'
        ]
        
        # Subject classification keywords
        self.subject_keywords = {
            'DSA': [
                'algorithm', 'data structure', 'array', 'string', 'tree', 'graph',
                'linked list', 'stack', 'queue', 'heap', 'hash', 'sorting',
                'searching', 'dynamic programming', 'greedy', 'recursion',
                'backtracking', 'binary search', 'bfs', 'dfs', 'dijkstra'
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
                'message queue', 'pub/sub', 'distributed system'
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
        
        # Screen capture initialization
        self.sct = mss.mss()
        
    def start_analysis(self, roi: Optional[Tuple[int, int, int, int]] = None):
        """Start continuous screen analysis"""
        if self.is_running:
            self.logger.warning("Screen analysis already running")
            return
            
        self.roi_coordinates = roi
        self.is_running = True
        self.analysis_thread = threading.Thread(target=self._analysis_loop, daemon=True)
        self.analysis_thread.start()
        self.logger.info("🔍 Screen analysis started")
        
    def stop_analysis(self):
        """Stop screen analysis"""
        self.is_running = False
        if self.analysis_thread:
            self.analysis_thread.join()
        self.logger.info("🛑 Screen analysis stopped")
        
    def _analysis_loop(self):
        """Main analysis loop running in background thread"""
        while self.is_running:
            try:
                # Capture screen
                screenshot = self._capture_screen()
                if screenshot is None:
                    time.sleep(self.scan_interval)
                    continue
                
                # Process image
                processed_image = self._preprocess_image(screenshot)
                
                # Extract text
                extracted_text = self._extract_text(processed_image)
                
                # Detect questions
                detected_questions = self._detect_questions(extracted_text)
                
                # Queue new questions
                for question in detected_questions:
                    if self._is_new_question(question):
                        self.question_queue.put({
                            'text': question,
                            'timestamp': datetime.now(),
                            'source': 'screen',
                            'confidence': self._calculate_confidence(question),
                            'subject': self._classify_subject(question)
                        })
                        self.logger.info(f"📋 New question detected: {question[:50]}...")
                        
            except Exception as e:
                self.logger.error(f"Error in analysis loop: {e}")
                
            time.sleep(self.scan_interval)
            
    def _capture_screen(self) -> Optional[np.ndarray]:
        """Capture screen or region of interest"""
        try:
            if self.roi_coordinates:
                # Capture specific region
                x, y, w, h = self.roi_coordinates
                monitor = {'top': y, 'left': x, 'width': w, 'height': h}
            else:
                # Capture entire screen
                monitor = self.sct.monitors[1]  # Primary monitor
                
            screenshot = self.sct.grab(monitor)
            img_array = np.array(screenshot)
            return cv2.cvtColor(img_array, cv2.COLOR_BGRA2BGR)
            
        except Exception as e:
            self.logger.error(f"Failed to capture screen: {e}")
            return None
            
    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for better OCR accuracy"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Morphological operations to clean up
        kernel = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        # Scale up for better OCR
        scaled = cv2.resize(cleaned, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        
        return scaled
        
    def _extract_text(self, image: np.ndarray) -> str:
        """Extract text from preprocessed image using OCR"""
        try:
            # Convert numpy array to PIL Image
            pil_image = Image.fromarray(image)
            
            # Extract text using Tesseract
            text = pytesseract.image_to_string(pil_image, config=self.ocr_config)
            
            # Clean up extracted text
            cleaned_text = self._clean_text(text)
            
            return cleaned_text
            
        except Exception as e:
            self.logger.error(f"OCR extraction failed: {e}")
            return ""
            
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove excessive whitespace
        cleaned = re.sub(r'\s+', ' ', text)
        
        # Remove special characters that might interfere
        cleaned = re.sub(r'[^\w\s.,?!()[\]{}:;-+*/%=<>@#$&]', '', cleaned)
        
        # Strip leading/trailing whitespace
        cleaned = cleaned.strip()
        
        return cleaned
        
    def _detect_questions(self, text: str) -> List[str]:
        """Detect potential questions in extracted text"""
        questions = []
        
        # Split text into sentences
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:  # Too short to be a meaningful question
                continue
                
            # Check if sentence matches question patterns
            for pattern in self.question_patterns:
                if re.search(pattern, sentence):
                    questions.append(sentence)
                    break
                    
        return questions
        
    def _is_new_question(self, question: str) -> bool:
        """Check if this is a new question we haven't seen recently"""
        question_hash = hashlib.md5(question.encode()).hexdigest()
        
        if question_hash == self.last_detected_hash:
            return False
            
        self.last_detected_hash = question_hash
        return True
        
    def _calculate_confidence(self, question: str) -> float:
        """Calculate confidence score for detected question"""
        confidence = 0.0
        
        # Base confidence for having question keywords
        for pattern in self.question_patterns:
            if re.search(pattern, question):
                confidence += 0.2
                
        # Bonus for technical keywords
        for subject, keywords in self.subject_keywords.items():
            for keyword in keywords:
                if keyword.lower() in question.lower():
                    confidence += 0.1
                    
        # Penalty for very short questions
        if len(question) < 20:
            confidence -= 0.2
            
        # Bonus for proper question structure
        if question.strip().endswith('?'):
            confidence += 0.1
            
        return min(1.0, max(0.0, confidence))
        
    def _classify_subject(self, question: str) -> str:
        """Classify the subject area of the question"""
        question_lower = question.lower()
        subject_scores = {}
        
        for subject, keywords in self.subject_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in question_lower:
                    score += 1
            subject_scores[subject] = score
            
        # Return subject with highest score
        if subject_scores:
            best_subject = max(subject_scores, key=subject_scores.get)
            if subject_scores[best_subject] > 0:
                return best_subject
                
        return 'GENERAL'
        
    def set_roi(self, x: int, y: int, width: int, height: int):
        """Set region of interest for focused scanning"""
        self.roi_coordinates = (x, y, width, height)
        self.logger.info(f"ROI set to: {self.roi_coordinates}")
        
    def clear_roi(self):
        """Clear region of interest to scan full screen"""
        self.roi_coordinates = None
        self.logger.info("ROI cleared - scanning full screen")
        
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
            
    def set_scan_interval(self, interval: float):
        """Set the scanning interval in seconds"""
        self.scan_interval = max(0.5, interval)  # Minimum 0.5 seconds
        self.logger.info(f"Scan interval set to {self.scan_interval} seconds")
        
    def set_confidence_threshold(self, threshold: float):
        """Set minimum confidence threshold for question detection"""
        self.confidence_threshold = max(0.0, min(1.0, threshold))
        self.logger.info(f"Confidence threshold set to {self.confidence_threshold}")

# Example usage and testing
if __name__ == "__main__":
    analyzer = ScreenAnalyzer()
    
    print("🔍 Starting screen analysis...")
    analyzer.start_analysis()
    
    try:
        # Run for 30 seconds as a test
        for i in range(30):
            time.sleep(1)
            questions = analyzer.get_detected_questions()
            
            for question in questions:
                print(f"\n📋 Detected Question:")
                print(f"   Text: {question['text']}")
                print(f"   Subject: {question['subject']}")
                print(f"   Confidence: {question['confidence']:.2f}")
                print(f"   Timestamp: {question['timestamp']}")
                
    except KeyboardInterrupt:
        print("\n🛑 Stopping analysis...")
        
    finally:
        analyzer.stop_analysis()
        print("✅ Analysis stopped")