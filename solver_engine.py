#!/usr/bin/env python3
"""
DSA-X GODMODE++ Solver Engine
Generates solutions for DSA problems and theoretical questions
"""

import re
import logging
from typing import Dict, List, Optional, Tuple
import time
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DSASolver:
    """Solver for DSA and algorithm problems"""
    
    def __init__(self):
        """Initialize DSA solver with common algorithms and data structures"""
        self.algorithms = {
            'two_sum': self.solve_two_sum,
            'binary_search': self.solve_binary_search,
            'linked_list': self.solve_linked_list,
            'tree_traversal': self.solve_tree_traversal,
            'dynamic_programming': self.solve_dynamic_programming,
            'sorting': self.solve_sorting,
            'graph': self.solve_graph,
            'stack_queue': self.solve_stack_queue,
            'string_manipulation': self.solve_string_manipulation,
            'array_manipulation': self.solve_array_manipulation
        }
    
    def identify_problem_type(self, text: str) -> str:
        """Identify the type of DSA problem"""
        text_lower = text.lower()
        
        if 'two sum' in text_lower or 'add up to target' in text_lower:
            return 'two_sum'
        elif 'binary search' in text_lower or 'sorted array' in text_lower:
            return 'binary_search'
        elif 'linked list' in text_lower or 'node' in text_lower:
            return 'linked_list'
        elif 'tree' in text_lower or 'binary tree' in text_lower:
            return 'tree_traversal'
        elif 'dynamic programming' in text_lower or 'dp' in text_lower:
            return 'dynamic_programming'
        elif 'sort' in text_lower or 'sorting' in text_lower:
            return 'sorting'
        elif 'graph' in text_lower or 'adjacency' in text_lower:
            return 'graph'
        elif 'stack' in text_lower or 'queue' in text_lower:
            return 'stack_queue'
        elif 'string' in text_lower or 'palindrome' in text_lower:
            return 'string_manipulation'
        elif 'array' in text_lower:
            return 'array_manipulation'
        else:
            return 'array_manipulation'  # Default
    
    def solve_two_sum(self, problem_text: str) -> Dict:
        """Solve Two Sum problem"""
        solution = {
            'title': 'Two Sum Solution',
            'description': 'Find two numbers in an array that add up to a target value',
            'approaches': [
                {
                    'name': 'Brute Force',
                    'complexity': 'O(n²) time, O(1) space',
                    'code': {
                        'python': '''def twoSum(nums, target):
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []''',
                        'java': '''public int[] twoSum(int[] nums, int target) {
    for (int i = 0; i < nums.length; i++) {
        for (int j = i + 1; j < nums.length; j++) {
            if (nums[i] + nums[j] == target) {
                return new int[]{i, j};
            }
        }
    }
    return new int[]{};
}''',
                        'cpp': '''vector<int> twoSum(vector<int>& nums, int target) {
    for (int i = 0; i < nums.size(); i++) {
        for (int j = i + 1; j < nums.size(); j++) {
            if (nums[i] + nums[j] == target) {
                return {i, j};
            }
        }
    }
    return {};
}'''
                    }
                },
                {
                    'name': 'Hash Map (Optimized)',
                    'complexity': 'O(n) time, O(n) space',
                    'code': {
                        'python': '''def twoSum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []''',
                        'java': '''public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> map = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (map.containsKey(complement)) {
            return new int[]{map.get(complement), i};
        }
        map.put(nums[i], i);
    }
    return new int[]{};
}''',
                        'cpp': '''vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int, int> map;
    for (int i = 0; i < nums.size(); i++) {
        int complement = target - nums[i];
        if (map.find(complement) != map.end()) {
            return {map[complement], i};
        }
        map[nums[i]] = i;
    }
    return {};
}'''
                    }
                }
            ],
            'explanation': [
                'The brute force approach checks every pair of numbers in the array.',
                'The optimized approach uses a hash map to store seen numbers.',
                'For each number, we check if its complement (target - num) exists in the map.',
                'If found, we return the indices of both numbers.',
                'Time complexity: O(n) for optimized, O(n²) for brute force.',
                'Space complexity: O(n) for optimized, O(1) for brute force.'
            ]
        }
        return solution
    
    def solve_binary_search(self, problem_text: str) -> Dict:
        """Solve Binary Search problem"""
        solution = {
            'title': 'Binary Search Solution',
            'description': 'Search for a target element in a sorted array',
            'approaches': [
                {
                    'name': 'Standard Binary Search',
                    'complexity': 'O(log n) time, O(1) space',
                    'code': {
                        'python': '''def binarySearch(nums, target):
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1''',
                        'java': '''public int binarySearch(int[] nums, int target) {
    int left = 0, right = nums.length - 1;
    
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) {
            return mid;
        } else if (nums[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    
    return -1;
}''',
                        'cpp': '''int binarySearch(vector<int>& nums, int target) {
    int left = 0, right = nums.size() - 1;
    
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) {
            return mid;
        } else if (nums[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    
    return -1;
}'''
                    }
                }
            ],
            'explanation': [
                'Binary search works on sorted arrays only.',
                'We maintain two pointers: left and right.',
                'Calculate mid point and compare with target.',
                'If target is found, return the index.',
                'If target is greater, search right half.',
                'If target is smaller, search left half.',
                'Time complexity: O(log n) as we halve the search space each time.',
                'Space complexity: O(1) as we use constant extra space.'
            ]
        }
        return solution
    
    def solve_linked_list(self, problem_text: str) -> Dict:
        """Solve Linked List problem"""
        solution = {
            'title': 'Linked List Solution',
            'description': 'Common linked list operations and problems',
            'approaches': [
                {
                    'name': 'Reverse Linked List',
                    'complexity': 'O(n) time, O(1) space',
                    'code': {
                        'python': '''class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverseList(head):
    prev = None
    curr = head
    
    while curr:
        next_temp = curr.next
        curr.next = prev
        prev = curr
        curr = next_temp
    
    return prev''',
                        'java': '''public class ListNode {
    int val;
    ListNode next;
    ListNode() {}
    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}

public ListNode reverseList(ListNode head) {
    ListNode prev = null;
    ListNode curr = head;
    
    while (curr != null) {
        ListNode nextTemp = curr.next;
        curr.next = prev;
        prev = curr;
        curr = nextTemp;
    }
    
    return prev;
}''',
                        'cpp': '''struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};

ListNode* reverseList(ListNode* head) {
    ListNode* prev = nullptr;
    ListNode* curr = head;
    
    while (curr != nullptr) {
        ListNode* nextTemp = curr->next;
        curr->next = prev;
        prev = curr;
        curr = nextTemp;
    }
    
    return prev;
}'''
                    }
                }
            ],
            'explanation': [
                'Linked list is a linear data structure with nodes connected by pointers.',
                'Each node contains data and a reference to the next node.',
                'To reverse a linked list, we need to change the direction of pointers.',
                'We use three pointers: prev, curr, and next_temp.',
                'Time complexity: O(n) as we visit each node once.',
                'Space complexity: O(1) as we use constant extra space.'
            ]
        }
        return solution
    
    def solve_tree_traversal(self, problem_text: str) -> Dict:
        """Solve Tree Traversal problem"""
        solution = {
            'title': 'Tree Traversal Solution',
            'description': 'Binary tree traversal algorithms',
            'approaches': [
                {
                    'name': 'Inorder Traversal',
                    'complexity': 'O(n) time, O(h) space',
                    'code': {
                        'python': '''class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inorderTraversal(root):
    result = []
    
    def inorder(node):
        if node:
            inorder(node.left)
            result.append(node.val)
            inorder(node.right)
    
    inorder(root)
    return result''',
                        'java': '''public class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode() {}
    TreeNode(int val) { this.val = val; }
    TreeNode(int val, TreeNode left, TreeNode right) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}

public List<Integer> inorderTraversal(TreeNode root) {
    List<Integer> result = new ArrayList<>();
    inorder(root, result);
    return result;
}

private void inorder(TreeNode node, List<Integer> result) {
    if (node != null) {
        inorder(node.left, result);
        result.add(node.val);
        inorder(node.right, result);
    }
}''',
                        'cpp': '''struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
};

vector<int> inorderTraversal(TreeNode* root) {
    vector<int> result;
    inorder(root, result);
    return result;
}

void inorder(TreeNode* node, vector<int>& result) {
    if (node != nullptr) {
        inorder(node->left, result);
        result.push_back(node->val);
        inorder(node->right, result);
    }
}'''
                    }
                }
            ],
            'explanation': [
                'Tree traversal visits all nodes in a specific order.',
                'Inorder traversal: left subtree → root → right subtree.',
                'Preorder traversal: root → left subtree → right subtree.',
                'Postorder traversal: left subtree → right subtree → root.',
                'Recursive approach is simple and intuitive.',
                'Iterative approach uses stack to simulate recursion.',
                'Time complexity: O(n) as we visit each node once.',
                'Space complexity: O(h) where h is the height of the tree.'
            ]
        }
        return solution
    
    def solve_dynamic_programming(self, problem_text: str) -> Dict:
        """Solve Dynamic Programming problem"""
        solution = {
            'title': 'Dynamic Programming Solution',
            'description': 'Dynamic programming approach for optimization problems',
            'approaches': [
                {
                    'name': 'Fibonacci with DP',
                    'complexity': 'O(n) time, O(1) space',
                    'code': {
                        'python': '''def fib(n):
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b''',
                        'java': '''public int fib(int n) {
    if (n <= 1) {
        return n;
    }
    
    int a = 0, b = 1;
    for (int i = 2; i <= n; i++) {
        int temp = a + b;
        a = b;
        b = temp;
    }
    
    return b;
}''',
                        'cpp': '''int fib(int n) {
    if (n <= 1) {
        return n;
    }
    
    int a = 0, b = 1;
    for (int i = 2; i <= n; i++) {
        int temp = a + b;
        a = b;
        b = temp;
    }
    
    return b;
}'''
                    }
                }
            ],
            'explanation': [
                'Dynamic programming solves complex problems by breaking them into simpler subproblems.',
                'We store the results of subproblems to avoid redundant calculations.',
                'Bottom-up approach builds solution from base cases.',
                'Top-down approach uses recursion with memoization.',
                'Key steps: identify subproblems, find recurrence relation, determine base cases.',
                'Time complexity: O(n) for optimized Fibonacci.',
                'Space complexity: O(1) for optimized Fibonacci.'
            ]
        }
        return solution
    
    def solve_sorting(self, problem_text: str) -> Dict:
        """Solve Sorting problem"""
        solution = {
            'title': 'Sorting Algorithm Solution',
            'description': 'Common sorting algorithms implementation',
            'approaches': [
                {
                    'name': 'Quick Sort',
                    'complexity': 'O(n log n) average, O(n²) worst case',
                    'code': {
                        'python': '''def quickSort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quickSort(left) + middle + quickSort(right)''',
                        'java': '''public void quickSort(int[] arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

private int partition(int[] arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    
    for (int j = low; j < high; j++) {
        if (arr[j] < pivot) {
            i++;
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }
    
    int temp = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = temp;
    
    return i + 1;
}''',
                        'cpp': '''void quickSort(vector<int>& arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

int partition(vector<int>& arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    
    for (int j = low; j < high; j++) {
        if (arr[j] < pivot) {
            i++;
            swap(arr[i], arr[j]);
        }
    }
    
    swap(arr[i + 1], arr[high]);
    return i + 1;
}'''
                    }
                }
            ],
            'explanation': [
                'Quick sort is a divide-and-conquer algorithm.',
                'It chooses a pivot element and partitions the array around it.',
                'Elements smaller than pivot go to the left, larger to the right.',
                'Recursively sort the left and right partitions.',
                'Average time complexity: O(n log n).',
                'Worst case time complexity: O(n²) when array is already sorted.',
                'Space complexity: O(log n) due to recursion stack.'
            ]
        }
        return solution
    
    def solve_graph(self, problem_text: str) -> Dict:
        """Solve Graph problem"""
        solution = {
            'title': 'Graph Algorithm Solution',
            'description': 'Common graph algorithms and traversals',
            'approaches': [
                {
                    'name': 'Breadth First Search (BFS)',
                    'complexity': 'O(V + E) time, O(V) space',
                    'code': {
                        'python': '''from collections import defaultdict, deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    result = []
    
    while queue:
        vertex = queue.popleft()
        result.append(vertex)
        
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return result''',
                        'java': '''import java.util.*;

public List<Integer> bfs(Map<Integer, List<Integer>> graph, int start) {
    Set<Integer> visited = new HashSet<>();
    Queue<Integer> queue = new LinkedList<>();
    List<Integer> result = new ArrayList<>();
    
    queue.offer(start);
    visited.add(start);
    
    while (!queue.isEmpty()) {
        int vertex = queue.poll();
        result.add(vertex);
        
        for (int neighbor : graph.getOrDefault(vertex, new ArrayList<>())) {
            if (!visited.contains(neighbor)) {
                visited.add(neighbor);
                queue.offer(neighbor);
            }
        }
    }
    
    return result;
}''',
                        'cpp': '''#include <vector>
#include <queue>
#include <unordered_set>
#include <unordered_map>

vector<int> bfs(unordered_map<int, vector<int>>& graph, int start) {
    unordered_set<int> visited;
    queue<int> q;
    vector<int> result;
    
    q.push(start);
    visited.insert(start);
    
    while (!q.empty()) {
        int vertex = q.front();
        q.pop();
        result.push_back(vertex);
        
        for (int neighbor : graph[vertex]) {
            if (visited.find(neighbor) == visited.end()) {
                visited.insert(neighbor);
                q.push(neighbor);
            }
        }
    }
    
    return result;
}'''
                    }
                }
            ],
            'explanation': [
                'BFS explores all vertices at the current depth before moving to the next level.',
                'It uses a queue data structure to maintain the order of exploration.',
                'BFS is useful for finding shortest paths in unweighted graphs.',
                'It can also be used for level-order traversal of trees.',
                'Time complexity: O(V + E) where V is vertices and E is edges.',
                'Space complexity: O(V) for the queue and visited set.'
            ]
        }
        return solution
    
    def solve_stack_queue(self, problem_text: str) -> Dict:
        """Solve Stack/Queue problem"""
        solution = {
            'title': 'Stack/Queue Solution',
            'description': 'Stack and queue data structure implementations',
            'approaches': [
                {
                    'name': 'Stack Implementation',
                    'complexity': 'O(1) for push/pop, O(n) space',
                    'code': {
                        'python': '''class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("Stack is empty")
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        raise IndexError("Stack is empty")
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)''',
                        'java': '''import java.util.*;

public class Stack<T> {
    private List<T> items;
    
    public Stack() {
        items = new ArrayList<>();
    }
    
    public void push(T item) {
        items.add(item);
    }
    
    public T pop() {
        if (isEmpty()) {
            throw new IllegalStateException("Stack is empty");
        }
        return items.remove(items.size() - 1);
    }
    
    public T peek() {
        if (isEmpty()) {
            throw new IllegalStateException("Stack is empty");
        }
        return items.get(items.size() - 1);
    }
    
    public boolean isEmpty() {
        return items.isEmpty();
    }
    
    public int size() {
        return items.size();
    }
}''',
                        'cpp': '''#include <vector>
#include <stdexcept>

template<typename T>
class Stack {
private:
    std::vector<T> items;
    
public:
    void push(const T& item) {
        items.push_back(item);
    }
    
    T pop() {
        if (isEmpty()) {
            throw std::runtime_error("Stack is empty");
        }
        T item = items.back();
        items.pop_back();
        return item;
    }
    
    T peek() const {
        if (isEmpty()) {
            throw std::runtime_error("Stack is empty");
        }
        return items.back();
    }
    
    bool isEmpty() const {
        return items.empty();
    }
    
    size_t size() const {
        return items.size();
    }
};'''
                    }
                }
            ],
            'explanation': [
                'Stack follows LIFO (Last In, First Out) principle.',
                'Main operations: push (add), pop (remove), peek (view top).',
                'Stack can be implemented using arrays or linked lists.',
                'Common applications: function call stack, undo operations, parentheses matching.',
                'Time complexity: O(1) for push, pop, and peek operations.',
                'Space complexity: O(n) where n is the number of elements.'
            ]
        }
        return solution
    
    def solve_string_manipulation(self, problem_text: str) -> Dict:
        """Solve String Manipulation problem"""
        solution = {
            'title': 'String Manipulation Solution',
            'description': 'Common string manipulation algorithms',
            'approaches': [
                {
                    'name': 'Palindrome Check',
                    'complexity': 'O(n) time, O(1) space',
                    'code': {
                        'python': '''def isPalindrome(s):
    # Remove non-alphanumeric characters and convert to lowercase
    s = ''.join(c.lower() for c in s if c.isalnum())
    
    # Check if string is palindrome
    return s == s[::-1]''',
                        'java': '''public boolean isPalindrome(String s) {
    // Remove non-alphanumeric characters and convert to lowercase
    String cleaned = s.replaceAll("[^a-zA-Z0-9]", "").toLowerCase();
    
    // Check if string is palindrome
    int left = 0, right = cleaned.length() - 1;
    while (left < right) {
        if (cleaned.charAt(left) != cleaned.charAt(right)) {
            return false;
        }
        left++;
        right--;
    }
    return true;
}''',
                        'cpp': '''#include <string>
#include <cctype>

bool isPalindrome(string s) {
    // Remove non-alphanumeric characters and convert to lowercase
    string cleaned;
    for (char c : s) {
        if (isalnum(c)) {
            cleaned += tolower(c);
        }
    }
    
    // Check if string is palindrome
    int left = 0, right = cleaned.length() - 1;
    while (left < right) {
        if (cleaned[left] != cleaned[right]) {
            return false;
        }
        left++;
        right--;
    }
    return true;
}'''
                    }
                }
            ],
            'explanation': [
                'String manipulation involves operations like searching, replacing, and transforming strings.',
                'Palindrome check verifies if a string reads the same forward and backward.',
                'We first clean the string by removing non-alphanumeric characters.',
                'Then we compare characters from both ends moving towards the center.',
                'Time complexity: O(n) where n is the length of the string.',
                'Space complexity: O(1) as we use constant extra space.'
            ]
        }
        return solution
    
    def solve_array_manipulation(self, problem_text: str) -> Dict:
        """Solve Array Manipulation problem"""
        solution = {
            'title': 'Array Manipulation Solution',
            'description': 'Common array manipulation algorithms',
            'approaches': [
                {
                    'name': 'Kadane\'s Algorithm (Maximum Subarray)',
                    'complexity': 'O(n) time, O(1) space',
                    'code': {
                        'python': '''def maxSubArray(nums):
    max_current = max_global = nums[0]
    
    for i in range(1, len(nums)):
        max_current = max(nums[i], max_current + nums[i])
        max_global = max(max_global, max_current)
    
    return max_global''',
                        'java': '''public int maxSubArray(int[] nums) {
    int maxCurrent = nums[0];
    int maxGlobal = nums[0];
    
    for (int i = 1; i < nums.length; i++) {
        maxCurrent = Math.max(nums[i], maxCurrent + nums[i]);
        maxGlobal = Math.max(maxGlobal, maxCurrent);
    }
    
    return maxGlobal;
}''',
                        'cpp': '''int maxSubArray(vector<int>& nums) {
    int maxCurrent = nums[0];
    int maxGlobal = nums[0];
    
    for (int i = 1; i < nums.size(); i++) {
        maxCurrent = max(nums[i], maxCurrent + nums[i]);
        maxGlobal = max(maxGlobal, maxCurrent);
    }
    
    return maxGlobal;
}'''
                    }
                }
            ],
            'explanation': [
                'Kadane\'s algorithm finds the maximum sum of a contiguous subarray.',
                'It maintains two variables: max_current and max_global.',
                'max_current tracks the maximum sum ending at current position.',
                'max_global tracks the overall maximum sum found so far.',
                'Time complexity: O(n) as we traverse the array once.',
                'Space complexity: O(1) as we use constant extra space.'
            ]
        }
        return solution
    
    def solve(self, problem_text: str) -> Dict:
        """Main solve method for DSA problems"""
        problem_type = self.identify_problem_type(problem_text)
        
        if problem_type in self.algorithms:
            return self.algorithms[problem_type](problem_text)
        else:
            return self.solve_array_manipulation(problem_text)

