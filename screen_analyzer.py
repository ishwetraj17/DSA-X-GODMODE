#!/usr/bin/env python3
"""
DSA-X GODMODE++ Screen Analyzer
Real-time OCR for detecting DSA questions and coding problems
"""

import cv2
import numpy as np
import pytesseract
import threading
import time
import mss
import mss.tools
from PIL import Image
import re
from typing import Optional, Callable
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ScreenAnalyzer:
    def __init__(self, callback: Optional[Callable] = None, region: Optional[tuple] = None):
        """
        Initialize the screen analyzer
        
        Args:
            callback: Function to call when text is detected
            region: (x, y, width, height) region to monitor, None for full screen
        """
        self.callback = callback
        self.region = region
        self.running = False
        self.thread = None
        self.last_text = ""
        self.confidence_threshold = 60
        
        # Configure Tesseract
        try:
            # Set Tesseract path for different OS
            if hasattr(pytesseract, 'get_tesseract_version'):
                logger.info(f"Tesseract version: {pytesseract.get_tesseract_version()}")
        except Exception as e:
            logger.warning(f"Tesseract not found: {e}")
            logger.info("Please install Tesseract: brew install tesseract (macOS) or sudo apt install tesseract-ocr (Ubuntu)")
        
        # DSA question patterns
        self.dsa_patterns = [
            r'leetcode\.com',
            r'geeksforgeeks\.org',
            r'coding\s+problem',
            r'algorithm\s+question',
            r'data\s+structure',
            r'array|linked\s+list|tree|graph|stack|queue|heap',
            r'two\s+pointers|sliding\s+window|dynamic\s+programming',
            r'time\s+complexity|space\s+complexity',
            r'given\s+an?\s+array',
            r'return\s+the\s+.*\s+of',
            r'input:.*output:',
            r'example\s*\d*:',
            r'constraints:',
            r'follow\s+up:'
        ]
        
        # Compile patterns for efficiency
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.dsa_patterns]
    
    def capture_screen(self) -> Optional[np.ndarray]:
        """Capture screen or region"""
        try:
            with mss.mss() as sct:
                if self.region:
                    monitor = {
                        "top": self.region[1],
                        "left": self.region[0],
                        "width": self.region[2],
                        "height": self.region[3]
                    }
                else:
                    monitor = sct.monitors[1]  # Primary monitor
                
                screenshot = sct.grab(monitor)
                img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
                return np.array(img)
        except Exception as e:
            logger.error(f"Screen capture failed: {e}")
            return None
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for better OCR results"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Apply thresholding to get black text on white background
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Apply morphological operations to clean up the image
        kernel = np.ones((1, 1), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        # Scale up for better OCR
        scaled = cv2.resize(cleaned, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        
        return scaled
    
    def extract_text(self, image: np.ndarray) -> str:
        """Extract text from image using OCR"""
        try:
            # Preprocess the image
            processed = self.preprocess_image(image)
            
            # Configure Tesseract for better accuracy
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789\s\n.,;:!?()[]{}-+=<>/\\|&*%$#@_'
            
            # Extract text
            text = pytesseract.image_to_string(processed, config=custom_config)
            
            # Clean up the text
            text = re.sub(r'\s+', ' ', text).strip()
            
            return text
        except Exception as e:
            logger.error(f"OCR failed: {e}")
            return ""
    
    def is_dsa_question(self, text: str) -> bool:
        """Check if the extracted text contains a DSA question"""
        if not text or len(text) < 20:  # Too short to be a meaningful question
            return False
        
        # Check for DSA patterns
        for pattern in self.compiled_patterns:
            if pattern.search(text):
                return True
        
        # Additional heuristics
        lines = text.split('\n')
        if len(lines) >= 3:  # Multiple lines suggest a problem statement
            # Check for common problem statement indicators
            indicators = ['given', 'find', 'return', 'input', 'output', 'example', 'constraint']
            text_lower = text.lower()
            indicator_count = sum(1 for indicator in indicators if indicator in text_lower)
            if indicator_count >= 2:
                return True
        
        return False
    
    def analyze_screen(self):
        """Main analysis loop"""
        logger.info("Starting screen analysis...")
        
        while self.running:
            try:
                # Capture screen
                image = self.capture_screen()
                if image is None:
                    time.sleep(1)
                    continue
                
                # Extract text
                text = self.extract_text(image)
                
                # Check if it's a new DSA question
                if text and text != self.last_text and self.is_dsa_question(text):
                    logger.info("DSA question detected!")
                    logger.info(f"Text: {text[:200]}...")
                    
                    # Call callback if provided
                    if self.callback:
                        self.callback(text, "screen")
                    
                    self.last_text = text
                
                # Sleep to avoid excessive CPU usage
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Analysis error: {e}")
                time.sleep(1)
    
    def start(self):
        """Start the screen analyzer in a separate thread"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.analyze_screen, daemon=True)
            self.thread.start()
            logger.info("Screen analyzer started")
    
    def stop(self):
        """Stop the screen analyzer"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        logger.info("Screen analyzer stopped")
    
    def set_region(self, region: tuple):
        """Set the screen region to monitor (x, y, width, height)"""
        self.region = region
        logger.info(f"Monitoring region set to: {region}")

def test_screen_analyzer():
    """Test function for the screen analyzer"""
    def on_text_detected(text, source):
        print(f"Detected from {source}: {text[:100]}...")
    
    analyzer = ScreenAnalyzer(callback=on_text_detected)
    
    try:
        analyzer.start()
        print("Screen analyzer running. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        analyzer.stop()
        print("Screen analyzer stopped.")

if __name__ == "__main__":
    test_screen_analyzer()