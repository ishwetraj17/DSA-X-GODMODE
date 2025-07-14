#!/usr/bin/env python3
"""
DSA-X GODMODE++ Main Orchestrator
Real-Time Intelligence System for DSA Problem Solving
"""

import threading
import time
import queue
import logging
from typing import Dict, List, Optional, Callable
import signal
import sys

# Import our modules
from screen_analyzer import ScreenAnalyzer
from voice_listener import VoiceListener
from question_router import QuestionRouter
from solver_engine import SolverEngine
from commentator import SolutionCommentator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dsa_godmode.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DSAGodMode:
    """Main orchestrator for DSA-X GODMODE++ system"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the DSA-X GODMODE++ system
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or self._get_default_config()
        self.running = False
        
        # Initialize components
        self.screen_analyzer = None
        self.voice_listener = None
        self.question_router = QuestionRouter()
        self.solver_engine = SolverEngine()
        self.solution_commentator = SolutionCommentator()
        
        # Question queue for processing
        self.question_queue = queue.PriorityQueue()
        self.processed_questions = []
        
        # Threads
        self.threads = []
        
        # Callbacks
        self.on_question_detected = None
        self.on_solution_ready = None
        self.on_error = None
        
        # Statistics
        self.stats = {
            'questions_processed': 0,
            'solutions_generated': 0,
            'screen_detections': 0,
            'voice_detections': 0,
            'start_time': None,
            'errors': 0
        }
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _get_default_config(self) -> Dict:
        """Get default configuration"""
        return {
            'screen_analysis': {
                'enabled': True,
                'region': None,  # None for full screen, or (x, y, width, height)
                'interval': 2.0  # seconds between captures
            },
            'voice_listening': {
                'enabled': True,
                'model_size': 'base',  # tiny, base, small, medium, large
                'silence_duration': 1.0
            },
            'question_processing': {
                'max_queue_size': 100,
                'priority_voice': True,
                'auto_solve': True
            },
            'output': {
                'save_solutions': True,
                'output_dir': 'solutions',
                'format': 'markdown'  # markdown, json, txt
            }
        }
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.stop()
        sys.exit(0)
    
    def set_callbacks(self, on_question_detected: Optional[Callable] = None,
                     on_solution_ready: Optional[Callable] = None,
                     on_error: Optional[Callable] = None):
        """Set callback functions for events"""
        self.on_question_detected = on_question_detected
        self.on_solution_ready = on_solution_ready
        self.on_error = on_error
    
    def _on_text_detected(self, text: str, source: str):
        """Callback for when text is detected from screen or voice"""
        try:
            logger.info(f"Text detected from {source}: {text[:100]}...")
            
            # Route the question
            routing_info = self.question_router.route_question(text, source)
            
            # Calculate priority
            priority = self.question_router.get_solver_priority(routing_info)
            
            # Add to processing queue
            if not self.question_queue.full():
                self.question_queue.put((-priority, routing_info))  # Negative for max heap
                logger.info(f"Question queued with priority {priority}")
                
                # Update statistics
                if source == 'screen':
                    self.stats['screen_detections'] += 1
                elif source == 'voice':
                    self.stats['voice_detections'] += 1
                
                # Call user callback
                if self.on_question_detected:
                    self.on_question_detected(text, source, routing_info)
            else:
                logger.warning("Question queue is full, dropping question")
                
        except Exception as e:
            logger.error(f"Error processing detected text: {e}")
            if self.on_error:
                self.on_error(e, "text_processing")
    
    def _process_questions(self):
        """Process questions from the queue"""
        logger.info("Starting question processing thread")
        
        while self.running:
            try:
                # Get question from queue with timeout
                try:
                    priority, routing_info = self.question_queue.get(timeout=1.0)
                except queue.Empty:
                    continue
                
                # Process the question
                self._solve_question(routing_info)
                
                # Mark task as done
                self.question_queue.task_done()
                
            except Exception as e:
                logger.error(f"Error in question processing: {e}")
                self.stats['errors'] += 1
                if self.on_error:
                    self.on_error(e, "question_processing")
    
    def _solve_question(self, routing_info: Dict):
        """Solve a single question"""
        try:
            logger.info(f"Solving question: {routing_info['text'][:50]}...")
            
            # Solve the question
            solution_result = self.solver_engine.solve(routing_info)
            
            if 'error' in solution_result:
                logger.error(f"Error solving question: {solution_result['error']}")
                return
            
            # Add comments to the solution
            if 'solution' in solution_result:
                commented_solution = self.solution_commentator.comment_solution(
                    solution_result['solution']
                )
                solution_result['commented_solution'] = commented_solution
                
                # Generate explanation
                explanation = self.solution_commentator.generate_explanation(
                    solution_result['solution']
                )
                solution_result['explanation'] = explanation
            
            # Store processed question
            self.processed_questions.append(solution_result)
            
            # Update statistics
            self.stats['questions_processed'] += 1
            self.stats['solutions_generated'] += 1
            
            # Call user callback
            if self.on_solution_ready:
                self.on_solution_ready(solution_result)
            
            logger.info(f"Question solved successfully in {solution_result.get('processing_time', 0):.2f}s")
            
        except Exception as e:
            logger.error(f"Error solving question: {e}")
            self.stats['errors'] += 1
            if self.on_error:
                self.on_error(e, "solving")
    
    def start(self):
        """Start the DSA-X GODMODE++ system"""
        if self.running:
            logger.warning("System is already running")
            return
        
        logger.info("Starting DSA-X GODMODE++ Real-Time Intelligence System")
        self.running = True
        self.stats['start_time'] = time.time()
        
        try:
            # Start screen analyzer if enabled
            if self.config['screen_analysis']['enabled']:
                logger.info("Initializing screen analyzer...")
                self.screen_analyzer = ScreenAnalyzer(
                    callback=self._on_text_detected,
                    region=self.config['screen_analysis']['region']
                )
                self.screen_analyzer.start()
                logger.info("Screen analyzer started")
            
            # Start voice listener if enabled
            if self.config['voice_listening']['enabled']:
                logger.info("Initializing voice listener...")
                self.voice_listener = VoiceListener(
                    callback=self._on_text_detected,
                    model_size=self.config['voice_listening']['model_size']
                )
                self.voice_listener.start()
                logger.info("Voice listener started")
            
            # Start question processing thread
            processing_thread = threading.Thread(
                target=self._process_questions,
                daemon=True,
                name="QuestionProcessor"
            )
            processing_thread.start()
            self.threads.append(processing_thread)
            
            logger.info("DSA-X GODMODE++ system started successfully")
            logger.info("Press Ctrl+C to stop the system")
            
        except Exception as e:
            logger.error(f"Error starting system: {e}")
            self.stop()
            raise
    
    def stop(self):
        """Stop the DSA-X GODMODE++ system"""
        if not self.running:
            return
        
        logger.info("Stopping DSA-X GODMODE++ system...")
        self.running = False
        
        # Stop screen analyzer
        if self.screen_analyzer:
            self.screen_analyzer.stop()
            logger.info("Screen analyzer stopped")
        
        # Stop voice listener
        if self.voice_listener:
            self.voice_listener.stop()
            logger.info("Voice listener stopped")
        
        # Wait for processing thread to finish
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=5.0)
        
        logger.info("DSA-X GODMODE++ system stopped")
    
    def get_stats(self) -> Dict:
        """Get system statistics"""
        stats = self.stats.copy()
        
        if stats['start_time']:
            stats['uptime'] = time.time() - stats['start_time']
        
        stats['queue_size'] = self.question_queue.qsize()
        stats['processed_count'] = len(self.processed_questions)
        
        return stats
    
    def get_recent_solutions(self, count: int = 10) -> List[Dict]:
        """Get recent solutions"""
        return self.processed_questions[-count:]
    
    def solve_question_manually(self, question: str) -> Dict:
        """Manually solve a question"""
        routing_info = self.question_router.route_question(question, "manual")
        self._solve_question(routing_info)
        
        if self.processed_questions:
            return self.processed_questions[-1]
        return {}
    
    def set_screen_region(self, region: tuple):
        """Set the screen region to monitor"""
        if self.screen_analyzer:
            self.screen_analyzer.set_region(region)
            logger.info(f"Screen region set to: {region}")
    
    def test_components(self) -> Dict:
        """Test all system components"""
        test_results = {
            'screen_analyzer': False,
            'voice_listener': False,
            'question_router': True,
            'solver_engine': True,
            'commentator': True
        }
        
        try:
            # Test screen analyzer
            test_analyzer = ScreenAnalyzer()
            test_results['screen_analyzer'] = True
            logger.info("Screen analyzer test passed")
        except Exception as e:
            logger.error(f"Screen analyzer test failed: {e}")
        
        try:
            # Test voice listener
            test_listener = VoiceListener()
            if test_listener.test_microphone():
                test_results['voice_listener'] = True
                logger.info("Voice listener test passed")
            else:
                logger.error("Voice listener test failed")
        except Exception as e:
            logger.error(f"Voice listener test failed: {e}")
        
        return test_results

def demo_callbacks():
    """Demo callback functions"""
    def on_question_detected(text, source, routing_info):
        print(f"\n🎯 Question detected from {source}:")
        print(f"   Text: {text[:100]}...")
        print(f"   Type: {routing_info['question_type']}")
        print(f"   Confidence: {routing_info['confidence']:.2f}")
    
    def on_solution_ready(solution_result):
        print(f"\n✅ Solution ready:")
        print(f"   Question: {solution_result['question'][:50]}...")
        print(f"   Solver: {solution_result['solver_type']}")
        print(f"   Time: {solution_result['processing_time']:.2f}s")
        
        if 'solution' in solution_result:
            solution = solution_result['solution']
            print(f"   Title: {solution.get('title', 'N/A')}")
    
    def on_error(error, context):
        print(f"\n❌ Error in {context}: {error}")
    
    return on_question_detected, on_solution_ready, on_error

def main():
    """Main function to run the DSA-X GODMODE++ system"""
    print("🚀 DSA-X GODMODE++ Real-Time Intelligence System")
    print("=" * 60)
    
    # Create system instance
    godmode = DSAGodMode()
    
    # Test components
    print("\n🔧 Testing system components...")
    test_results = godmode.test_components()
    
    for component, status in test_results.items():
        status_icon = "✅" if status else "❌"
        print(f"   {status_icon} {component}")
    
    # Set up callbacks
    on_question_detected, on_solution_ready, on_error = demo_callbacks()
    godmode.set_callbacks(on_question_detected, on_solution_ready, on_error)
    
    # Start the system
    try:
        godmode.start()
        
        # Keep the main thread alive
        while godmode.running:
            time.sleep(1)
            
            # Print stats every 30 seconds
            if int(time.time()) % 30 == 0:
                stats = godmode.get_stats()
                print(f"\n📊 Stats: {stats['questions_processed']} questions, "
                      f"{stats['solutions_generated']} solutions, "
                      f"{stats['errors']} errors")
    
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down...")
    finally:
        godmode.stop()
        
        # Print final stats
        final_stats = godmode.get_stats()
        print(f"\n📈 Final Stats:")
        print(f"   Questions Processed: {final_stats['questions_processed']}")
        print(f"   Solutions Generated: {final_stats['solutions_generated']}")
        print(f"   Screen Detections: {final_stats['screen_detections']}")
        print(f"   Voice Detections: {final_stats['voice_detections']}")
        print(f"   Errors: {final_stats['errors']}")
        print(f"   Uptime: {final_stats.get('uptime', 0):.1f} seconds")

if __name__ == "__main__":
    main()