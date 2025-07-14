#!/usr/bin/env python3
"""
DSA-X GODMODE++ Question Router
Routes questions to appropriate solvers based on classification
"""

import re
import logging
from typing import Dict, List, Optional, Tuple
from enum import Enum
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QuestionType(Enum):
    """Enumeration of question types"""
    DSA = "dsa"
    DBMS = "dbms"
    OOP = "oop"
    HLD = "hld"
    LLD = "lld"
    SYSTEM_DESIGN = "system_design"
    ALGORITHM = "algorithm"
    DATA_STRUCTURE = "data_structure"
    THEORETICAL = "theoretical"
    UNKNOWN = "unknown"

class QuestionRouter:
    def __init__(self):
        """Initialize the question router with classification patterns"""
        
        # DSA patterns
        self.dsa_patterns = [
            r'array|linked\s+list|tree|graph|stack|queue|heap|hash',
            r'two\s+pointers|sliding\s+window|dynamic\s+programming',
            r'backtracking|recursion|divide\s+and\s+conquer',
            r'binary\s+search|linear\s+search|sorting',
            r'time\s+complexity|space\s+complexity|optimization',
            r'leetcode|geeksforgeeks|hackerrank|codeforces',
            r'given\s+an?\s+array|return\s+the\s+.*\s+of',
            r'input:.*output:|example\s*\d*:|constraints:',
            r'maximum|minimum|sum|count|reverse|merge',
            r'palindrome|anagram|substring|subsequence',
            r'path|cycle|connected|component|traversal',
            r'insert|delete|update|search|find'
        ]
        
        # DBMS patterns
        self.dbms_patterns = [
            r'database|sql|mysql|postgresql|oracle|mongodb',
            r'normalization|denormalization|acid|transaction',
            r'index|primary\s+key|foreign\s+key|candidate\s+key',
            r'join|inner\s+join|left\s+join|right\s+join',
            r'group\s+by|having|order\s+by|distinct',
            r'stored\s+procedure|trigger|view|cursor',
            r'deadlock|locking|isolation|consistency',
            r'rdbms|nosql|relational|non\s*relational',
            r'query\s+optimization|execution\s+plan',
            r'data\s+warehouse|data\s+mining|etl'
        ]
        
        # OOP patterns
        self.oop_patterns = [
            r'object\s*oriented|oop|class|object|method',
            r'encapsulation|inheritance|polymorphism|abstraction',
            r'interface|abstract\s+class|virtual|override',
            r'constructor|destructor|getter|setter',
            r'public|private|protected|static|final',
            r'overloading|overriding|binding|late\s+binding',
            r'composition|aggregation|association',
            r'design\s+pattern|singleton|factory|observer',
            r'java|c\+\+|python|javascript|typescript',
            r'instance|reference|pointer|memory\s+management'
        ]
        
        # System Design patterns
        self.system_design_patterns = [
            r'system\s+design|high\s+level\s+design|hld',
            r'low\s+level\s+design|lld|microservices',
            r'scalability|load\s+balancing|caching',
            r'distributed\s+system|distributed\s+computing',
            r'consistency|availability|partition\s+tolerance|cap',
            r'latency|throughput|bandwidth|qps',
            r'horizontal\s+scaling|vertical\s+scaling',
            r'database\s+sharding|replication|backup',
            r'api\s+design|rest|graphql|soap',
            r'message\s+queue|kafka|rabbitmq|redis',
            r'cdn|load\s+balancer|reverse\s+proxy',
            r'monitoring|logging|alerting|metrics'
        ]
        
        # Compile all patterns for efficiency
        self.compiled_patterns = {
            QuestionType.DSA: [re.compile(pattern, re.IGNORECASE) for pattern in self.dsa_patterns],
            QuestionType.DBMS: [re.compile(pattern, re.IGNORECASE) for pattern in self.dbms_patterns],
            QuestionType.OOP: [re.compile(pattern, re.IGNORECASE) for pattern in self.oop_patterns],
            QuestionType.SYSTEM_DESIGN: [re.compile(pattern, re.IGNORECASE) for pattern in self.system_design_patterns]
        }
        
        # Question type keywords for additional classification
        self.type_keywords = {
            QuestionType.DSA: [
                'algorithm', 'data structure', 'coding', 'programming',
                'leetcode', 'geeksforgeeks', 'hackerrank', 'codeforces',
                'array', 'linked list', 'tree', 'graph', 'stack', 'queue',
                'sort', 'search', 'optimize', 'complexity'
            ],
            QuestionType.DBMS: [
                'database', 'sql', 'mysql', 'postgresql', 'oracle',
                'normalization', 'transaction', 'index', 'join',
                'query', 'rdbms', 'nosql', 'acid'
            ],
            QuestionType.OOP: [
                'object oriented', 'class', 'object', 'method',
                'inheritance', 'polymorphism', 'encapsulation',
                'interface', 'design pattern', 'java', 'c++'
            ],
            QuestionType.SYSTEM_DESIGN: [
                'system design', 'scalability', 'distributed',
                'microservices', 'load balancing', 'caching',
                'api design', 'architecture', 'high level'
            ]
        }
    
    def classify_question(self, text: str) -> Tuple[QuestionType, float]:
        """
        Classify the question type and return confidence score
        
        Args:
            text: The question text to classify
            
        Returns:
            Tuple of (QuestionType, confidence_score)
        """
        if not text or len(text.strip()) < 10:
            return QuestionType.UNKNOWN, 0.0
        
        text_lower = text.lower()
        scores = {}
        
        # Calculate pattern-based scores
        for question_type, patterns in self.compiled_patterns.items():
            score = 0
            for pattern in patterns:
                if pattern.search(text):
                    score += 1
            scores[question_type] = score
        
        # Calculate keyword-based scores
        for question_type, keywords in self.type_keywords.items():
            keyword_score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    keyword_score += 1
            scores[question_type] = scores.get(question_type, 0) + keyword_score * 0.5
        
        # Find the best match
        if not scores:
            return QuestionType.UNKNOWN, 0.0
        
        best_type = max(scores.keys(), key=lambda k: scores[k])
        best_score = scores[best_type]
        
        # Normalize confidence score (0-1)
        total_patterns = len(self.dsa_patterns) + len(self.dbms_patterns) + len(self.oop_patterns) + len(self.system_design_patterns)
        confidence = min(best_score / total_patterns, 1.0)
        
        # Set minimum threshold
        if confidence < 0.1:
            return QuestionType.UNKNOWN, confidence
        
        logger.info(f"Question classified as {best_type.value} with confidence {confidence:.2f}")
        return best_type, confidence
    
    def extract_question_details(self, text: str) -> Dict:
        """
        Extract detailed information from the question
        
        Args:
            text: The question text
            
        Returns:
            Dictionary containing extracted details
        """
        details = {
            'original_text': text,
            'question_type': QuestionType.UNKNOWN,
            'confidence': 0.0,
            'keywords': [],
            'constraints': [],
            'examples': [],
            'complexity_requirements': []
        }
        
        # Classify the question
        question_type, confidence = self.classify_question(text)
        details['question_type'] = question_type
        details['confidence'] = confidence
        
        # Extract keywords
        text_lower = text.lower()
        all_keywords = []
        for keywords in self.type_keywords.values():
            all_keywords.extend(keywords)
        
        found_keywords = [keyword for keyword in all_keywords if keyword in text_lower]
        details['keywords'] = list(set(found_keywords))
        
        # Extract constraints
        constraint_patterns = [
            r'constraints?:.*?(?=\n|$)',
            r'1\s*<=\s*n\s*<=\s*\d+',
            r'time\s+complexity.*?(?=\n|$)',
            r'space\s+complexity.*?(?=\n|$)'
        ]
        
        for pattern in constraint_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            details['constraints'].extend(matches)
        
        # Extract examples
        example_patterns = [
            r'example\s*\d*:.*?(?=\n|$)',
            r'input:.*?output:',
            r'sample\s+input.*?sample\s+output'
        ]
        
        for pattern in example_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            details['examples'].extend(matches)
        
        # Extract complexity requirements
        complexity_patterns = [
            r'O\([^)]+\)',
            r'time\s+complexity.*?O\([^)]+\)',
            r'space\s+complexity.*?O\([^)]+\)'
        ]
        
        for pattern in complexity_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            details['complexity_requirements'].extend(matches)
        
        return details
    
    def route_question(self, text: str, source: str = "unknown") -> Dict:
        """
        Route a question to the appropriate solver
        
        Args:
            text: The question text
            source: Source of the question (screen, voice, etc.)
            
        Returns:
            Dictionary containing routing information
        """
        logger.info(f"Routing question from {source}: {text[:100]}...")
        
        # Extract question details
        details = self.extract_question_details(text)
        
        # Determine solver type based on question type
        solver_mapping = {
            QuestionType.DSA: "dsa_solver",
            QuestionType.ALGORITHM: "dsa_solver",
            QuestionType.DATA_STRUCTURE: "dsa_solver",
            QuestionType.DBMS: "theoretical_solver",
            QuestionType.OOP: "theoretical_solver",
            QuestionType.SYSTEM_DESIGN: "theoretical_solver",
            QuestionType.HLD: "theoretical_solver",
            QuestionType.LLD: "theoretical_solver",
            QuestionType.THEORETICAL: "theoretical_solver",
            QuestionType.UNKNOWN: "general_solver"
        }
        
        solver_type = solver_mapping.get(details['question_type'], "general_solver")
        
        routing_info = {
            'text': text,
            'source': source,
            'question_type': details['question_type'].value,
            'confidence': details['confidence'],
            'solver_type': solver_type,
            'details': details,
            'timestamp': time.time()
        }
        
        logger.info(f"Question routed to {solver_type} solver")
        return routing_info
    
    def get_solver_priority(self, routing_info: Dict) -> int:
        """
        Get priority for solver execution
        
        Args:
            routing_info: Routing information dictionary
            
        Returns:
            Priority score (higher = more important)
        """
        priority = 0
        
        # Base priority by question type
        type_priorities = {
            QuestionType.DSA.value: 10,
            QuestionType.ALGORITHM.value: 9,
            QuestionType.DATA_STRUCTURE.value: 8,
            QuestionType.SYSTEM_DESIGN.value: 7,
            QuestionType.DBMS.value: 6,
            QuestionType.OOP.value: 5,
            QuestionType.THEORETICAL.value: 4,
            QuestionType.UNKNOWN.value: 1
        }
        
        priority += type_priorities.get(routing_info['question_type'], 1)
        
        # Boost priority based on confidence
        priority += int(routing_info['confidence'] * 10)
        
        # Boost priority for voice input (real-time)
        if routing_info['source'] == 'voice':
            priority += 5
        
        return priority

def test_question_router():
    """Test function for the question router"""
    router = QuestionRouter()
    
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
    
    for question in test_questions:
        print(f"\nQuestion: {question[:80]}...")
        routing_info = router.route_question(question, "test")
        print(f"Type: {routing_info['question_type']}")
        print(f"Confidence: {routing_info['confidence']:.2f}")
        print(f"Solver: {routing_info['solver_type']}")
        print(f"Priority: {router.get_solver_priority(routing_info)}")

if __name__ == "__main__":
    test_question_router()