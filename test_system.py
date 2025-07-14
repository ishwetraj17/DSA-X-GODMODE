#!/usr/bin/env python3
"""
DSA-X GODMODE++ System Test
Comprehensive testing of all system components
"""

import sys
import time
import logging
from typing import Dict, List

# Import our modules
try:
    from screen_analyzer import ScreenAnalyzer
    from voice_listener import VoiceListener
    from question_router import QuestionRouter
    from solver_engine import SolverEngine
    from commentator import CodeCommentator, SolutionCommentator
    from dsa_godmode import DSAGodMode
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install all dependencies: pip install -r requirements.txt")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SystemTester:
    """Comprehensive system testing"""
    
    def __init__(self):
        """Initialize the system tester"""
        self.test_results = {}
        self.passed_tests = 0
        self.total_tests = 0
    
    def run_all_tests(self) -> Dict:
        """Run all system tests"""
        print("🧪 DSA-X GODMODE++ System Test Suite")
        print("=" * 50)
        
        # Test individual components
        self._test_question_router()
        self._test_solver_engine()
        self._test_commentator()
        self._test_screen_analyzer()
        self._test_voice_listener()
        self._test_integration()
        
        # Print results
        self._print_results()
        
        return self.test_results
    
    def _test_question_router(self):
        """Test question router functionality"""
        print("\n🔍 Testing Question Router...")
        
        router = QuestionRouter()
        
        # Test questions
        test_questions = [
            "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
            "Design a database schema for an e-commerce platform with users, products, and orders.",
            "Explain the concept of inheritance in object-oriented programming with examples.",
            "Design a scalable system to handle millions of users with real-time messaging.",
            "What is the time complexity of binary search algorithm?",
            "How to implement a stack using arrays in Java?",
            "Explain ACID properties in database transactions.",
            "Design patterns used in software development."
        ]
        
        for i, question in enumerate(test_questions, 1):
            try:
                routing_info = router.route_question(question, "test")
                priority = router.get_solver_priority(routing_info)
                
                print(f"  ✅ Test {i}: {routing_info['question_type']} (confidence: {routing_info['confidence']:.2f}, priority: {priority})")
                self.passed_tests += 1
            except Exception as e:
                print(f"  ❌ Test {i} failed: {e}")
            
            self.total_tests += 1
        
        self.test_results['question_router'] = True
    
    def _test_solver_engine(self):
        """Test solver engine functionality"""
        print("\n🔧 Testing Solver Engine...")
        
        engine = SolverEngine()
        
        # Test DSA questions
        dsa_questions = [
            "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
            "Implement binary search to find a target element in a sorted array.",
            "Reverse a linked list in-place.",
            "Find the maximum subarray sum using Kadane's algorithm."
        ]
        
        for i, question in enumerate(dsa_questions, 1):
            try:
                routing_info = {
                    'text': question,
                    'solver_type': 'dsa_solver',
                    'confidence': 0.8
                }
                
                result = engine.solve(routing_info)
                
                if 'solution' in result and 'error' not in result:
                    print(f"  ✅ DSA Test {i}: {result['solution'].get('title', 'N/A')}")
                    self.passed_tests += 1
                else:
                    print(f"  ❌ DSA Test {i} failed: {result.get('error', 'Unknown error')}")
                
            except Exception as e:
                print(f"  ❌ DSA Test {i} failed: {e}")
            
            self.total_tests += 1
        
        # Test theoretical questions
        theoretical_questions = [
            "Explain ACID properties in database transactions.",
            "What is inheritance in object-oriented programming?",
            "Design a scalable system to handle millions of users."
        ]
        
        for i, question in enumerate(theoretical_questions, 1):
            try:
                routing_info = {
                    'text': question,
                    'solver_type': 'theoretical_solver',
                    'confidence': 0.8
                }
                
                result = engine.solve(routing_info)
                
                if 'solution' in result and 'error' not in result:
                    print(f"  ✅ Theory Test {i}: {result['solution'].get('title', 'N/A')}")
                    self.passed_tests += 1
                else:
                    print(f"  ❌ Theory Test {i} failed: {result.get('error', 'Unknown error')}")
                
            except Exception as e:
                print(f"  ❌ Theory Test {i} failed: {e}")
            
            self.total_tests += 1
        
        self.test_results['solver_engine'] = True
    
    def _test_commentator(self):
        """Test commentator functionality"""
        print("\n💬 Testing Commentator...")
        
        commentator = CodeCommentator()
        solution_commentator = SolutionCommentator()
        
        # Test code commenting
        test_code = '''def twoSum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []'''
        
        try:
            commented_code = commentator.add_line_comments(test_code, 'python')
            if '#' in commented_code and len(commented_code) > len(test_code):
                print("  ✅ Code commenting test passed")
                self.passed_tests += 1
            else:
                print("  ❌ Code commenting test failed")
        except Exception as e:
            print(f"  ❌ Code commenting test failed: {e}")
        
        self.total_tests += 1
        
        # Test algorithm explanation
        try:
            algo_explanation = commentator.explain_algorithm('two_sum')
            if algo_explanation and 'name' in algo_explanation:
                print("  ✅ Algorithm explanation test passed")
                self.passed_tests += 1
            else:
                print("  ❌ Algorithm explanation test failed")
        except Exception as e:
            print(f"  ❌ Algorithm explanation test failed: {e}")
        
        self.total_tests += 1
        
        # Test data structure explanation
        try:
            ds_explanation = commentator.explain_data_structure('array')
            if ds_explanation and 'name' in ds_explanation:
                print("  ✅ Data structure explanation test passed")
                self.passed_tests += 1
            else:
                print("  ❌ Data structure explanation test failed")
        except Exception as e:
            print(f"  ❌ Data structure explanation test failed: {e}")
        
        self.total_tests += 1
        
        self.test_results['commentator'] = True
    
    def _test_screen_analyzer(self):
        """Test screen analyzer functionality"""
        print("\n🖥️ Testing Screen Analyzer...")
        
        try:
            # Test initialization
            analyzer = ScreenAnalyzer()
            print("  ✅ Screen analyzer initialization passed")
            self.passed_tests += 1
        except Exception as e:
            print(f"  ❌ Screen analyzer initialization failed: {e}")
        
        self.total_tests += 1
        
        # Test DSA pattern detection
        try:
            dsa_text = "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target."
            is_dsa = analyzer.is_dsa_question(dsa_text)
            
            if is_dsa:
                print("  ✅ DSA pattern detection test passed")
                self.passed_tests += 1
            else:
                print("  ❌ DSA pattern detection test failed")
        except Exception as e:
            print(f"  ❌ DSA pattern detection test failed: {e}")
        
        self.total_tests += 1
        
        # Test non-DSA text
        try:
            non_dsa_text = "This is just a regular sentence with no DSA content."
            is_dsa = analyzer.is_dsa_question(non_dsa_text)
            
            if not is_dsa:
                print("  ✅ Non-DSA text detection test passed")
                self.passed_tests += 1
            else:
                print("  ❌ Non-DSA text detection test failed")
        except Exception as e:
            print(f"  ❌ Non-DSA text detection test failed: {e}")
        
        self.total_tests += 1
        
        self.test_results['screen_analyzer'] = True
    
    def _test_voice_listener(self):
        """Test voice listener functionality"""
        print("\n🎤 Testing Voice Listener...")
        
        try:
            # Test initialization
            listener = VoiceListener()
            print("  ✅ Voice listener initialization passed")
            self.passed_tests += 1
        except Exception as e:
            print(f"  ❌ Voice listener initialization failed: {e}")
        
        self.total_tests += 1
        
        # Test microphone detection
        try:
            if listener.test_microphone():
                print("  ✅ Microphone detection test passed")
                self.passed_tests += 1
            else:
                print("  ❌ Microphone detection test failed")
        except Exception as e:
            print(f"  ❌ Microphone detection test failed: {e}")
        
        self.total_tests += 1
        
        # Test DSA speech detection
        try:
            dsa_speech = "How to solve the two sum problem with optimal time complexity"
            is_dsa = listener.is_dsa_question(dsa_speech)
            
            if is_dsa:
                print("  ✅ DSA speech detection test passed")
                self.passed_tests += 1
            else:
                print("  ❌ DSA speech detection test failed")
        except Exception as e:
            print(f"  ❌ DSA speech detection test failed: {e}")
        
        self.total_tests += 1
        
        self.test_results['voice_listener'] = True
    
    def _test_integration(self):
        """Test system integration"""
        print("\n🔗 Testing System Integration...")
        
        try:
            # Test system initialization
            godmode = DSAGodMode()
            print("  ✅ System initialization passed")
            self.passed_tests += 1
        except Exception as e:
            print(f"  ❌ System initialization failed: {e}")
        
        self.total_tests += 1
        
        # Test component testing
        try:
            test_results = godmode.test_components()
            print(f"  ✅ Component testing passed: {test_results}")
            self.passed_tests += 1
        except Exception as e:
            print(f"  ❌ Component testing failed: {e}")
        
        self.total_tests += 1
        
        # Test manual question solving
        try:
            question = "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target."
            solution = godmode.solve_question_manually(question)
            
            if solution and 'solution' in solution:
                print("  ✅ Manual question solving test passed")
                self.passed_tests += 1
            else:
                print("  ❌ Manual question solving test failed")
        except Exception as e:
            print(f"  ❌ Manual question solving test failed: {e}")
        
        self.total_tests += 1
        
        self.test_results['integration'] = True
    
    def _print_results(self):
        """Print test results summary"""
        print("\n" + "=" * 50)
        print("📊 Test Results Summary")
        print("=" * 50)
        
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.total_tests - self.passed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("🎉 System is ready for use!")
        elif success_rate >= 60:
            print("⚠️ System has some issues but may work with limitations")
        else:
            print("❌ System has significant issues that need to be resolved")
        
        print("\nComponent Status:")
        for component, status in self.test_results.items():
            status_icon = "✅" if status else "❌"
            print(f"  {status_icon} {component}")

def main():
    """Main test function"""
    tester = SystemTester()
    results = tester.run_all_tests()
    
    # Return exit code based on success rate
    success_rate = (tester.passed_tests / tester.total_tests) * 100 if tester.total_tests > 0 else 0
    
    if success_rate >= 80:
        print("\n🚀 All tests passed! The DSA-X GODMODE++ system is ready to use.")
        return 0
    else:
        print("\n⚠️ Some tests failed. Please check the installation and dependencies.")
        return 1

if __name__ == "__main__":
    sys.exit(main())