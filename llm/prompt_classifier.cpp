/*
 * DSA-X GODMODE++: Ultra-Stealth AI Assistant
 * Prompt Classification Engine
 * 
 * Implemented by Shwet Raj
 * Debug checkpoint: Question type detection and language analysis
 */

#include <string>
#include <vector>
#include <map>
#include <regex>
#include <algorithm>
#include <set>
#include <iostream>

enum class PromptType {
    DSA_ALGORITHM,
    DSA_DATA_STRUCTURE, 
    SYSTEM_DESIGN_HLD,
    SYSTEM_DESIGN_LLD,
    BEHAVIORAL_STAR,
    OOP_DESIGN,
    OS_CONCEPTS,
    DBMS_CONCEPTS,
    NETWORKING,
    GENERAL_CODING,
    UNKNOWN
};

enum class ProgrammingLanguage {
    JAVA,
    CPP,
    PYTHON,
    JAVASCRIPT,
    AUTO_DETECT
};

class PromptClassifier {
private:
    // Keyword patterns for each prompt type
    std::map<PromptType, std::vector<std::string>> keywordPatterns;
    std::map<PromptType, std::vector<std::regex>> regexPatterns;
    std::map<ProgrammingLanguage, std::vector<std::string>> languageKeywords;
    
    // Confidence scoring weights
    struct ScoringWeights {
        float exactKeywordMatch = 2.0f;
        float partialKeywordMatch = 1.0f;
        float regexMatch = 1.5f;
        float contextualMatch = 0.5f;
    } weights;
    
public:
    struct ClassificationResult {
        PromptType type;
        ProgrammingLanguage language;
        float confidence;
        std::vector<std::string> detectedKeywords;
        std::string reasoning;
    };
    
    PromptClassifier() {
        initializePatterns();
    }
    
    ClassificationResult classifyPrompt(const std::string& prompt) {
        ClassificationResult result;
        std::string lowercasePrompt = toLowercase(prompt);
        
        // Calculate scores for each prompt type
        std::map<PromptType, float> scores;
        std::map<PromptType, std::vector<std::string>> matchedKeywords;
        
        for (const auto& [type, keywords] : keywordPatterns) {
            float score = calculateTypeScore(lowercasePrompt, type, matchedKeywords[type]);
            scores[type] = score;
        }
        
        // Find the highest scoring type
        auto maxElement = std::max_element(scores.begin(), scores.end(),
            [](const auto& a, const auto& b) { return a.second < b.second; });
        
        result.type = maxElement->first;
        result.confidence = maxElement->second;
        result.detectedKeywords = matchedKeywords[result.type];
        result.language = detectProgrammingLanguage(lowercasePrompt);
        result.reasoning = generateReasoning(result, scores);
        
        // Normalize confidence to 0-1 range
        result.confidence = std::min(1.0f, result.confidence / 10.0f);
        
        // Set minimum confidence threshold
        if (result.confidence < 0.3f) {
            result.type = PromptType::UNKNOWN;
        }
        
        return result;
    }
    
    std::string promptTypeToString(PromptType type) {
        switch (type) {
            case PromptType::DSA_ALGORITHM: return "DSA Algorithm";
            case PromptType::DSA_DATA_STRUCTURE: return "DSA Data Structure";
            case PromptType::SYSTEM_DESIGN_HLD: return "System Design (HLD)";
            case PromptType::SYSTEM_DESIGN_LLD: return "System Design (LLD)";
            case PromptType::BEHAVIORAL_STAR: return "Behavioral (STAR)";
            case PromptType::OOP_DESIGN: return "OOP Design";
            case PromptType::OS_CONCEPTS: return "Operating Systems";
            case PromptType::DBMS_CONCEPTS: return "Database Management";
            case PromptType::NETWORKING: return "Networking";
            case PromptType::GENERAL_CODING: return "General Coding";
            case PromptType::UNKNOWN: return "Unknown";
            default: return "Unknown";
        }
    }
    
