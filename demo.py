#!/usr/bin/env python3
"""
DSA-X GODMODE++ Demo
Showcase the system capabilities with example questions and solutions
"""

import time
import sys
from typing import Dict, List

# Import our modules
try:
    from dsa_godmode import DSAGodMode
    from question_router import QuestionRouter
    from solver_engine import SolverEngine
    from commentator import SolutionCommentator
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install all dependencies: pip install -r requirements.txt")
    sys.exit(1)

def demo_question_routing():
    """Demo question routing capabilities"""
    print("🎯 Question Routing Demo")
    print("=" * 40)
    
    router = QuestionRouter()
    
    demo_questions = [
        {
            'text': "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
            'expected_type': 'dsa'
        },
        {
            'text': "Design a database schema for an e-commerce platform with users, products, and orders.",
            'expected_type': 'dbms'
        },
        {
            'text': "Explain the concept of inheritance in object-oriented programming with examples.",
            'expected_type': 'oop'
        },
        {
            'text': "Design a scalable system to handle millions of users with real-time messaging.",
            'expected_type': 'system_design'
        },
        {
            'text': "What is the time complexity of binary search algorithm?",
            'expected_type': 'dsa'
        }
    ]
    
    for i, question_data in enumerate(demo_questions, 1):
        print(f"\n{i}. Question: {question_data['text'][:80]}...")
        
        routing_info = router.route_question(question_data['text'], "demo")
        priority = router.get_solver_priority(routing_info)
        
        print(f"   Type: {routing_info['question_type']}")
        print(f"   Confidence: {routing_info['confidence']:.2f}")
        print(f"   Priority: {priority}")
        print(f"   Solver: {routing_info['solver_type']}")

def demo_solver_engine():
    """Demo solver engine capabilities"""
    print("\n🔧 Solver Engine Demo")
    print("=" * 40)
    
    engine = SolverEngine()
    
    demo_questions = [
        "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
        "Implement binary search to find a target element in a sorted array.",
        "Explain ACID properties in database transactions.",
        "What is inheritance in object-oriented programming?",
        "Design a scalable system to handle millions of users."
    ]
    
    for i, question in enumerate(demo_questions, 1):
        print(f"\n{i}. Solving: {question[:60]}...")
        
        routing_info = {
            'text': question,
            'solver_type': 'dsa_solver' if 'array' in question.lower() or 'binary' in question.lower() else 'theoretical_solver',
            'confidence': 0.8
        }
        
        start_time = time.time()
        result = engine.solve(routing_info)
        processing_time = time.time() - start_time
        
        if 'solution' in result and 'error' not in result:
            solution = result['solution']
            print(f"   ✅ Solved in {processing_time:.2f}s")
            print(f"   Title: {solution.get('title', 'N/A')}")
            print(f"   Description: {solution.get('description', 'N/A')[:100]}...")
            
            if 'approaches' in solution:
                print(f"   Approaches: {len(solution['approaches'])}")
                for j, approach in enumerate(solution['approaches'], 1):
                    print(f"     {j}. {approach['name']} ({approach.get('complexity', 'N/A')})")
        else:
            print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")

def demo_commentator():
    """Demo commentator capabilities"""
    print("\n💬 Commentator Demo")
    print("=" * 40)
    
    from commentator import CodeCommentator, SolutionCommentator
    
    commentator = CodeCommentator()
    solution_commentator = SolutionCommentator()
    
    # Demo code commenting
    print("\n1. Code Commenting Demo:")
    test_code = '''def twoSum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []'''
    
    print("Original code:")
    print(test_code)
    
    commented_code = commentator.add_line_comments(test_code, 'python')
    print("\nCommented code:")
    print(commented_code)
    
    # Demo algorithm explanation
    print("\n2. Algorithm Explanation Demo:")
    algo_explanation = commentator.explain_algorithm('two_sum')
    print(f"Algorithm: {algo_explanation['name']}")
    print(f"Description: {algo_explanation['description']}")
    
    if 'key_insights' in algo_explanation:
        print("Key Insights:")
        for insight in algo_explanation['key_insights']:
            print(f"  • {insight}")
    
    # Demo complexity explanation
    print("\n3. Complexity Explanation Demo:")
    complexity_info = commentator.explain_complexity('O(n)')
    print(f"Complexity: {complexity_info['name']}")
    print(f"Description: {complexity_info['description']}")
    
    if 'examples' in complexity_info:
        print("Examples:")
        for example in complexity_info['examples']:
            print(f"  • {example}")