class TheoreticalSolver:
    """Solver for theoretical questions (DBMS, OOP, System Design)"""
    
    def __init__(self):
        """Initialize theoretical solver"""
        self.theoretical_topics = {
            'dbms': self.solve_dbms,
            'oop': self.solve_oop,
            'system_design': self.solve_system_design,
            'hld': self.solve_system_design,
            'lld': self.solve_system_design
        }
    
    def identify_topic(self, text: str) -> str:
        """Identify the theoretical topic"""
        text_lower = text.lower()
        
        if any(keyword in text_lower for keyword in ['database', 'sql', 'mysql', 'acid', 'normalization']):
            return 'dbms'
        elif any(keyword in text_lower for keyword in ['object oriented', 'class', 'inheritance', 'polymorphism']):
            return 'oop'
        elif any(keyword in text_lower for keyword in ['system design', 'scalability', 'microservices', 'architecture']):
            return 'system_design'
        else:
            return 'dbms'  # Default
    
    def solve_dbms(self, question_text: str) -> Dict:
        """Solve DBMS questions"""
        solution = {
            'title': 'Database Management System (DBMS)',
            'description': 'Comprehensive explanation of DBMS concepts',
            'topics': [
                {
                    'name': 'ACID Properties',
                    'explanation': [
                        'Atomicity: All operations in a transaction succeed or all fail.',
                        'Consistency: Database remains in a valid state before and after transaction.',
                        'Isolation: Concurrent transactions don\'t interfere with each other.',
                        'Durability: Committed transactions persist even after system failure.'
                    ]
                },
                {
                    'name': 'Normalization',
                    'explanation': [
                        '1NF: Eliminate repeating groups and ensure atomic values.',
                        '2NF: Remove partial dependencies (all non-key attributes depend on entire primary key).',
                        '3NF: Remove transitive dependencies (non-key attributes don\'t depend on other non-key attributes).',
                        'BCNF: Every determinant must be a candidate key.',
                        '4NF: Eliminate multi-valued dependencies.',
                        '5NF: Eliminate join dependencies.'
                    ]
                },
                {
                    'name': 'Indexing',
                    'explanation': [
                        'Primary Index: Clustered index on primary key.',
                        'Secondary Index: Non-clustered index on non-primary key columns.',
                        'B-tree Index: Most common, supports range queries.',
                        'Hash Index: Fast equality lookups, no range support.',
                        'Composite Index: Index on multiple columns.',
                        'Covering Index: Contains all columns needed for a query.'
                    ]
                },
                {
                    'name': 'Transaction Isolation Levels',
                    'explanation': [
                        'Read Uncommitted: Lowest isolation, allows dirty reads.',
                        'Read Committed: Prevents dirty reads, allows non-repeatable reads.',
                        'Repeatable Read: Prevents dirty and non-repeatable reads.',
                        'Serializable: Highest isolation, prevents all concurrency anomalies.'
                    ]
                }
            ],
            'code_examples': {
                'sql_basics': '''-- Basic SQL operations
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com');
SELECT * FROM users WHERE email = 'john@example.com';
UPDATE users SET name = 'Jane Doe' WHERE id = 1;
DELETE FROM users WHERE id = 1;''',
                'joins': '''-- Different types of JOINs
SELECT u.name, o.order_id
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

SELECT u.name, o.order_id
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

SELECT u.name, o.order_id
FROM users u
RIGHT JOIN orders o ON u.id = o.user_id;'''
            }
        }
        return solution
    
    def solve_oop(self, question_text: str) -> Dict:
        """Solve OOP questions"""
        solution = {
            'title': 'Object-Oriented Programming (OOP)',
            'description': 'Comprehensive explanation of OOP concepts',
            'topics': [
                {
                    'name': 'Four Pillars of OOP',
                    'explanation': [
                        'Encapsulation: Bundling data and methods that operate on that data.',
                        'Inheritance: Creating new classes from existing ones.',
                        'Polymorphism: Same interface, different implementations.',
                        'Abstraction: Hiding complex implementation details.'
                    ]
                },
                {
                    'name': 'Access Modifiers',
                    'explanation': [
                        'Public: Accessible from anywhere.',
                        'Private: Accessible only within the same class.',
                        'Protected: Accessible within the same package and subclasses.',
                        'Default (Package-private): Accessible within the same package.'
                    ]
                },
                {
                    'name': 'Design Patterns',
                    'explanation': [
                        'Singleton: Ensures only one instance of a class exists.',
                        'Factory: Creates objects without specifying exact class.',
                        'Observer: Notifies multiple objects when state changes.',
                        'Strategy: Defines family of algorithms, makes them interchangeable.',
                        'Decorator: Adds behavior to objects dynamically.',
                        'Command: Encapsulates request as an object.'
                    ]
                }
            ],
            'code_examples': {
                'java_oop': '''// Java OOP Example
public abstract class Animal {
    protected String name;
    
    public Animal(String name) {
        this.name = name;
    }
    
    public abstract void makeSound();
    
    public void sleep() {
        System.out.println(name + " is sleeping");
    }
}

public class Dog extends Animal {
    public Dog(String name) {
        super(name);
    }
    
    @Override
    public void makeSound() {
        System.out.println(name + " says: Woof!");
    }
}

public class Cat extends Animal {
    public Cat(String name) {
        super(name);
    }
    
    @Override
    public void makeSound() {
        System.out.println(name + " says: Meow!");
    }
}''',
                'python_oop': '''# Python OOP Example
from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def make_sound(self):
        pass
    
    def sleep(self):
        print(f"{self.name} is sleeping")

class Dog(Animal):
    def make_sound(self):
        print(f"{self.name} says: Woof!")

class Cat(Animal):
    def make_sound(self):
        print(f"{self.name} says: Meow!")

# Polymorphism example
animals = [Dog("Buddy"), Cat("Whiskers")]
for animal in animals:
    animal.make_sound()  # Different implementations'''
            }
        }
        return solution
    
    def solve_system_design(self, question_text: str) -> Dict:
        """Solve System Design questions"""
        solution = {
            'title': 'System Design',
            'description': 'Comprehensive guide to system design principles',
            'topics': [
                {
                    'name': 'Scalability',
                    'explanation': [
                        'Horizontal Scaling: Adding more machines to handle load.',
                        'Vertical Scaling: Adding more resources to existing machines.',
                        'Load Balancing: Distributing traffic across multiple servers.',
                        'Database Sharding: Partitioning data across multiple databases.',
                        'Caching: Storing frequently accessed data in fast storage.',
                        'CDN: Content Delivery Network for static content.'
                    ]
                },
                {
                    'name': 'CAP Theorem',
                    'explanation': [
                        'Consistency: All nodes see the same data at the same time.',
                        'Availability: Every request receives a response.',
                        'Partition Tolerance: System continues operating despite network failures.',
                        'Trade-offs: Can only guarantee two out of three properties.'
                    ]
                },
                {
                    'name': 'Microservices',
                    'explanation': [
                        'Service Decomposition: Breaking application into small, independent services.',
                        'API Gateway: Single entry point for all client requests.',
                        'Service Discovery: Finding and connecting to available services.',
                        'Circuit Breaker: Preventing cascade failures.',
                        'Event-Driven Architecture: Loose coupling through events.',
                        'Container Orchestration: Managing containerized services.'
                    ]
                }
            ],
            'code_examples': {
                'load_balancer': '''// Load Balancer Configuration (Nginx)
upstream backend {
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
    server 192.168.1.12:8080;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}''',
                'cache_implementation': '''// Redis Cache Implementation
import redis

class CacheService:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
    
    def get(self, key):
        return self.redis_client.get(key)
    
    def set(self, key, value, expire=3600):
        self.redis_client.setex(key, expire, value)
    
    def delete(self, key):
        self.redis_client.delete(key)'''
            }
        }
        return solution
    
    def solve(self, question_text: str) -> Dict:
        """Main solve method for theoretical questions"""
        topic = self.identify_topic(question_text)
        
        if topic in self.theoretical_topics:
            return self.theoretical_topics[topic](question_text)
        else:
            return self.solve_dbms(question_text)