    std::string languageToString(ProgrammingLanguage lang) {
        switch (lang) {
            case ProgrammingLanguage::JAVA: return "Java";
            case ProgrammingLanguage::CPP: return "C++";
            case ProgrammingLanguage::PYTHON: return "Python";
            case ProgrammingLanguage::JAVASCRIPT: return "JavaScript";
            case ProgrammingLanguage::AUTO_DETECT: return "Auto-detect";
            default: return "Auto-detect";
        }
    }

private:
    void initializePatterns() {
        // DSA Algorithm keywords
        keywordPatterns[PromptType::DSA_ALGORITHM] = {
            "algorithm", "implement", "solve", "optimize", "complexity", "time complexity",
            "space complexity", "sorting", "searching", "recursive", "iterative", "dynamic programming",
            "greedy", "backtracking", "divide and conquer", "merge sort", "quick sort", "binary search",
            "depth first", "breadth first", "dfs", "bfs", "dijkstra", "minimum spanning tree",
            "shortest path", "topological sort", "kadane", "sliding window", "two pointers"
        };
        
        // DSA Data Structure keywords  
        keywordPatterns[PromptType::DSA_DATA_STRUCTURE] = {
            "data structure", "array", "linked list", "stack", "queue", "tree", "binary tree",
            "heap", "hash table", "hash map", "graph", "trie", "segment tree", "fenwick tree",
            "disjoint set", "union find", "priority queue", "deque", "set", "map", "vector",
            "matrix", "2d array", "circular queue", "doubly linked", "avl tree", "red black tree"
        };
        
        // System Design HLD keywords
        keywordPatterns[PromptType::SYSTEM_DESIGN_HLD] = {
            "system design", "architecture", "scalability", "high level design", "microservices",
            "load balancer", "database sharding", "caching", "cdn", "message queue", "pub sub",
            "distributed system", "horizontal scaling", "vertical scaling", "fault tolerance",
            "availability", "consistency", "partition tolerance", "cap theorem", "eventual consistency",
            "master slave", "replication", "federation", "reverse proxy"
        };
        
        // System Design LLD keywords
        keywordPatterns[PromptType::SYSTEM_DESIGN_LLD] = {
            "low level design", "class diagram", "object oriented", "design patterns", "singleton",
            "factory", "observer", "decorator", "strategy", "command", "adapter", "facade",
            "mvc", "mvp", "mvvm", "solid principles", "inheritance", "polymorphism", "encapsulation",
            "abstraction", "interface", "abstract class", "composition", "aggregation"
        };
        
        // Behavioral STAR keywords
        keywordPatterns[PromptType::BEHAVIORAL_STAR] = {
            "tell me about", "describe a time", "give me an example", "walk me through",
            "challenging situation", "conflict", "leadership", "teamwork", "communication",
            "problem solving", "deadline", "stress", "failure", "success", "achievement",
            "weakness", "strength", "motivation", "career goal", "why do you want",
            "how do you handle", "experience with", "project you worked on"
        };
        
        // OOP Design keywords
        keywordPatterns[PromptType::OOP_DESIGN] = {
            "object oriented", "class design", "inheritance", "polymorphism", "encapsulation",
            "abstraction", "interface", "abstract", "virtual", "override", "overload",
            "constructor", "destructor", "static", "final", "private", "protected", "public",
            "composition", "aggregation", "has-a", "is-a", "coupling", "cohesion"
        };
        
        // OS Concepts keywords
        keywordPatterns[PromptType::OS_CONCEPTS] = {
            "operating system", "process", "thread", "scheduling", "deadlock", "semaphore",
            "mutex", "synchronization", "memory management", "virtual memory", "paging",
            "segmentation", "file system", "i/o", "interrupt", "system call", "kernel",
            "user space", "context switching", "race condition", "critical section",
            "producer consumer", "readers writers", "dining philosophers"
        };
        
        // DBMS keywords
        keywordPatterns[PromptType::DBMS_CONCEPTS] = {
            "database", "sql", "nosql", "relational", "normalization", "denormalization",
            "acid", "transaction", "isolation", "consistency", "durability", "atomicity",
            "index", "b-tree", "hash index", "join", "inner join", "outer join", "foreign key",
            "primary key", "constraint", "trigger", "stored procedure", "view", "materialized view",
            "replication", "partitioning", "mongodb", "mysql", "postgresql"
        };
        
        // Networking keywords
        keywordPatterns[PromptType::NETWORKING] = {
            "network", "tcp", "udp", "http", "https", "rest", "api", "socket", "protocol",
            "osi model", "tcp/ip", "dns", "dhcp", "nat", "firewall", "load balancing",
            "routing", "switching", "ethernet", "wifi", "ssl", "tls", "websocket",
            "cors", "authentication", "authorization", "oauth", "jwt"
        };
        
        // General Coding keywords
        keywordPatterns[PromptType::GENERAL_CODING] = {
            "code", "function", "method", "class", "variable", "loop", "condition", "if else",
            "switch", "for loop", "while loop", "return", "parameter", "argument", "exception",
            "error handling", "try catch", "debug", "test", "unit test", "refactor", "optimize"
        };
        
        // Programming language keywords
        languageKeywords[ProgrammingLanguage::JAVA] = {
            "java", "class", "public static void main", "system.out.println", "arraylist",
            "hashmap", "string", "integer", "public", "private", "protected", "static",
            "final", "extends", "implements", "interface", "package", "import"
        };
        
        languageKeywords[ProgrammingLanguage::CPP] = {
            "c++", "cpp", "#include", "iostream", "vector", "map", "unordered_map", "std::",
            "namespace", "using namespace std", "cin", "cout", "endl", "template", "class",
            "struct", "public:", "private:", "protected:", "virtual", "const"
        };
        
        languageKeywords[ProgrammingLanguage::PYTHON] = {
            "python", "def", "class", "import", "from", "if __name__", "print", "len",
            "range", "enumerate", "list", "dict", "tuple", "set", "lambda", "self",
            "init", "return", "pass", "elif", "is", "in", "not in"
        };
        
        languageKeywords[ProgrammingLanguage::JAVASCRIPT] = {
            "javascript", "js", "function", "var", "let", "const", "console.log", "array",
            "object", "json", "async", "await", "promise", "callback", "arrow function",
            "prototype", "this", "null", "undefined", "typeof", "node.js", "npm"
        };
        
        // Initialize regex patterns for more complex matching
        initializeRegexPatterns();
    }
    
