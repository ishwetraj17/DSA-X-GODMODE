#!/usr/bin/env python3
"""
DSA-X GODMODE++: Ultra-Stealth AI Assistant
Clipboard Monitoring Fallback System

Implemented by Shwet Raj
Debug checkpoint: Clipboard text capture and processing
"""

import threading
import time
import queue
import re
import hashlib
from typing import Optional, Callable, Set
import platform

# Platform-specific clipboard imports
try:
    if platform.system() == "Windows":
        import win32clipboard
        import win32con
    elif platform.system() == "Darwin":  # macOS
        import subprocess
    else:  # Linux
        import subprocess
except ImportError as e:
    print(f"Warning: Platform-specific clipboard module not available: {e}")

class ClipboardMonitor:
    """
    Monitors clipboard for text changes and triggers processing
    when meaningful content is detected.
    """
    
    def __init__(self):
        self.is_running = False
        self.monitoring_thread = None
        self.text_queue = queue.Queue()
        self.callback_function = None
        
        # Content filtering
        self.seen_hashes: Set[str] = set()
        self.last_content = ""
        self.min_length = 10
        self.max_length = 5000
        
        # Monitoring settings
        self.check_interval = 0.5  # seconds
        self.duplicate_timeout = 30  # seconds
        
        # Content patterns to filter out noise
        self.noise_patterns = [
            r'^https?://',  # URLs
            r'^\w+@\w+\.\w+',  # Email addresses
            r'^\d+$',  # Pure numbers
            r'^[A-Z0-9]{8,}$',  # IDs/tokens
            r'^\s*$',  # Whitespace only
        ]
        
        print("📋 Clipboard Monitor initialized")
    
    def start_monitoring(self, callback: Optional[Callable[[str], None]] = None):
        """
        Start clipboard monitoring in a separate thread.
        
        Args:
            callback: Function to call when new text is detected
        """
        if self.is_running:
            print("⚠️  Clipboard monitoring already running")
            return
        
        self.callback_function = callback
        self.is_running = True
        self.monitoring_thread = threading.Thread(target=self._monitor_clipboard, daemon=True)
        self.monitoring_thread.start()
        
        print("🎯 Clipboard monitoring started")
    
    def stop_monitoring(self):
        """Stop clipboard monitoring and clean up resources."""
        if not self.is_running:
            return
        
        self.is_running = False
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=2.0)
        
        # Clear sensitive data
        self.seen_hashes.clear()
        self.last_content = ""
        
        print("🛑 Clipboard monitoring stopped")
    
    def _monitor_clipboard(self):
        """Main monitoring loop that runs in separate thread."""
        print("🔄 Clipboard monitoring loop started")
        
        while self.is_running:
            try:
                current_content = self._get_clipboard_text()
                
                if current_content and self._is_valid_content(current_content):
                    if self._is_new_content(current_content):
                        processed_text = self._process_text(current_content)
                        
                        if processed_text:
                            print(f"📝 New clipboard content detected: {processed_text[:50]}...")
                            
                            # Add to queue
                            self.text_queue.put(processed_text)
                            
                            # Call callback if provided
                            if self.callback_function:
                                try:
                                    self.callback_function(processed_text)
                                except Exception as callback_error:
                                    print(f"🚨 Callback error: {callback_error}")
                            
                            # Update tracking
                            self.last_content = current_content
                            content_hash = self._generate_hash(current_content)
                            self.seen_hashes.add(content_hash)
                
                time.sleep(self.check_interval)
                
            except Exception as e:
                print(f"🚨 Clipboard monitoring error: {e}")
                time.sleep(1.0)  # Longer delay on error
        
        print("🔄 Clipboard monitoring loop ended")
    
    def _get_clipboard_text(self) -> Optional[str]:
        """Get current clipboard text content."""
        try:
            if platform.system() == "Windows":
                return self._get_clipboard_windows()
            elif platform.system() == "Darwin":
                return self._get_clipboard_macos()
            else:
                return self._get_clipboard_linux()
        except Exception as e:
            # Clipboard access can fail frequently, so don't spam errors
            return None
    
    def _get_clipboard_windows(self) -> Optional[str]:
        """Get clipboard content on Windows."""
        try:
            win32clipboard.OpenClipboard()
            if win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
                data = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
                win32clipboard.CloseClipboard()
                return data
            win32clipboard.CloseClipboard()
        except Exception:
            try:
                win32clipboard.CloseClipboard()
            except:
                pass
        return None
    
    def _get_clipboard_macos(self) -> Optional[str]:
        """Get clipboard content on macOS."""
        try:
            result = subprocess.run(['pbpaste'], capture_output=True, text=True, timeout=1.0)
            if result.returncode == 0:
                return result.stdout
        except Exception:
            pass
        return None
    
    def _get_clipboard_linux(self) -> Optional[str]:
        """Get clipboard content on Linux."""
        try:
            # Try xclip first
            result = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], 
                                  capture_output=True, text=True, timeout=1.0)
            if result.returncode == 0:
                return result.stdout
        except Exception:
            try:
                # Fallback to xsel
                result = subprocess.run(['xsel', '--clipboard', '--output'], 
                                      capture_output=True, text=True, timeout=1.0)
                if result.returncode == 0:
                    return result.stdout
            except Exception:
                pass
        return None
    
    def _is_valid_content(self, content: str) -> bool:
        """Check if content meets filtering criteria."""
        if not content or len(content.strip()) < self.min_length:
            return False
        
        if len(content) > self.max_length:
            return False
        
        # Check noise patterns
        content_cleaned = content.strip()
        for pattern in self.noise_patterns:
            if re.match(pattern, content_cleaned, re.IGNORECASE):
                return False
        
        # Must contain some alphabetic characters (not just numbers/symbols)
        if not re.search(r'[a-zA-Z]', content):
            return False
        
        # Check for technical question keywords
        technical_indicators = [
            'algorithm', 'function', 'class', 'implement', 'solve', 'design',
            'optimize', 'complexity', 'data structure', 'system', 'database',
            'network', 'how', 'what', 'why', 'explain', 'write', 'code',
            'example', 'difference', 'between', 'interview', 'question'
        ]
        
        content_lower = content.lower()
        for indicator in technical_indicators:
            if indicator in content_lower:
                return True
        
        # If no technical indicators but looks like a question
        if '?' in content or content.strip().endswith('?'):
            return True
        
        # If it's a substantial text (likely a question or prompt)
        if len(content.strip()) > 30 and ' ' in content.strip():
            return True
        
        return False
    
    def _is_new_content(self, content: str) -> bool:
        """Check if content is new and hasn't been seen recently."""
        if content == self.last_content:
            return False
        
        content_hash = self._generate_hash(content)
        if content_hash in self.seen_hashes:
            return False
        
        # Clean old hashes periodically
        if len(self.seen_hashes) > 100:
            # Keep only recent hashes (simplified approach)
            self.seen_hashes = set(list(self.seen_hashes)[-50:])
        
        return True
    
    def _process_text(self, text: str) -> str:
        """Clean and normalize text for processing."""
        if not text:
            return ""
        
        # Remove excessive whitespace
        processed = re.sub(r'\s+', ' ', text.strip())
        
        # Remove common artifacts
        processed = re.sub(r'\ufeff', '', processed)  # BOM
        processed = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', processed)  # Control chars
        
        # Normalize quotes
        processed = re.sub(r'["""]', '"', processed)
        processed = re.sub(r'[''']', "'", processed)
        
        # Remove email signatures and common noise
        lines = processed.split('\n')
        filtered_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not self._is_noise_line(line):
                filtered_lines.append(line)
        
        result = ' '.join(filtered_lines)
        
        # Final length check
        if len(result) < self.min_length:
            return ""
        
        return result
    
    def _is_noise_line(self, line: str) -> bool:
        """Check if a line should be filtered out as noise."""
        noise_patterns = [
            r'^sent from my',
            r'^get outlook for',
            r'^this email was sent',
            r'^confidential',
            r'^disclaimer:',
            r'^unsubscribe',
            r'^\[.*\]$',  # [tags]
            r'^>+\s',     # Email quotes
            r'^--+$',     # Separators
        ]
        
        line_lower = line.lower()
        for pattern in noise_patterns:
            if re.match(pattern, line_lower):
                return True
        
        return False
    
    def _generate_hash(self, content: str) -> str:
        """Generate hash for content deduplication."""
        return hashlib.md5(content.encode('utf-8')).hexdigest()[:16]
    
    def get_queued_text(self) -> Optional[str]:
        """Get the next text from the queue (non-blocking)."""
        try:
            return self.text_queue.get_nowait()
        except queue.Empty:
            return None
    
    def has_queued_text(self) -> bool:
        """Check if there's text waiting in the queue."""
        return not self.text_queue.empty()
    
    def clear_queue(self):
        """Clear all queued text."""
        while not self.text_queue.empty():
            try:
                self.text_queue.get_nowait()
            except queue.Empty:
                break
    
    def set_text_filters(self, min_length: int = None, max_length: int = None, 
                        check_interval: float = None):
        """Update filtering parameters."""
        if min_length is not None:
            self.min_length = max(1, min_length)
        if max_length is not None:
            self.max_length = max(self.min_length, max_length)
        if check_interval is not None:
            self.check_interval = max(0.1, check_interval)
    
    def get_status(self) -> dict:
        """Get current monitoring status."""
        return {
            'is_running': self.is_running,
            'queue_size': self.text_queue.qsize(),
            'seen_hashes_count': len(self.seen_hashes),
            'last_content_length': len(self.last_content),
            'check_interval': self.check_interval,
            'min_length': self.min_length,
            'max_length': self.max_length
        }


def main():
    """Test the clipboard monitor functionality."""
    def text_callback(text: str):
        print(f"🎯 Callback received: {text[:100]}...")
    
    monitor = ClipboardMonitor()
    
    try:
        # Start monitoring
        monitor.start_monitoring(callback=text_callback)
        
        print("📋 Clipboard monitor test started")
        print("📝 Copy some text to clipboard to test...")
        print("🛑 Press Ctrl+C to stop")
        
        while True:
            # Check for queued text
            if monitor.has_queued_text():
                text = monitor.get_queued_text()
                if text:
                    print(f"📥 Queued text: {text[:50]}...")
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping clipboard monitor...")
        monitor.stop_monitoring()
    except Exception as e:
        print(f"💥 Test error: {e}")
        monitor.stop_monitoring()


if __name__ == "__main__":
    main()