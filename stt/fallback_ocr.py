#!/usr/bin/env python3
"""
DSA-X GODMODE++: Ultra-Stealth AI Assistant
OCR Screen Capture Fallback System

Implemented by Shwet Raj
Debug checkpoint: Screen region OCR and text extraction
"""

import threading
import time
import queue
import re
import cv2
import numpy as np
import hashlib
from typing import Optional, Callable, List, Tuple, Dict
import platform

# OCR engine imports
try:
    import pytesseract
    import easyocr
    OCR_AVAILABLE = True
except ImportError as e:
    print(f"Warning: OCR libraries not available: {e}")
    OCR_AVAILABLE = False

# Screen capture imports
try:
    import pyautogui
    import PIL.Image
    SCREEN_CAPTURE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Screen capture libraries not available: {e}")
    SCREEN_CAPTURE_AVAILABLE = False

class OCRRegion:
    """Defines a screen region for OCR monitoring."""
    
    def __init__(self, x: int, y: int, width: int, height: int, name: str = ""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name or f"Region_{x}_{y}"
        self.last_hash = ""
        self.last_text = ""
        self.confidence_threshold = 0.6
        
    def get_bounds(self) -> Tuple[int, int, int, int]:
        """Get region bounds as (x, y, width, height)."""
        return (self.x, self.y, self.width, self.height)
    
    def contains_point(self, x: int, y: int) -> bool:
        """Check if point is within this region."""
        return (self.x <= x <= self.x + self.width and 
                self.y <= y <= self.y + self.height)
    
    def __str__(self):
        return f"OCRRegion({self.name}: {self.x},{self.y} {self.width}x{self.height})"

class OCRFallback:
    """
    OCR-based text capture from screen regions.
    Monitors specified screen areas for text changes.
    """
    
    def __init__(self):
        self.is_running = False
        self.monitoring_thread = None
        self.text_queue = queue.Queue()
        self.callback_function = None
        
        # OCR regions to monitor
        self.regions: List[OCRRegion] = []
        self.active_regions: List[OCRRegion] = []
        
        # OCR engines
        self.ocr_engines = []
        self.current_engine = None
        self._initialize_ocr_engines()
        
        # Monitoring settings
        self.check_interval = 2.0  # seconds (OCR is expensive)
        self.confidence_threshold = 0.7
        self.min_text_length = 5
        self.max_text_length = 2000
        
        # Image processing settings
        self.preprocessing_enabled = True
        self.noise_reduction = True
        self.contrast_enhancement = True
        
        # Content filtering
        self.seen_hashes = set()
        self.last_successful_ocr = ""
        
        print("👁️  OCR Fallback system initialized")
    
    def _initialize_ocr_engines(self):
        """Initialize available OCR engines."""
        if not OCR_AVAILABLE:
            print("❌ OCR libraries not available")
            return
        
        # Try to initialize Tesseract
        try:
            pytesseract.get_tesseract_version()
            self.ocr_engines.append('tesseract')
            print("✅ Tesseract OCR available")
        except Exception as e:
            print(f"⚠️  Tesseract not available: {e}")
        
        # Try to initialize EasyOCR
        try:
            # EasyOCR will be initialized on first use to avoid startup delay
            self.ocr_engines.append('easyocr')
            print("✅ EasyOCR available")
        except Exception as e:
            print(f"⚠️  EasyOCR not available: {e}")
        
        # Set default engine
        if self.ocr_engines:
            self.current_engine = self.ocr_engines[0]
            print(f"🎯 Using OCR engine: {self.current_engine}")
        else:
            print("❌ No OCR engines available")
    
    def add_region(self, x: int, y: int, width: int, height: int, name: str = "") -> bool:
        """Add a screen region for OCR monitoring."""
        if not SCREEN_CAPTURE_AVAILABLE:
            print("❌ Screen capture not available")
            return False
        
        # Validate region bounds
        screen_width, screen_height = pyautogui.size()
        if (x < 0 or y < 0 or x + width > screen_width or y + height > screen_height):
            print(f"❌ Invalid region bounds: {x},{y} {width}x{height}")
            return False
        
        region = OCRRegion(x, y, width, height, name)
        self.regions.append(region)
        
        print(f"📍 Added OCR region: {region}")
        return True
    
    def add_auto_regions(self) -> int:
        """Add common screen regions automatically."""
        if not SCREEN_CAPTURE_AVAILABLE:
            return 0
        
        screen_width, screen_height = pyautogui.size()
        added_count = 0
        
        # Common regions for interview platforms
        common_regions = [
            # Video call text areas (center portion)
            (int(screen_width * 0.2), int(screen_height * 0.3), 
             int(screen_width * 0.6), int(screen_height * 0.4), "VideoCall_Center"),
            
            # Chat/question areas (right side)
            (int(screen_width * 0.7), int(screen_height * 0.1), 
             int(screen_width * 0.3), int(screen_height * 0.8), "Chat_Right"),
            
            # Document/code sharing areas (left side)
            (0, int(screen_height * 0.1), 
             int(screen_width * 0.5), int(screen_height * 0.8), "Document_Left"),
            
            # Bottom notification area
            (int(screen_width * 0.1), int(screen_height * 0.8), 
             int(screen_width * 0.8), int(screen_height * 0.2), "Notifications_Bottom")
        ]
        
        for x, y, w, h, name in common_regions:
            if self.add_region(x, y, w, h, name):
                added_count += 1
        
        print(f"📍 Added {added_count} automatic OCR regions")
        return added_count
    
    def start_monitoring(self, callback: Optional[Callable[[str], None]] = None):
        """Start OCR monitoring of registered regions."""
        if not OCR_AVAILABLE or not SCREEN_CAPTURE_AVAILABLE:
            print("❌ OCR or screen capture not available")
            return False
        
        if self.is_running:
            print("⚠️  OCR monitoring already running")
            return True
        
        if not self.regions:
            print("⚠️  No regions configured, adding automatic regions")
            self.add_auto_regions()
        
        if not self.regions:
            print("❌ No OCR regions configured")
            return False
        
        self.callback_function = callback
        self.is_running = True
        self.active_regions = self.regions.copy()
        
        self.monitoring_thread = threading.Thread(target=self._monitor_regions, daemon=True)
        self.monitoring_thread.start()
        
        print(f"👁️  OCR monitoring started for {len(self.active_regions)} regions")
        return True
    
    def stop_monitoring(self):
        """Stop OCR monitoring and clean up resources."""
        if not self.is_running:
            return
        
        self.is_running = False
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=5.0)
        
        # Clear sensitive data
        self.seen_hashes.clear()
        self.last_successful_ocr = ""
        
        print("🛑 OCR monitoring stopped")
    
    def _monitor_regions(self):
        """Main OCR monitoring loop."""
        print("🔄 OCR monitoring loop started")
        
        while self.is_running:
            try:
                for region in self.active_regions:
                    if not self.is_running:
                        break
                    
                    text = self._capture_region_text(region)
                    if text and self._is_new_meaningful_text(text, region):
                        processed_text = self._process_ocr_text(text)
                        
                        if processed_text:
                            print(f"👁️  OCR detected from {region.name}: {processed_text[:50]}...")
                            
                            # Add to queue
                            self.text_queue.put(processed_text)
                            
                            # Call callback
                            if self.callback_function:
                                try:
                                    self.callback_function(processed_text)
                                except Exception as e:
                                    print(f"🚨 OCR callback error: {e}")
                            
                            # Update region tracking
                            region.last_text = text
                            region.last_hash = self._generate_hash(text)
                            self.last_successful_ocr = processed_text
                
                time.sleep(self.check_interval)
                
            except Exception as e:
                print(f"🚨 OCR monitoring error: {e}")
                time.sleep(5.0)  # Longer delay on error
        
        print("🔄 OCR monitoring loop ended")
    
    def _capture_region_text(self, region: OCRRegion) -> Optional[str]:
        """Capture and extract text from a screen region."""
        try:
            # Capture screenshot of region
            screenshot = pyautogui.screenshot(region=(region.x, region.y, region.width, region.height))
            
            # Convert to numpy array for processing
            image = np.array(screenshot)
            
            # Preprocess image if enabled
            if self.preprocessing_enabled:
                image = self._preprocess_image(image)
            
            # Perform OCR
            text = self._extract_text_from_image(image)
            
            return text
            
        except Exception as e:
            print(f"🚨 Region capture error for {region.name}: {e}")
            return None
    
    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image to improve OCR accuracy."""
        try:
            # Convert to grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
            
            # Apply noise reduction
            if self.noise_reduction:
                gray = cv2.medianBlur(gray, 3)
            
            # Enhance contrast
            if self.contrast_enhancement:
                gray = cv2.equalizeHist(gray)
            
            # Apply thresholding to get binary image
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            return binary
            
        except Exception as e:
            print(f"🚨 Image preprocessing error: {e}")
            return image
    
    def _extract_text_from_image(self, image: np.ndarray) -> Optional[str]:
        """Extract text from preprocessed image using OCR."""
        if not self.current_engine:
            return None
        
        try:
            if self.current_engine == 'tesseract':
                return self._tesseract_ocr(image)
            elif self.current_engine == 'easyocr':
                return self._easyocr_ocr(image)
            else:
                return None
                
        except Exception as e:
            print(f"🚨 OCR extraction error: {e}")
            return None
    
    def _tesseract_ocr(self, image: np.ndarray) -> Optional[str]:
        """Extract text using Tesseract OCR."""
        try:
            # Configure Tesseract for better accuracy
            config = '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,?!():;"\'-+=<>[]{}|\\/@#$%^&*~` '
            
            text = pytesseract.image_to_string(image, config=config)
            return text.strip()
            
        except Exception as e:
            print(f"🚨 Tesseract OCR error: {e}")
            return None
    
    def _easyocr_ocr(self, image: np.ndarray) -> Optional[str]:
        """Extract text using EasyOCR."""
        try:
            # Initialize EasyOCR reader (cached after first use)
            if not hasattr(self, '_easyocr_reader'):
                self._easyocr_reader = easyocr.Reader(['en'], gpu=False, verbose=False)
            
            results = self._easyocr_reader.readtext(image, detail=1)
            
            # Extract text with confidence filtering
            text_parts = []
            for (bbox, text, confidence) in results:
                if confidence >= self.confidence_threshold:
                    text_parts.append(text)
            
            return ' '.join(text_parts).strip()
            
        except Exception as e:
            print(f"🚨 EasyOCR error: {e}")
            return None
    
    def _is_new_meaningful_text(self, text: str, region: OCRRegion) -> bool:
        """Check if OCR text is new and meaningful."""
        if not text or len(text.strip()) < self.min_text_length:
            return False
        
        if len(text) > self.max_text_length:
            return False
        
        # Check if text has changed for this region
        text_hash = self._generate_hash(text)
        if text_hash == region.last_hash:
            return False
        
        # Check global duplicate detection
        if text_hash in self.seen_hashes:
            return False
        
        # Check for meaningful content
        if not self._is_meaningful_content(text):
            return False
        
        return True
    
    def _is_meaningful_content(self, text: str) -> bool:
        """Check if text content is meaningful for processing."""
        # Must contain some letters
        if not re.search(r'[a-zA-Z]', text):
            return False
        
        # Filter out common UI elements
        ui_noise = [
            r'^(ok|cancel|yes|no|close|minimize|maximize)$',
            r'^\d+:\d+$',  # Time stamps
            r'^[★☆⭐]+$',  # Star ratings
            r'^[←→↑↓]+$',  # Arrows
            r'^\s*[■□▪▫]+\s*$',  # Bullets
        ]
        
        text_lower = text.lower().strip()
        for pattern in ui_noise:
            if re.match(pattern, text_lower):
                return False
        
        # Look for question indicators
        question_indicators = [
            'how', 'what', 'why', 'where', 'when', 'which', 'who',
            'explain', 'describe', 'implement', 'solve', 'design',
            'algorithm', 'function', 'class', 'method', 'code',
            'complexity', 'optimize', 'interview', 'question'
        ]
        
        for indicator in question_indicators:
            if indicator in text_lower:
                return True
        
        # Check for question marks or substantial content
        if '?' in text or len(text.strip()) > 30:
            return True
        
        return False
    
    def _process_ocr_text(self, text: str) -> str:
        """Clean and process OCR text."""
        if not text:
            return ""
        
        # Remove OCR artifacts and noise
        processed = re.sub(r'[^\w\s\-.,!?;:()\'"\/\\@#$%^&*+=<>{}[\]|~`]', '', text)
        
        # Normalize whitespace
        processed = re.sub(r'\s+', ' ', processed.strip())
        
        # Remove standalone characters (OCR errors)
        words = processed.split()
        filtered_words = []
        for word in words:
            if len(word) > 1 or word.lower() in ['a', 'i']:
                filtered_words.append(word)
        
        result = ' '.join(filtered_words)
        
        # Final validation
        if len(result) < self.min_text_length:
            return ""
        
        return result
    
    def _generate_hash(self, text: str) -> str:
        """Generate hash for text deduplication."""
        return hashlib.md5(text.encode('utf-8')).hexdigest()[:16]
    
    def get_queued_text(self) -> Optional[str]:
        """Get the next OCR text from queue (non-blocking)."""
        try:
            return self.text_queue.get_nowait()
        except queue.Empty:
            return None
    
    def has_queued_text(self) -> bool:
        """Check if there's OCR text waiting in queue."""
        return not self.text_queue.empty()
    
    def clear_queue(self):
        """Clear all queued OCR text."""
        while not self.text_queue.empty():
            try:
                self.text_queue.get_nowait()
            except queue.Empty:
                break
    
    def set_ocr_engine(self, engine: str) -> bool:
        """Set the OCR engine to use."""
        if engine in self.ocr_engines:
            self.current_engine = engine
            print(f"🎯 OCR engine set to: {engine}")
            return True
        else:
            print(f"❌ OCR engine '{engine}' not available. Available: {self.ocr_engines}")
            return False
    
    def set_confidence_threshold(self, threshold: float):
        """Set OCR confidence threshold."""
        self.confidence_threshold = max(0.0, min(1.0, threshold))
        for region in self.regions:
            region.confidence_threshold = self.confidence_threshold
    
    def get_status(self) -> Dict:
        """Get current OCR system status."""
        return {
            'is_running': self.is_running,
            'ocr_available': OCR_AVAILABLE,
            'screen_capture_available': SCREEN_CAPTURE_AVAILABLE,
            'current_engine': self.current_engine,
            'available_engines': self.ocr_engines,
            'region_count': len(self.regions),
            'active_regions': len(self.active_regions),
            'queue_size': self.text_queue.qsize(),
            'confidence_threshold': self.confidence_threshold,
            'check_interval': self.check_interval
        }
    
    def clear_regions(self):
        """Clear all OCR regions."""
        self.regions.clear()
        self.active_regions.clear()
        print("🗑️  All OCR regions cleared")


