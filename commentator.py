#!/usr/bin/env python3
"""
DSA-X GODMODE++ Commentator
Provides detailed explanations and commentary for code solutions
"""

import re
import logging
from typing import Dict, List, Optional, Tuple
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CodeCommentator:
    """Provides detailed code commentary and explanations"""
    
    def __init__(self):
        """Initialize the code commentator"""
        self.comment_templates = {
            'python': {
                'function': '# Function: {name}\n# Purpose: {purpose}\n# Parameters: {params}\n# Returns: {returns}\n',
                'line': '# {explanation}\n',
                'block': '"""\n{explanation}\n"""\n',
                'variable': '# {name}: {explanation}\n'
            },
            'java': {
                'function': '/**\n * Function: {name}\n * Purpose: {purpose}\n * Parameters: {params}\n * Returns: {returns}\n */\n',
                'line': '// {explanation}\n',
                'block': '/*\n{explanation}\n*/\n',
                'variable': '// {name}: {explanation}\n'
            },
            'cpp': {
                'function': '/**\n * Function: {name}\n * Purpose: {purpose}\n * Parameters: {params}\n * Returns: {returns}\n */\n',
                'line': '// {explanation}\n',
                'block': '/*\n{explanation}\n*/\n',
                'variable': '// {name}: {explanation}\n'
            }
        }
        
        # Common code patterns and their explanations
        self.code_patterns = {
            'two_pointers': {
                'pattern': r'left.*right|start.*end|i.*j',
                'explanation': 'Two-pointer technique: Using two pointers to traverse the array efficiently'
            },
            'hash_map': {
                'pattern': r'HashMap|unordered_map|dict|{}',
                'explanation': 'Hash map: Using key-value pairs for O(1) lookups'
            },
            'stack': {
                'pattern': r'Stack|stack|push|pop',
                'explanation': 'Stack: LIFO data structure for managing function calls or parentheses'
            },
            'queue': {
                'pattern': r'Queue|queue|offer|poll',
                'explanation': 'Queue: FIFO data structure for BFS or level-order traversal'
            },
            'recursion': {
                'pattern': r'def.*\(.*\):|public.*\(.*\)|function.*\(.*\)',
                'explanation': 'Recursive function: Function calling itself to solve subproblems'
            },
            'dynamic_programming': {
                'pattern': r'dp\[|memo\[|cache\[',
                'explanation': 'Dynamic programming: Storing results of subproblems to avoid recomputation'
            },
            'binary_search': {
                'pattern': r'left.*<=.*right|start.*<=.*end',
                'explanation': 'Binary search: Dividing search space in half each iteration'
            },
            'sorting': {
                'pattern': r'sort\(|Arrays\.sort|std::sort',
                'explanation': 'Sorting: Arranging elements in ascending or descending order'
            }
        }
    
    def add_line_comments(self, code: str, language: str = 'python') -> str:
        """Add line-by-line comments to code"""
        if language not in self.comment_templates:
            language = 'python'
        
        lines = code.split('\n')
        commented_lines = []
        
        for line in lines:
            stripped_line = line.strip()
            
            if not stripped_line or stripped_line.startswith('#'):
                commented_lines.append(line)
                continue
            
            # Add comments based on code patterns
            comment = self._analyze_line(stripped_line)
            if comment:
                commented_lines.append(f"{self.comment_templates[language]['line'].format(explanation=comment)}")
            
            commented_lines.append(line)
        
        return '\n'.join(commented_lines)
    
    def _analyze_line(self, line: str) -> Optional[str]:
        """Analyze a single line of code and return explanation"""
        line_lower = line.lower()
        
        # Check for variable declarations
        if re.match(r'^\s*(int|long|float|double|String|List|vector|unordered_map|HashMap)\s+\w+', line):
            var_name = re.search(r'(\w+)\s*[=;]', line)
            if var_name:
                return f"Declaring variable {var_name.group(1)}"
        
        # Check for function definitions
        if re.match(r'^\s*(def|public|private|protected|static)\s+\w+\s*\(', line):
            func_name = re.search(r'(def|public|private|protected|static)\s+(\w+)', line)
            if func_name:
                return f"Defining function {func_name.group(2)}"
        
        # Check for loops
        if 'for' in line_lower:
            if 'range' in line_lower:
                return "For loop: Iterating through a range of values"
            elif 'in' in line_lower:
                return "For-each loop: Iterating through collection elements"
            else:
                return "For loop: Traditional C-style iteration"
        
        if 'while' in line_lower:
            return "While loop: Continue until condition becomes false"
        
        # Check for conditionals
        if 'if' in line_lower:
            return "If statement: Conditional execution based on boolean expression"
        
        if 'else' in line_lower:
            return "Else statement: Alternative execution path when condition is false"
        
        # Check for return statements
        if 'return' in line_lower:
            return "Return statement: Exiting function and returning value"
        
        # Check for specific algorithms
        for pattern_name, pattern_info in self.code_patterns.items():
            if re.search(pattern_info['pattern'], line, re.IGNORECASE):
                return pattern_info['explanation']
        
        # Check for mathematical operations
        if any(op in line for op in ['+', '-', '*', '/', '%', '=']):
            if '=' in line and not line.startswith('='):
                return "Assignment: Storing result of calculation in variable"
        
        # Check for method calls
        if re.search(r'\.\w+\s*\(', line):
            return "Method call: Invoking function on object or class"
        
        return None
    
    def add_function_header(self, code: str, function_name: str, purpose: str, 
                          params: str = "", returns: str = "", language: str = 'python') -> str:
        """Add detailed function header comment"""
        if language not in self.comment_templates:
            language = 'python'
        
        header = self.comment_templates[language]['function'].format(
            name=function_name,
            purpose=purpose,
            params=params,
            returns=returns
        )
        
        return header + code
    
    def explain_algorithm(self, algorithm_name: str) -> Dict:
        """Provide detailed explanation of common algorithms"""
        explanations = {
            'two_sum': {
                'name': 'Two Sum Algorithm',
                'description': 'Find two numbers in an array that add up to a target value',
                'approaches': [
                    {
                        'name': 'Brute Force',
                        'complexity': 'O(n²) time, O(1) space',
                        'explanation': [
                            'Use nested loops to check every pair of numbers',
                            'Outer loop selects first number',
                            'Inner loop selects second number',
                            'Check if their sum equals target',
                            'Return indices when found'
                        ]
                    },
                    {
                        'name': 'Hash Map',
                        'complexity': 'O(n) time, O(n) space',
                        'explanation': [
                            'Use hash map to store seen numbers',
                            'For each number, calculate complement (target - num)',
                            'Check if complement exists in hash map',
                            'If found, return current index and complement index',
                            'Store current number and its index in hash map'
                        ]
                    }
                ],
                'key_insights': [
                    'Hash map provides O(1) lookup time',
                    'Single pass through array is sufficient',
                    'Trade-off: space for time complexity'
                ]
            },
            'binary_search': {
                'name': 'Binary Search Algorithm',
                'description': 'Search for target element in sorted array',
                'approaches': [
                    {
                        'name': 'Standard Binary Search',
                        'complexity': 'O(log n) time, O(1) space',
                        'explanation': [
                            'Initialize left and right pointers',
                            'Calculate mid point: (left + right) / 2',
                            'Compare target with element at mid',
                            'If equal, return mid index',
                            'If target < mid, search left half (right = mid - 1)',
                            'If target > mid, search right half (left = mid + 1)',
                            'Continue until left > right'
                        ]
                    }
                ],
                'key_insights': [
                    'Array must be sorted for binary search to work',
                    'Each iteration reduces search space by half',
                    'Logarithmic time complexity due to halving'
                ]
            },
            'linked_list_reverse': {
                'name': 'Linked List Reversal',
                'description': 'Reverse the order of nodes in a linked list',
                'approaches': [
                    {
                        'name': 'Iterative',
                        'complexity': 'O(n) time, O(1) space',
                        'explanation': [
                            'Use three pointers: prev, curr, next_temp',
                            'Initialize prev as null, curr as head',
                            'Store next node: next_temp = curr.next',
                            'Reverse link: curr.next = prev',
                            'Move pointers: prev = curr, curr = next_temp',
                            'Continue until curr becomes null',
                            'Return prev as new head'
                        ]
                    }
                ],
                'key_insights': [
                    'Need to store next node before changing links',
                    'Three pointers prevent loss of references',
                    'In-place reversal with constant space'
                ]
            }
        }
        
        return explanations.get(algorithm_name, {
            'name': algorithm_name,
            'description': 'Algorithm explanation not available',
            'approaches': [],
            'key_insights': []
        })
    
    def explain_data_structure(self, ds_name: str) -> Dict:
        """Provide detailed explanation of data structures"""
        explanations = {
            'array': {
                'name': 'Array Data Structure',
                'description': 'Contiguous memory allocation for elements',
                'operations': {
                    'access': 'O(1) - Direct indexing',
                    'search': 'O(n) - Linear search',
                    'insert': 'O(n) - Shift elements',
                    'delete': 'O(n) - Shift elements'
                },
                'use_cases': [
                    'When size is known and fixed',
                    'Random access is frequent',
                    'Memory efficiency is important'
                ],
                'limitations': [
                    'Fixed size (static arrays)',
                    'Insertion/deletion is expensive',
                    'Memory fragmentation'
                ]
            },
            'linked_list': {
                'name': 'Linked List Data Structure',
                'description': 'Nodes connected by pointers',
                'operations': {
                    'access': 'O(n) - Traverse from head',
                    'search': 'O(n) - Linear search',
                    'insert': 'O(1) - At beginning/end',
                    'delete': 'O(1) - At beginning/end'
                },
                'use_cases': [
                    'Dynamic size requirements',
                    'Frequent insertions/deletions',
                    'Implementing stack/queue'
                ],
                'limitations': [
                    'No random access',
                    'Extra memory for pointers',
                    'Cache unfriendly'
                ]
            },
            'stack': {
                'name': 'Stack Data Structure',
                'description': 'LIFO (Last In, First Out) linear data structure',
                'operations': {
                    'push': 'O(1) - Add to top',
                    'pop': 'O(1) - Remove from top',
                    'peek': 'O(1) - View top element',
                    'isEmpty': 'O(1) - Check if empty'
                },
                'use_cases': [
                    'Function call stack',
                    'Undo operations',
                    'Parentheses matching',
                    'Expression evaluation'
                ],
                'implementation': [
                    'Using arrays',
                    'Using linked lists'
                ]
            },
            'queue': {
                'name': 'Queue Data Structure',
                'description': 'FIFO (First In, First Out) linear data structure',
                'operations': {
                    'enqueue': 'O(1) - Add to rear',
                    'dequeue': 'O(1) - Remove from front',
                    'peek': 'O(1) - View front element',
                    'isEmpty': 'O(1) - Check if empty'
                },
                'use_cases': [
                    'Breadth-first search',
                    'Level-order traversal',
                    'Task scheduling',
                    'Print spooling'
                ],
                'implementation': [
                    'Using arrays (circular)',
                    'Using linked lists'
                ]
            }
        }
        
        return explanations.get(ds_name, {
            'name': ds_name,
            'description': 'Data structure explanation not available',
            'operations': {},
            'use_cases': [],
            'limitations': []
        })
    
    def explain_complexity(self, complexity: str) -> Dict:
        """Explain time and space complexity"""
        explanations = {
            'O(1)': {
                'name': 'Constant Time/Space',
                'description': 'Performance remains constant regardless of input size',
                'examples': [
                    'Array access by index',
                    'Hash map insertion/lookup',
                    'Stack push/pop operations'
                ]
            },
            'O(log n)': {
                'name': 'Logarithmic Time/Space',
                'description': 'Performance grows logarithmically with input size',
                'examples': [
                    'Binary search',
                    'Binary tree operations',
                    'Divide and conquer algorithms'
                ]
            },
            'O(n)': {
                'name': 'Linear Time/Space',
                'description': 'Performance grows linearly with input size',
                'examples': [
                    'Linear search',
                    'Array traversal',
                    'Linked list operations'
                ]
            },
            'O(n log n)': {
                'name': 'Linearithmic Time/Space',
                'description': 'Performance grows as n times log n',
                'examples': [
                    'Merge sort',
                    'Quick sort',
                    'Heap sort'
                ]
            },
            'O(n²)': {
                'name': 'Quadratic Time/Space',
                'description': 'Performance grows quadratically with input size',
                'examples': [
                    'Bubble sort',
                    'Selection sort',
                    'Nested loops'
                ]
            },
            'O(2ⁿ)': {
                'name': 'Exponential Time/Space',
                'description': 'Performance grows exponentially with input size',
                'examples': [
                    'Recursive Fibonacci',
                    'Subset generation',
                    'Tower of Hanoi'
                ]
            }
        }
        
        return explanations.get(complexity, {
            'name': complexity,
            'description': 'Complexity explanation not available',
            'examples': []
        })

