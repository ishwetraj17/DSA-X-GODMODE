"""
DSA-X GODMODE++: REAL-TIME INTELLIGENCE MODE
Main Real-Time Intelligence Controller

Implemented by Shwet Raj
Classification: OMNISCIENT INTELLIGENCE
Debug checkpoint: Real-time omniscient operation
"""

import asyncio
import threading
import time
import queue
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from screen_analyzer import ScreenAnalyzer
from voice_listener import VoiceListener
from universal_solver import UniversalSolver, QuestionType

@dataclass
class IntelligenceConfig:
    screen_analysis_enabled: bool = True
    voice_listening_enabled: bool = True
    web_search_enabled: bool = True
    auto_solve_enabled: bool = True
    confidence_threshold: float = 0.7
    scan_interval: float = 2.0
    silence_duration: float = 2.0
    whisper_model_size: str = "base"

class RealTimeIntelligenceController:
    def __init__(self, config: IntelligenceConfig = None):
        self.config = config or IntelligenceConfig()
        self.is_running = False
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.screen_analyzer = ScreenAnalyzer() if self.config.screen_analysis_enabled else None
        self.voice_listener = VoiceListener(self.config.whisper_model_size) if self.config.voice_listening_enabled else None
        self.universal_solver = UniversalSolver()
        
        # Question processing
        self.question_queue = queue.Queue()
        self.solution_queue = queue.Queue()
        self.processed_questions = set()  # Avoid duplicate processing
        
        # Threading
        self.controller_thread = None
        self.solver_thread = None
        
        # Statistics
        self.stats = {
            'questions_detected': 0,
            'questions_solved': 0,
            'screen_detections': 0,
            'voice_detections': 0,
            'start_time': None,
            'last_question_time': None
        }
        
        # Callbacks for UI integration
        self.question_detected_callback = None
        self.solution_ready_callback = None
        
    def start_intelligence(self):
        """Start the real-time intelligence system"""
        if self.is_running:
            self.logger.warning("Intelligence system already running")
            return
            
        self.logger.info("🚀 Starting DSA-X GODMODE++ Real-Time Intelligence...")
        
        # Start components
        if self.screen_analyzer:
            self.screen_analyzer.start_analysis()
            self.screen_analyzer.set_scan_interval(self.config.scan_interval)
            self.screen_analyzer.set_confidence_threshold(self.config.confidence_threshold)
            
        if self.voice_listener:
            self.voice_listener.start_listening()
            self.voice_listener.set_silence_duration(self.config.silence_duration)
            self.voice_listener.set_confidence_threshold(self.config.confidence_threshold)
            
        # Start processing threads
        self.is_running = True
        self.controller_thread = threading.Thread(target=self._intelligence_loop, daemon=True)
        self.solver_thread = threading.Thread(target=self._solver_loop, daemon=True)
        
        self.controller_thread.start()
        self.solver_thread.start()
        
        # Initialize stats
        self.stats['start_time'] = datetime.now()
        
        self.logger.info("✅ Real-Time Intelligence System ACTIVE")
        print("""
🔥 DSA-X GODMODE++ REAL-TIME INTELLIGENCE MODE ACTIVE

🔍 Screen Analysis: Continuously scanning for questions
🎤 Voice Listening: Monitoring audio for spoken questions  
🧠 Universal Solver: Ready to solve any technical question
🌐 Web Enhancement: Searching for optimal solutions

Status: OMNISCIENT INTELLIGENCE ENABLED ✨
        """)
        
    def stop_intelligence(self):
        """Stop the real-time intelligence system"""
        if not self.is_running:
            return
            
        self.logger.info("🛑 Stopping Real-Time Intelligence System...")
        
        self.is_running = False
        
        # Stop components
        if self.screen_analyzer:
            self.screen_analyzer.stop_analysis()
            
        if self.voice_listener:
            self.voice_listener.stop_listening()
            
        # Wait for threads to complete
        if self.controller_thread:
            self.controller_thread.join()
        if self.solver_thread:
            self.solver_thread.join()
            
        # Print final statistics
        self._print_final_stats()
        
        self.logger.info("✅ Real-Time Intelligence System stopped")
        
    def _intelligence_loop(self):
        """Main intelligence gathering loop"""
        self.logger.info("🧠 Starting intelligence gathering loop...")
        
        while self.is_running:
            try:
                # Collect questions from screen analyzer
                if self.screen_analyzer:
                    screen_questions = self.screen_analyzer.get_detected_questions()
                    for question_data in screen_questions:
                        self._process_detected_question(question_data, 'screen')
                        self.stats['screen_detections'] += 1
                
                # Collect questions from voice listener
                if self.voice_listener:
                    voice_questions = self.voice_listener.get_detected_questions()
                    for question_data in voice_questions:
                        self._process_detected_question(question_data, 'voice')
                        self.stats['voice_detections'] += 1
                
                # Sleep to prevent excessive CPU usage
                time.sleep(0.5)
                
            except Exception as e:
                self.logger.error(f"Error in intelligence loop: {e}")
                time.sleep(1.0)
                
        self.logger.info("🧠 Intelligence gathering loop stopped")
        
    def _solver_loop(self):
        """Main question solving loop"""
        self.logger.info("💡 Starting question solving loop...")
        
        while self.is_running:
            try:
                # Get question from queue
                question_data = self.question_queue.get(timeout=1.0)
                
                # Solve the question
                solution = self._solve_question(question_data)
                
                # Queue the solution
                self.solution_queue.put({
                    'question_data': question_data,
                    'solution': solution,
                    'timestamp': datetime.now()
                })
                
                # Update statistics
                self.stats['questions_solved'] += 1
                
                # Notify callback if registered
                if self.solution_ready_callback:
                    self.solution_ready_callback(question_data, solution)
                
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"Error in solver loop: {e}")
                
        self.logger.info("💡 Question solving loop stopped")
        
    def _process_detected_question(self, question_data: Dict, source: str):
        """Process a detected question from any source"""
        question_text = question_data.get('text', '').strip()
        
        if not question_text or len(question_text) < 10:
            return
            
        # Avoid duplicate processing
        question_hash = hash(question_text.lower())
        if question_hash in self.processed_questions:
            return
            
        self.processed_questions.add(question_hash)
        
        # Check confidence threshold
        confidence = question_data.get('confidence', 0.0)
        if confidence < self.config.confidence_threshold:
            self.logger.info(f"Question below confidence threshold: {confidence:.2f}")
            return
            
        # Enhance question data
        enhanced_question = {
            **question_data,
            'source': source,
            'detection_time': datetime.now(),
            'processed': False
        }
        
        # Queue for solving if auto-solve is enabled
        if self.config.auto_solve_enabled:
            self.question_queue.put(enhanced_question)
            
        # Update statistics
        self.stats['questions_detected'] += 1
        self.stats['last_question_time'] = datetime.now()
        
        # Log detection
        self.logger.info(f"📋 Question detected from {source}: {question_text[:60]}...")
        
        # Notify callback if registered
        if self.question_detected_callback:
            self.question_detected_callback(enhanced_question)
            
    def _solve_question(self, question_data: Dict) -> Dict[str, Any]:
        """Solve a detected question"""
        question_text = question_data.get('text', '')
        source = question_data.get('source', 'unknown')
        
        self.logger.info(f"🧠 Solving question from {source}: {question_text[:50]}...")
        
        try:
            # Use universal solver
            solution = self.universal_solver.solve_question(question_text)
            
            # Enhance solution with metadata
            solution.update({
                'source': source,
                'original_detection': question_data,
                'solve_time': datetime.now(),
                'solver_version': 'DSA-X GODMODE++ v3.0'
            })
            
            self.logger.info(f"✅ Question solved successfully (confidence: {solution.get('confidence', 0):.2f})")
            return solution
            
        except Exception as e:
            self.logger.error(f"Failed to solve question: {e}")
            return {
                'error': str(e),
                'question': question_text,
                'source': source,
                'timestamp': datetime.now().isoformat()
            }
            
    def get_latest_solution(self) -> Optional[Dict[str, Any]]:
        """Get the most recent solution"""
        try:
            return self.solution_queue.get_nowait()
        except queue.Empty:
            return None
            
    def get_all_solutions(self) -> List[Dict[str, Any]]:
        """Get all available solutions"""
        solutions = []
        while True:
            try:
                solutions.append(self.solution_queue.get_nowait())
            except queue.Empty:
                break
        return solutions
        
    def manually_solve_question(self, question: str) -> Dict[str, Any]:
        """Manually solve a question (for testing or direct input)"""
        question_data = {
            'text': question,
            'source': 'manual',
            'timestamp': datetime.now(),
            'confidence': 1.0,
            'subject': 'MANUAL'
        }
        
        return self._solve_question(question_data)
        
    def set_region_of_interest(self, x: int, y: int, width: int, height: int):
        """Set screen region of interest for focused scanning"""
        if self.screen_analyzer:
            self.screen_analyzer.set_roi(x, y, width, height)
            self.logger.info(f"Screen ROI set to: ({x}, {y}, {width}, {height})")
            
    def clear_region_of_interest(self):
        """Clear screen region of interest"""
        if self.screen_analyzer:
            self.screen_analyzer.clear_roi()
            self.logger.info("Screen ROI cleared")
            
    def update_config(self, **kwargs):
        """Update configuration parameters"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
                self.logger.info(f"Config updated: {key} = {value}")
                
                # Apply changes to components
                if key == 'scan_interval' and self.screen_analyzer:
                    self.screen_analyzer.set_scan_interval(value)
                elif key == 'silence_duration' and self.voice_listener:
                    self.voice_listener.set_silence_duration(value)
                elif key == 'confidence_threshold':
                    if self.screen_analyzer:
                        self.screen_analyzer.set_confidence_threshold(value)
                    if self.voice_listener:
                        self.voice_listener.set_confidence_threshold(value)
                        
    def get_statistics(self) -> Dict[str, Any]:
        """Get current system statistics"""
        if self.stats['start_time']:
            runtime = datetime.now() - self.stats['start_time']
            runtime_seconds = runtime.total_seconds()
        else:
            runtime_seconds = 0
            
        return {
            **self.stats,
            'runtime_seconds': runtime_seconds,
            'questions_per_minute': self.stats['questions_detected'] / max(runtime_seconds / 60, 1),
            'solve_success_rate': self.stats['questions_solved'] / max(self.stats['questions_detected'], 1)
        }
        
    def _print_final_stats(self):
        """Print final statistics when stopping"""
        stats = self.get_statistics()
        
        print(f"""