    void initializeRegexPatterns() {
        // DSA Algorithm patterns
        regexPatterns[PromptType::DSA_ALGORITHM] = {
            std::regex(R"(find.*minimum|maximum)"),
            std::regex(R"(sort.*array|list)"),
            std::regex(R"(search.*element|target)"),
            std::regex(R"(path.*graph|tree)"),
            std::regex(R"(O\([^)]+\))"), // Big O notation
            std::regex(R"(time.*complexity|space.*complexity)")
        };
        
        // System Design patterns
        regexPatterns[PromptType::SYSTEM_DESIGN_HLD] = {
            std::regex(R"(design.*system|application)"),
            std::regex(R"(handle.*million|billion.*users)"),
            std::regex(R"(scale.*to.*users)"),
            std::regex(R"(how.*would.*you.*design)")
        };
        
        // Behavioral patterns
        regexPatterns[PromptType::BEHAVIORAL_STAR] = {
            std::regex(R"(tell.*me.*about.*time)"),
            std::regex(R"(describe.*situation|experience)"),
            std::regex(R"(give.*example.*when)"),
            std::regex(R"(how.*did.*you.*handle)")
        };
    }
    
    float calculateTypeScore(const std::string& prompt, PromptType type, 
                           std::vector<std::string>& matchedKeywords) {
        float score = 0.0f;
        
        // Check keyword matches
        for (const std::string& keyword : keywordPatterns[type]) {
            if (prompt.find(keyword) != std::string::npos) {
                score += weights.exactKeywordMatch;
                matchedKeywords.push_back(keyword);
            } else {
                // Check for partial matches
                std::vector<std::string> keywordWords = splitString(keyword);
                int partialMatches = 0;
                for (const std::string& word : keywordWords) {
                    if (prompt.find(word) != std::string::npos) {
                        partialMatches++;
                    }
                }
                if (partialMatches > 0) {
                    score += weights.partialKeywordMatch * (partialMatches / (float)keywordWords.size());
                }
            }
        }
        
        // Check regex patterns
        for (const std::regex& pattern : regexPatterns[type]) {
            if (std::regex_search(prompt, pattern)) {
                score += weights.regexMatch;
            }
        }
        
        return score;
    }
    
    ProgrammingLanguage detectProgrammingLanguage(const std::string& prompt) {
        std::map<ProgrammingLanguage, float> scores;
        
        for (const auto& [lang, keywords] : languageKeywords) {
            float score = 0.0f;
            for (const std::string& keyword : keywords) {
                if (prompt.find(keyword) != std::string::npos) {
                    score += 1.0f;
                }
            }
            scores[lang] = score;
        }
        
        // Find highest scoring language
        auto maxElement = std::max_element(scores.begin(), scores.end(),
            [](const auto& a, const auto& b) { return a.second < b.second; });
        
        if (maxElement->second > 0.0f) {
            return maxElement->first;
        }
        
        return ProgrammingLanguage::AUTO_DETECT;
    }
    
    std::string generateReasoning(const ClassificationResult& result,
                                const std::map<PromptType, float>& scores) {
        std::string reasoning = "Classification: " + promptTypeToString(result.type) + 
                              " (confidence: " + std::to_string(result.confidence) + ")\n";
        
        reasoning += "Detected keywords: ";
        for (size_t i = 0; i < result.detectedKeywords.size(); ++i) {
            reasoning += result.detectedKeywords[i];
            if (i < result.detectedKeywords.size() - 1) reasoning += ", ";
        }
        reasoning += "\n";
        
        reasoning += "Language preference: " + languageToString(result.language) + "\n";
        
        return reasoning;
    }
    
    std::string toLowercase(const std::string& str) {
        std::string result = str;
        std::transform(result.begin(), result.end(), result.begin(), ::tolower);
        return result;
    }
    
    std::vector<std::string> splitString(const std::string& str, char delimiter = ' ') {
        std::vector<std::string> tokens;
        std::string token;
        for (char c : str) {
            if (c == delimiter) {
                if (!token.empty()) {
                    tokens.push_back(token);
                    token.clear();
                }
            } else {
                token += c;
            }
        }
        if (!token.empty()) {
            tokens.push_back(token);
        }
        return tokens;
    }
};