class SolutionCommentator:
    """High-level commentator for complete solutions"""
    
    def __init__(self):
        """Initialize the solution commentator"""
        self.code_commentator = CodeCommentator()
    
    def comment_solution(self, solution: Dict) -> Dict:
        """Add comprehensive comments to a solution"""
        commented_solution = solution.copy()
        
        if 'approaches' in solution:
            for approach in commented_solution['approaches']:
                if 'code' in approach:
                    for language, code in approach['code'].items():
                        # Add line comments
                        commented_code = self.code_commentator.add_line_comments(code, language)
                        
                        # Add function header if it's a function
                        if 'def ' in code or 'public ' in code or 'function ' in code:
                            func_name = self._extract_function_name(code)
                            if func_name:
                                commented_code = self.code_commentator.add_function_header(
                                    commented_code,
                                    func_name,
                                    approach.get('name', 'Algorithm implementation'),
                                    language=language
                                )
                        
                        approach['code'][language] = commented_code
        
        return commented_solution
    
    def _extract_function_name(self, code: str) -> Optional[str]:
        """Extract function name from code"""
        patterns = [
            r'def\s+(\w+)\s*\(',
            r'public\s+\w+\s+(\w+)\s*\(',
            r'function\s+(\w+)\s*\('
        ]
        
        for pattern in patterns:
            match = re.search(pattern, code)
            if match:
                return match.group(1)
        
        return None
    
    def generate_explanation(self, solution: Dict) -> str:
        """Generate comprehensive explanation for a solution"""
        explanation_parts = []
        
        if 'title' in solution:
            explanation_parts.append(f"# {solution['title']}")
            explanation_parts.append("")
        
        if 'description' in solution:
            explanation_parts.append(f"## Description")
            explanation_parts.append(solution['description'])
            explanation_parts.append("")
        
        if 'approaches' in solution:
            explanation_parts.append("## Approaches")
            for i, approach in enumerate(solution['approaches'], 1):
                explanation_parts.append(f"### {i}. {approach['name']}")
                
                if 'complexity' in approach:
                    explanation_parts.append(f"**Complexity:** {approach['complexity']}")
                    explanation_parts.append("")
                
                # Add algorithm explanation if available
                algorithm_name = self._identify_algorithm(approach['name'])
                if algorithm_name:
                    algo_explanation = self.code_commentator.explain_algorithm(algorithm_name)
                    if 'key_insights' in algo_explanation:
                        explanation_parts.append("**Key Insights:**")
                        for insight in algo_explanation['key_insights']:
                            explanation_parts.append(f"- {insight}")
                        explanation_parts.append("")
        
        if 'explanation' in solution:
            explanation_parts.append("## Step-by-Step Explanation")
            for step in solution['explanation']:
                explanation_parts.append(f"- {step}")
            explanation_parts.append("")
        
        return '\n'.join(explanation_parts)
    
    def _identify_algorithm(self, approach_name: str) -> Optional[str]:
        """Identify algorithm from approach name"""
        name_lower = approach_name.lower()
        
        if 'two sum' in name_lower or 'hash map' in name_lower:
            return 'two_sum'
        elif 'binary search' in name_lower:
            return 'binary_search'
        elif 'linked list' in name_lower or 'reverse' in name_lower:
            return 'linked_list_reverse'
        
        return None
    
    def add_complexity_explanation(self, complexity: str) -> str:
        """Add detailed complexity explanation"""
        complexity_info = self.code_commentator.explain_complexity(complexity)
        
        explanation = f"## Complexity Analysis: {complexity}\n\n"
        explanation += f"**Type:** {complexity_info['name']}\n\n"
        explanation += f"**Description:** {complexity_info['description']}\n\n"
        
        if 'examples' in complexity_info:
            explanation += "**Examples:**\n"
            for example in complexity_info['examples']:
                explanation += f"- {example}\n"
        
        return explanation

def test_commentator():
    """Test function for the commentator"""
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
    
    print("Original Code:")
    print(test_code)
    print("\nCommented Code:")
    print(commentator.add_line_comments(test_code, 'python'))
    
    # Test algorithm explanation
    print("\n" + "="*50)
    print("Algorithm Explanation:")
    algo_explanation = commentator.explain_algorithm('two_sum')
    print(f"Name: {algo_explanation['name']}")
    print(f"Description: {algo_explanation['description']}")
    
    # Test data structure explanation
    print("\n" + "="*50)
    print("Data Structure Explanation:")
    ds_explanation = commentator.explain_data_structure('hash_map')
    print(f"Name: {ds_explanation['name']}")
    print(f"Description: {ds_explanation['description']}")

if __name__ == "__main__":
    test_commentator()