📊 DSA-X GODMODE++ FINAL STATISTICS

Runtime: {stats['runtime_seconds']:.1f} seconds
Questions Detected: {stats['questions_detected']}
Questions Solved: {stats['questions_solved']}
Screen Detections: {stats['screen_detections']}
Voice Detections: {stats['voice_detections']}
Questions/Minute: {stats['questions_per_minute']:.1f}
Success Rate: {stats['solve_success_rate']:.1%}

Status: OMNISCIENT INTELLIGENCE MISSION COMPLETE ✨
        """)
        
    def register_question_callback(self, callback):
        """Register callback for when questions are detected"""
        self.question_detected_callback = callback
        
    def register_solution_callback(self, callback):
        """Register callback for when solutions are ready"""
        self.solution_ready_callback = callback
        
    def is_intelligence_active(self) -> bool:
        """Check if intelligence system is currently active"""
        return self.is_running

# CLI Interface for standalone operation
def main():
    """Main CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='DSA-X GODMODE++ Real-Time Intelligence')
    parser.add_argument('--no-screen', action='store_true', help='Disable screen analysis')
    parser.add_argument('--no-voice', action='store_true', help='Disable voice listening')
    parser.add_argument('--no-web', action='store_true', help='Disable web search')
    parser.add_argument('--confidence', type=float, default=0.7, help='Confidence threshold')
    parser.add_argument('--scan-interval', type=float, default=2.0, help='Screen scan interval')
    parser.add_argument('--silence-duration', type=float, default=2.0, help='Voice silence duration')
    parser.add_argument('--whisper-model', default='base', help='Whisper model size')
    parser.add_argument('--roi', nargs=4, type=int, metavar=('X', 'Y', 'W', 'H'), help='Screen region of interest')
    
    args = parser.parse_args()
    
    # Create configuration
    config = IntelligenceConfig(
        screen_analysis_enabled=not args.no_screen,
        voice_listening_enabled=not args.no_voice,
        web_search_enabled=not args.no_web,
        confidence_threshold=args.confidence,
        scan_interval=args.scan_interval,
        silence_duration=args.silence_duration,
        whisper_model_size=args.whisper_model
    )
    
    # Create and configure controller
    controller = RealTimeIntelligenceController(config)
    
    # Set ROI if specified
    if args.roi:
        controller.set_region_of_interest(*args.roi)
        
    # Define callbacks for live output
    def on_question_detected(question_data):
        print(f"\n🔍 QUESTION DETECTED ({question_data['source'].upper()})")
        print(f"   Text: {question_data['text']}")
        print(f"   Subject: {question_data.get('subject', 'Unknown')}")
        print(f"   Confidence: {question_data.get('confidence', 0):.2f}")
        print(f"   Time: {question_data['detection_time']}")
        
    def on_solution_ready(question_data, solution):
        print(f"\n💡 SOLUTION READY")
        print(f"   Question: {question_data['text'][:60]}...")
        if 'analysis' in solution:
            analysis = solution['analysis']
            print(f"   Type: {analysis.question_type.value}")
            print(f"   Difficulty: {analysis.difficulty}")
        print(f"   Solutions: {len(solution.get('solutions', {}))}")
        print(f"   Confidence: {solution.get('confidence', 0):.2f}")
        
        # Print solutions
        for sol_name, sol_data in solution.get('solutions', {}).items():
            print(f"\n   {sol_name.upper()} SOLUTION:")
            if hasattr(sol_data, 'explanation'):
                print(f"   {sol_data.explanation}")
            if hasattr(sol_data, 'time_complexity'):
                print(f"   Time: {sol_data.time_complexity}")
            if hasattr(sol_data, 'space_complexity'):
                print(f"   Space: {sol_data.space_complexity}")
    
    # Register callbacks
    controller.register_question_callback(on_question_detected)
    controller.register_solution_callback(on_solution_ready)
    
    try:
        # Start the intelligence system
        controller.start_intelligence()
        
        print("\n🎯 Real-Time Intelligence System is now active!")
        print("   - Monitoring screen for questions")
        print("   - Listening for spoken questions")
        print("   - Auto-solving detected questions")
        print("\nPress Ctrl+C to stop...")
        
        # Keep running until interrupted
        while controller.is_intelligence_active():
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested...")
    finally:
        controller.stop_intelligence()

if __name__ == "__main__":
    main()