class SolverEngine:
    """Main solver engine that coordinates different solvers"""
    
    def __init__(self):
        """Initialize the solver engine"""
        self.dsa_solver = DSASolver()
        self.theoretical_solver = TheoreticalSolver()
    
    def solve(self, routing_info: Dict) -> Dict:
        """
        Solve a question based on routing information
        
        Args:
            routing_info: Routing information from question router
            
        Returns:
            Dictionary containing the solution
        """
        question_text = routing_info['text']
        solver_type = routing_info['solver_type']
        
        logger.info(f"Solving question with {solver_type}")
        
        start_time = time.time()
        
        try:
            if solver_type == "dsa_solver":
                solution = self.dsa_solver.solve(question_text)
            elif solver_type == "theoretical_solver":
                solution = self.theoretical_solver.solve(question_text)
            else:
                # Try both solvers and return the best match
                dsa_solution = self.dsa_solver.solve(question_text)
                theoretical_solution = self.theoretical_solver.solve(question_text)
                
                # Choose based on confidence
                if routing_info['confidence'] > 0.5:
                    solution = dsa_solution
                else:
                    solution = theoretical_solution
            
            solution_time = time.time() - start_time
            
            result = {
                'question': question_text,
                'solver_type': solver_type,
                'solution': solution,
                'processing_time': solution_time,
                'timestamp': time.time()
            }
            
            logger.info(f"Solution generated in {solution_time:.2f} seconds")
            return result
            
        except Exception as e:
            logger.error(f"Error solving question: {e}")
            return {
                'question': question_text,
                'solver_type': solver_type,
                'error': str(e),
                'processing_time': time.time() - start_time,
                'timestamp': time.time()
            }

def test_solver_engine():
    """Test function for the solver engine"""
    engine = SolverEngine()
    
    test_questions = [
        "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
        "Explain ACID properties in database transactions.",
        "What is inheritance in object-oriented programming?",
        "Design a scalable system to handle millions of users."
    ]
    
    for question in test_questions:
        print(f"\n{'='*50}")
        print(f"Question: {question}")
        print(f"{'='*50}")
        
        # Create mock routing info
        routing_info = {
            'text': question,
            'solver_type': 'dsa_solver' if 'array' in question.lower() else 'theoretical_solver',
            'confidence': 0.8
        }
        
        result = engine.solve(routing_info)
        print(f"Solution Type: {result['solver_type']}")
        print(f"Processing Time: {result['processing_time']:.2f}s")
        
        if 'solution' in result:
            solution = result['solution']
            print(f"Title: {solution.get('title', 'N/A')}")
            print(f"Description: {solution.get('description', 'N/A')}")

if __name__ == "__main__":
    test_solver_engine()