def main():
    """Test the OCR fallback functionality."""
    def text_callback(text: str):
        print(f"🎯 OCR Callback: {text[:100]}...")
    
    ocr = OCRFallback()
    
    if not OCR_AVAILABLE or not SCREEN_CAPTURE_AVAILABLE:
        print("❌ OCR or screen capture not available for testing")
        return
    
    try:
        # Add some test regions
        screen_width, screen_height = pyautogui.size()
        
        # Add center region for testing
        center_x = screen_width // 4
        center_y = screen_height // 4
        center_w = screen_width // 2
        center_h = screen_height // 2
        
        ocr.add_region(center_x, center_y, center_w, center_h, "Test_Center")
        
        # Start monitoring
        print("👁️  Starting OCR test...")
        ocr.start_monitoring(callback=text_callback)
        
        print("📝 Open some text on screen to test OCR...")
        print("🛑 Press Ctrl+C to stop")
        
        while True:
            # Check for queued text
            if ocr.has_queued_text():
                text = ocr.get_queued_text()
                if text:
                    print(f"📥 Queued OCR: {text[:50]}...")
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping OCR test...")
        ocr.stop_monitoring()
    except Exception as e:
        print(f"💥 Test error: {e}")
        ocr.stop_monitoring()


if __name__ == "__main__":
    main()