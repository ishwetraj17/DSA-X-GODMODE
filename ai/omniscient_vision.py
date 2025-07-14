"""
DSA-X GODMODE++: OMNISCIENT VISION SYSTEM
Real-Time Screen Analysis & Question Detection

Implemented by Shwet Raj
Classification: SUPERNATURAL VISION INTELLIGENCE
Debug checkpoint: Omniscient screen perception
"""

import cv2
import numpy as np
import pytesseract
import threading
import time
import queue
import json
import re
from typing import List, Dict, Tuple, Optional
from PIL import Image, ImageGrab
from dataclasses import dataclass
import logging
from datetime import datetime

@dataclass
class DetectedQuestion:
    text: str
    question_type: str
    difficulty: str
    timestamp: datetime
    screen_region: Tuple[int, int, int, int]
    confidence: float
    source: str = "screen"

class OmniscientVision:
    def __init__(self):
        self.is_active = False
        self.vision_thread = None
        self.question_queue = queue.Queue()
        
        # Advanced OCR configuration
        self.ocr_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,()[]{}:;!?-+=*/<>@#$%^&_|\\"\' '
        
        # Question detection patterns
        self.question_patterns = {
            'dsa': [
                r'given.*array', r'binary.*tree', r'linked.*list', r'time.*complexity',
                r'implement.*algorithm', r'find.*element', r'sort.*array', r'search.*tree',
                r'dynamic.*programming', r'graph.*traversal', r'sliding.*window',
                r'two.*pointer', r'backtrack', r'recursion', r'iteration'
            ],
            'lld': [
                r'design.*pattern', r'class.*diagram', r'object.*oriented',
                r'inheritance', r'polymorphism', r'encapsulation', r'abstraction',
                r'solid.*principle', r'design.*system', r'low.*level.*design'
            ],
            'hld': [
                r'system.*design', r'high.*level.*design', r'architecture',
                r'microservice', r'database.*design', r'scalability', r'load.*balancer',
                r'distributed.*system', r'caching', r'api.*design'
            ],
            'dbms': [
                r'database', r'sql', r'nosql', r'join', r'normalization',
                r'transaction', r'acid', r'index', r'query.*optimization',
                r'relational.*model', r'primary.*key', r'foreign.*key'
            ],
            'oops': [
                r'class', r'object', r'inheritance', r'polymorphism',
                r'encapsulation', r'abstraction', r'constructor', r'destructor',
                r'virtual.*function', r'overloading', r'overriding'
            ],
            'theoretical': [
                r'explain', r'describe', r'what.*is', r'difference.*between',
                r'advantages', r'disadvantages', r'pros.*cons', r'compare'
            ]
        }
        
        # Platform-specific screen regions
        self.common_regions = {
            'leetcode': (200, 150, 1200, 800),
            'geeksforgeeks': (150, 200, 1300, 900),
            'hackerrank': (200, 180, 1250, 850),
            'codechef': (180, 160, 1280, 820),
            'codeforces': (160, 140, 1320, 880),
            'fullscreen': (0, 0, 1920, 1080)
        }
        
        # Advanced image preprocessing
        self.preprocessing_enabled = True
        self.adaptive_thresholding = True
        self.noise_reduction = True
        
        print("🔮 OMNISCIENT VISION SYSTEM INITIALIZED")
    
    def activate_vision(self):
        """Activate omniscient screen monitoring"""
        if self.is_active:
            return True
            
        print("👁️ ACTIVATING OMNISCIENT VISION...")
        self.is_active = True
        self.vision_thread = threading.Thread(target=self._vision_loop, daemon=True)
        self.vision_thread.start()
        print("✅ OMNISCIENT VISION ACTIVE - SUPERNATURAL PERCEPTION ENABLED")
        return True
    
    def deactivate_vision(self):
        """Deactivate vision system"""
        self.is_active = False
        if self.vision_thread:
            self.vision_thread.join(timeout=2)
        print("👁️ Omniscient vision deactivated")
    
    def _vision_loop(self):
        """Main vision processing loop"""
        print("👁️ Starting omniscient vision loop...")
        
        while self.is_active:
            try:
                # Capture screen with supernatural precision
                screenshot = self._capture_screen_with_precision()
                
                # Analyze multiple regions simultaneously
                detected_questions = self._analyze_multiple_regions(screenshot)
                
                # Process detected questions
                for question in detected_questions:
                    if self._validate_question(question):
                        self.question_queue.put(question)
                        print(f"🔍 QUESTION DETECTED: {question.question_type.upper()} - {question.text[:100]}...")
                
                # Adaptive sleep based on detection activity
                sleep_time = 0.5 if detected_questions else 2.0
                time.sleep(sleep_time)
                
            except Exception as e:
                print(f"⚠️ Vision error: {e}")
                time.sleep(1)
        
        print("👁️ Omniscient vision loop stopped")
    
    def _capture_screen_with_precision(self) -> np.ndarray:
        """Capture screen with supernatural precision"""
        try:
            # High-precision screen capture
            screenshot = ImageGrab.grab()
            screenshot_np = np.array(screenshot)
            
            # Convert to optimal format for OCR
            if len(screenshot_np.shape) == 3:
                screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            
            return screenshot_np
            
        except Exception as e:
            print(f"📸 Screen capture error: {e}")
            return np.zeros((1080, 1920, 3), dtype=np.uint8)
    
    def _analyze_multiple_regions(self, screenshot: np.ndarray) -> List[DetectedQuestion]:
        """Analyze multiple screen regions simultaneously"""
        detected_questions = []
        
        # Analyze common coding platform regions
        for platform, region in self.common_regions.items():
            x1, y1, x2, y2 = region
            
            # Extract region with bounds checking
            h, w = screenshot.shape[:2]
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)
            
            if x2 > x1 and y2 > y1:
                region_img = screenshot[y1:y2, x1:x2]
                
                # Supernatural OCR analysis
                questions = self._extract_questions_from_region(region_img, region, platform)
                detected_questions.extend(questions)
        
        return detected_questions
    
    def _extract_questions_from_region(self, region_img: np.ndarray, 
                                     region: Tuple[int, int, int, int], 
                                     platform: str) -> List[DetectedQuestion]:
        """Extract questions from screen region with supernatural precision"""
        questions = []
        
        try:
            # Advanced image preprocessing
            processed_img = self._preprocess_image_advanced(region_img)
            
            # Multiple OCR attempts with different configurations
            texts = self._multi_ocr_extraction(processed_img)
            
            for text, confidence in texts:
                if len(text.strip()) > 20:  # Filter short text
                    # Classify question type
                    question_type = self._classify_question_type(text)
                    difficulty = self._assess_difficulty(text)
                    
                    if question_type != 'unknown':
                        question = DetectedQuestion(
                            text=text.strip(),
                            question_type=question_type,
                            difficulty=difficulty,
                            timestamp=datetime.now(),
                            screen_region=region,
                            confidence=confidence,
                            source=f"screen_{platform}"
                        )
                        questions.append(question)
        
        except Exception as e:
            print(f"🔍 Region analysis error: {e}")
        
        return questions
    
    def _preprocess_image_advanced(self, img: np.ndarray) -> np.ndarray:
        """Advanced image preprocessing for supernatural OCR accuracy"""
        if not self.preprocessing_enabled:
            return img
        
        try:
            # Convert to grayscale
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                gray = img.copy()
            
            # Noise reduction
            if self.noise_reduction:
                gray = cv2.medianBlur(gray, 3)
                gray = cv2.bilateralFilter(gray, 9, 75, 75)
            
            # Adaptive thresholding for varying lighting
            if self.adaptive_thresholding:
                binary = cv2.adaptiveThreshold(
                    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                    cv2.THRESH_BINARY, 11, 2
                )
            else:
                _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Morphological operations to clean up
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
            binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
            
            # Scale image for better OCR
            scale_factor = 2
            height, width = binary.shape
            binary = cv2.resize(binary, (width * scale_factor, height * scale_factor), 
                              interpolation=cv2.INTER_CUBIC)
            
            return binary
            
        except Exception as e:
            print(f"🖼️ Preprocessing error: {e}")
            return img
    
    def _multi_ocr_extraction(self, img: np.ndarray) -> List[Tuple[str, float]]:
        """Multiple OCR attempts with different configurations"""
        texts = []
        
        # Configuration variations for maximum accuracy
        configs = [
            r'--oem 3 --psm 6',  # Uniform text block
            r'--oem 3 --psm 7',  # Single text line
            r'--oem 3 --psm 8',  # Single word
            r'--oem 3 --psm 11', # Sparse text
            r'--oem 3 --psm 13'  # Raw line, no word segmentation
        ]
        
        for config in configs:
            try:
                # Extract text with confidence
                data = pytesseract.image_to_data(img, config=config, output_type=pytesseract.Output.DICT)
                
                # Combine text with confidence
                text_parts = []
                confidences = []
                
                for i in range(len(data['text'])):
                    if int(data['conf'][i]) > 30:  # Confidence threshold
                        text = data['text'][i].strip()
                        if text:
                            text_parts.append(text)
                            confidences.append(int(data['conf'][i]))
                
                if text_parts:
                    combined_text = ' '.join(text_parts)
                    avg_confidence = sum(confidences) / len(confidences) / 100.0
                    texts.append((combined_text, avg_confidence))
                    
            except Exception as e:
                print(f"📝 OCR config error: {e}")
                continue
        
        # Remove duplicates and return best results
        unique_texts = []
        seen = set()
        
        for text, conf in sorted(texts, key=lambda x: x[1], reverse=True):
            text_normalized = text.lower().strip()
            if text_normalized not in seen and len(text) > 20:
                seen.add(text_normalized)
                unique_texts.append((text, conf))
        
        return unique_texts[:3]  # Top 3 results
    
    def _classify_question_type(self, text: str) -> str:
        """Classify question type using supernatural pattern recognition"""
        text_lower = text.lower()
        
        # Score each category
        scores = {}
        for category, patterns in self.question_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower))
                score += matches
            scores[category] = score
        
        # Return category with highest score
        if scores:
            best_category = max(scores.items(), key=lambda x: x[1])
            if best_category[1] > 0:
                return best_category[0]
        
        return 'unknown'
    
    def _assess_difficulty(self, text: str) -> str:
        """Assess question difficulty using advanced analysis"""
        text_lower = text.lower()
        
        # Difficulty indicators
        easy_indicators = ['basic', 'simple', 'easy', 'beginner', 'introduction']
        medium_indicators = ['medium', 'intermediate', 'moderate', 'standard']
        hard_indicators = ['hard', 'difficult', 'complex', 'advanced', 'expert', 'optimal']
        
        easy_score = sum(1 for indicator in easy_indicators if indicator in text_lower)
        medium_score = sum(1 for indicator in medium_indicators if indicator in text_lower)
        hard_score = sum(1 for indicator in hard_indicators if indicator in text_lower)
        
        # Additional complexity analysis
        if 'time complexity' in text_lower or 'space complexity' in text_lower:
            hard_score += 1
        
        if 'optimize' in text_lower or 'efficient' in text_lower:
            hard_score += 1
        
        if len(text) > 500:  # Long questions tend to be harder
            medium_score += 1
        
        if hard_score > medium_score and hard_score > easy_score:
            return 'hard'
        elif medium_score > easy_score:
            return 'medium'
        else:
            return 'easy'
    
    def _validate_question(self, question: DetectedQuestion) -> bool:
        """Validate detected question with supernatural intelligence"""
        # Basic validation
        if len(question.text) < 30:
            return False
        
        if question.confidence < 0.3:
            return False
        
        # Check for common false positives
        false_positives = [
            'advertisement', 'cookie', 'privacy', 'terms', 'login',
            'register', 'subscribe', 'follow', 'share', 'like'
        ]
        
        text_lower = question.text.lower()
        for fp in false_positives:
            if fp in text_lower:
                return False
        
        # Must contain question-like structure
        question_indicators = ['?', 'find', 'implement', 'design', 'explain', 'what', 'how', 'why']
        has_question_indicator = any(indicator in text_lower for indicator in question_indicators)
        
        return has_question_indicator
    
    def get_detected_question(self) -> Optional[DetectedQuestion]:
        """Get next detected question from queue"""
        try:
            return self.question_queue.get_nowait()
        except queue.Empty:
            return None
    
    def has_questions(self) -> bool:
        """Check if questions are available"""
        return not self.question_queue.empty()
    
    def set_adaptive_region(self, x: int, y: int, width: int, height: int):
        """Set custom adaptive scanning region"""
        self.common_regions['adaptive'] = (x, y, x + width, y + height)
        print(f"📍 Adaptive region set: ({x}, {y}, {width}, {height})")
    
    def enable_preprocessing(self, enable: bool = True):
        """Enable/disable advanced preprocessing"""
        self.preprocessing_enabled = enable
        print(f"🖼️ Advanced preprocessing: {'Enabled' if enable else 'Disabled'}")
    
    def get_vision_stats(self) -> Dict:
        """Get vision system statistics"""
        return {
            'is_active': self.is_active,
            'questions_pending': self.question_queue.qsize(),
            'regions_monitored': len(self.common_regions),
            'preprocessing_enabled': self.preprocessing_enabled
        }

# Example usage
if __name__ == "__main__":
    vision = OmniscientVision()
    vision.activate_vision()
    
    print("🔮 Monitoring screen for questions...")
    
    try:
        while True:
            if vision.has_questions():
                question = vision.get_detected_question()
                print(f"📖 Question: {question.text}")
                print(f"🏷️ Type: {question.question_type}")
                print(f"⭐ Difficulty: {question.difficulty}")
                print("-" * 80)
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        vision.deactivate_vision()
        print("👁️ Vision system stopped")