def demo_full_system():
    """Demo the complete system"""
    print("\n🚀 Full System Demo")
    print("=" * 40)
    
    # Create system instance
    godmode = DSAGodMode()
    
    # Set up demo callbacks
    def on_question_detected(text, source, routing_info):
        print(f"\n🎯 Demo: Question detected from {source}")
        print(f"   Text: {text[:80]}...")
        print(f"   Type: {routing_info['question_type']}")
    
    def on_solution_ready(solution_result):
        print(f"\n✅ Demo: Solution ready")
        print(f"   Question: {solution_result['question'][:50]}...")
        print(f"   Processing Time: {solution_result['processing_time']:.2f}s")
        
        if 'solution' in solution_result:
            solution = solution_result['solution']
            print(f"   Title: {solution.get('title', 'N/A')}")
    
    def on_error(error, context):
        print(f"\n❌ Demo: Error in {context}: {error}")
    
    godmode.set_callbacks(on_question_detected, on_solution_ready, on_error)
    
    # Demo manual question solving
    print("\n1. Manual Question Solving Demo:")
    demo_questions = [
        "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
        "Explain ACID properties in database transactions.",
        "What is inheritance in object-oriented programming?"
    ]
    
    for i, question in enumerate(demo_questions, 1):
        print(f"\n   Solving question {i}...")
        solution = godmode.solve_question_manually(question)
        
        if solution and 'solution' in solution:
            sol = solution['solution']
            print(f"   ✅ {sol.get('title', 'Solution generated')}")
            
            if 'explanation' in solution:
                print(f"   Explanation: {solution['explanation'][:100]}...")
        else:
            print(f"   ❌ Failed to solve question {i}")
    
    # Demo statistics
    print("\n2. System Statistics Demo:")
    stats = godmode.get_stats()
    print(f"   Questions Processed: {stats['questions_processed']}")
    print(f"   Solutions Generated: {stats['solutions_generated']}")
    print(f"   Processing Time: {stats.get('uptime', 0):.1f}s")

def interactive_demo():
    """Interactive demo where user can ask questions"""
    print("\n🎮 Interactive Demo")
    print("=" * 40)
    print("Ask me any DSA, DBMS, OOP, or System Design question!")
    print("Type 'quit' to exit the demo.")
    
    godmode = DSAGodMode()
    
    while True:
        try:
            question = input("\n🤔 Your question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("👋 Thanks for trying the demo!")
                break
            
            if not question:
                continue
            
            print("🔍 Processing your question...")
            start_time = time.time()
            
            solution = godmode.solve_question_manually(question)
            processing_time = time.time() - start_time
            
            if solution and 'solution' in solution:
                sol = solution['solution']
                print(f"\n✅ Solution ({processing_time:.2f}s):")
                print(f"Title: {sol.get('title', 'N/A')}")
                print(f"Description: {sol.get('description', 'N/A')}")
                
                if 'approaches' in sol:
                    print("\nApproaches:")
                    for i, approach in enumerate(sol['approaches'], 1):
                        print(f"{i}. {approach['name']} ({approach.get('complexity', 'N/A')})")
                        
                        if 'code' in approach and 'python' in approach['code']:
                            print("Python Implementation:")
                            print(approach['code']['python'])
                            break  # Show only first approach for brevity
                
                if 'explanation' in solution:
                    print(f"\nExplanation: {solution['explanation'][:200]}...")
            else:
                print("❌ Sorry, I couldn't solve that question.")
        
        except KeyboardInterrupt:
            print("\n👋 Demo interrupted. Thanks for trying!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main demo function"""
    print("🚀 DSA-X GODMODE++ System Demo")
    print("=" * 50)
    print("This demo showcases the capabilities of the DSA-X GODMODE++ system.")
    print("Choose a demo option:")
    print("1. Question Routing Demo")
    print("2. Solver Engine Demo")
    print("3. Commentator Demo")
    print("4. Full System Demo")
    print("5. Interactive Demo")
    print("6. Run All Demos")
    print("0. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (0-6): ").strip()
            
            if choice == '0':
                print("👋 Thanks for trying the demo!")
                break
            elif choice == '1':
                demo_question_routing()
            elif choice == '2':
                demo_solver_engine()
            elif choice == '3':
                demo_commentator()
            elif choice == '4':
                demo_full_system()
            elif choice == '5':
                interactive_demo()
            elif choice == '6':
                print("\n🎬 Running all demos...")
                demo_question_routing()
                demo_solver_engine()
                demo_commentator()
                demo_full_system()
                print("\n🎉 All demos completed!")
            else:
                print("❌ Invalid choice. Please enter a number between 0 and 6.")
        
        except KeyboardInterrupt:
            print("\n👋 Demo interrupted. Thanks for trying!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()