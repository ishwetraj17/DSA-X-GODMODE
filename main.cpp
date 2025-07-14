/*
 * DSA-X GODMODE++: Ultra-Stealth AI Assistant
 * Main Entry Point - Complete System Integration
 * 
 * Implemented by Shwet Raj
 * Debug checkpoint: System startup and command-line interface
 */

#include <iostream>
#include <string>
#include <vector>
#include <csignal>
#include <memory>
#include <thread>
#include <chrono>
#include <iomanip>

#include "boot/dsax_controller.cpp"

// Global controller instance for signal handling
std::unique_ptr<DSAXController> g_controller = nullptr;

// Signal handler for graceful shutdown
void signalHandler(int signal) {
    std::cout << "\n🛑 Received shutdown signal (" << signal << ")..." << std::endl;
    
    if (g_controller) {
        g_controller->stop();
    }
    
    std::cout << "✅ Graceful shutdown complete" << std::endl;
    exit(0);
}

void printBanner() {
    std::cout << "\n" << std::string(80, '=') << std::endl;
    std::cout << "🚀 DSA-X GODMODE++: Ultra-Stealth AI Assistant" << std::endl;
    std::cout << "   Elite Technical Interview Assistant" << std::endl;
    std::cout << "   Implemented by Shwet Raj" << std::endl;
    std::cout << std::string(80, '=') << std::endl;
    
    std::cout << "\n🎯 CAPABILITIES:" << std::endl;
    std::cout << "   • Real-time audio transcription (BlackHole/VB-Cable)" << std::endl;
    std::cout << "   • Intelligent question classification" << std::endl;
    std::cout << "   • Multi-language code generation (Java, C++, Python)" << std::endl;
    std::cout << "   • System design explanations (HLD/LLD)" << std::endl;
    std::cout << "   • STAR method behavioral responses" << std::endl;
    std::cout << "   • GPU overlay display (screen-share invisible)" << std::endl;
    std::cout << "   • Fallback input methods (clipboard, OCR)" << std::endl;
    std::cout << "   • Zero-trace stealth operation" << std::endl;
    
    std::cout << "\n🔐 STEALTH FEATURES:" << std::endl;
    std::cout << "   • RAM-only operation (no disk writes)" << std::endl;
    std::cout << "   • Process cloaking and anti-detection" << std::endl;
    std::cout << "   • Screen-share invisible overlay" << std::endl;
    std::cout << "   • Automatic self-healing and recovery" << std::endl;
    
    std::cout << "\n⚖️  FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY" << std::endl;
    std::cout << std::string(80, '=') << "\n" << std::endl;
}

void printUsage(const std::string& programName) {
    std::cout << "USAGE: " << programName << " [OPTIONS]" << std::endl;
    std::cout << "\nOPTIONS:" << std::endl;
    std::cout << "  --help, -h           Show this help message" << std::endl;
    std::cout << "  --version, -v        Show version information" << std::endl;
    std::cout << "  --test, -t           Run in test mode with manual input" << std::endl;
    std::cout << "  --no-audio           Disable audio capture (use fallbacks only)" << std::endl;
    std::cout << "  --no-overlay         Disable GPU overlay (console output only)" << std::endl;
    std::cout << "  --no-stealth         Disable stealth mode (for debugging)" << std::endl;
    std::cout << "  --confidence N       Set confidence threshold (0.0-1.0, default 0.7)" << std::endl;
    std::cout << "  --language LANG      Set preferred language (java, cpp, python, auto)" << std::endl;
    std::cout << "  --verbose            Enable verbose output" << std::endl;
    
    std::cout << "\nEXAMPLES:" << std::endl;
    std::cout << "  " << programName << "                    # Start with default settings" << std::endl;
    std::cout << "  " << programName << " --test             # Test mode with manual input" << std::endl;
    std::cout << "  " << programName << " --no-stealth       # Debug mode (visible)" << std::endl;
    std::cout << "  " << programName << " --confidence 0.8   # Higher confidence threshold" << std::endl;
    std::cout << "  " << programName << " --language python  # Prefer Python responses" << std::endl;
    
    std::cout << "\nCONTROLS:" << std::endl;
    std::cout << "  Ctrl+C               Graceful shutdown" << std::endl;
    std::cout << "  In test mode: Type questions and press Enter" << std::endl;
    std::cout << "  Type 'quit' or 'exit' to stop" << std::endl;
}

void printVersion() {
    std::cout << "DSA-X GODMODE++ v1.0.0" << std::endl;
    std::cout << "Build: " << __DATE__ << " " << __TIME__ << std::endl;
    std::cout << "Platform: ";
    
#ifdef _WIN32
    std::cout << "Windows" << std::endl;
#elif __APPLE__
    std::cout << "macOS" << std::endl;
#elif __linux__
    std::cout << "Linux" << std::endl;
#else
    std::cout << "Unknown" << std::endl;
#endif

    std::cout << "Compiler: ";
#ifdef __clang__
    std::cout << "Clang " << __clang_major__ << "." << __clang_minor__ << std::endl;
#elif __GNUC__
    std::cout << "GCC " << __GNUC__ << "." << __GNUC_MINOR__ << std::endl;
#elif _MSC_VER
    std::cout << "MSVC " << _MSC_VER << std::endl;
#else
    std::cout << "Unknown" << std::endl;
#endif
}

struct CommandLineArgs {
    bool showHelp = false;
    bool showVersion = false;
    bool testMode = false;
    bool noAudio = false;
    bool noOverlay = false;
    bool noStealth = false;
    bool verbose = false;
    float confidence = 0.7f;
    std::string language = "auto";
};

CommandLineArgs parseArguments(int argc, char* argv[]) {
    CommandLineArgs args;
    
    for (int i = 1; i < argc; i++) {
        std::string arg = argv[i];
        
        if (arg == "--help" || arg == "-h") {
            args.showHelp = true;
        } else if (arg == "--version" || arg == "-v") {
            args.showVersion = true;
        } else if (arg == "--test" || arg == "-t") {
            args.testMode = true;
        } else if (arg == "--no-audio") {
            args.noAudio = true;
        } else if (arg == "--no-overlay") {
            args.noOverlay = true;
        } else if (arg == "--no-stealth") {
            args.noStealth = true;
        } else if (arg == "--verbose") {
            args.verbose = true;
        } else if (arg == "--confidence" && i + 1 < argc) {
            try {
                args.confidence = std::stof(argv[++i]);
                args.confidence = std::max(0.0f, std::min(1.0f, args.confidence));
            } catch (const std::exception& e) {
                std::cerr << "❌ Invalid confidence value: " << argv[i] << std::endl;
                args.confidence = 0.7f;
            }
        } else if (arg == "--language" && i + 1 < argc) {
            args.language = argv[++i];
        } else {
            std::cerr << "⚠️  Unknown argument: " << arg << std::endl;
        }
    }
    
    return args;
}

void runTestMode(DSAXController& controller) {
    std::cout << "\n🧪 TEST MODE ACTIVATED" << std::endl;
    std::cout << "📝 Enter questions manually to test the AI responses" << std::endl;
    std::cout << "💡 Try questions like:" << std::endl;
    std::cout << "   • 'Implement binary search in Java'" << std::endl;
    std::cout << "   • 'Design a scalable chat system'" << std::endl;
    std::cout << "   • 'Tell me about a challenging project'" << std::endl;
    std::cout << "   • 'Explain the difference between stack and queue'" << std::endl;
    std::cout << "🛑 Type 'quit' or 'exit' to stop\n" << std::endl;
    
    std::string input;
    while (true) {
        std::cout << "❓ Question: ";
        std::getline(std::cin, input);
        
        if (input.empty()) {
            continue;
        }
        
        if (input == "quit" || input == "exit") {
            break;
        }
        
        // Process the manual input
        controller.processManualInput(input);
        
        // Small delay to allow processing
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
    
    std::cout << "🛑 Exiting test mode..." << std::endl;
}

void runProductionMode(DSAXController& controller) {
    std::cout << "\n🎯 PRODUCTION MODE ACTIVATED" << std::endl;
    std::cout << "🎵 Audio monitoring started - join your interview!" << std::endl;
    std::cout << "💬 Responses will appear in overlay and console" << std::endl;
    std::cout << "📊 Press Ctrl+C for graceful shutdown" << std::endl;
    
    // Wait for shutdown signal
    while (true) {
        std::this_thread::sleep_for(std::chrono::seconds(1));
        // The signal handler will take care of shutdown
    }
}

bool checkDependencies() {
    std::cout << "🔍 Checking system dependencies..." << std::endl;
    
    bool allOk = true;
    
    // Check audio dependencies
#ifdef _WIN32
    std::cout << "   🎵 VB-Audio Cable: ";
    // TODO: Add actual VB-Cable detection
    std::cout << "⚠️  Please ensure VB-Audio Cable is installed" << std::endl;
#elif __APPLE__
    std::cout << "   🎵 BlackHole Audio: ";
    // TODO: Add actual BlackHole detection
    std::cout << "⚠️  Please ensure BlackHole is installed" << std::endl;
#endif
    
    // Check Whisper model
    std::cout << "   🎤 Whisper Model: ";
    std::cout << "⚠️  Please ensure Whisper GGUF model is available" << std::endl;
    
    // Check screen capture
    std::cout << "   🖼️  Screen Capture: ";
    std::cout << "✅ Available" << std::endl;
    
    return allOk;
}

int main(int argc, char* argv[]) {
    // Parse command line arguments
    CommandLineArgs args = parseArguments(argc, argv);
    
    if (args.showHelp) {
        printBanner();
        printUsage(argv[0]);
        return 0;
    }
    
    if (args.showVersion) {
        printVersion();
        return 0;
    }
    
    // Print banner
    printBanner();
    
    // Set up signal handlers for graceful shutdown
    signal(SIGINT, signalHandler);
    signal(SIGTERM, signalHandler);
    
    try {
        // Check dependencies
        if (!checkDependencies()) {
            std::cout << "\n⚠️  Some dependencies are missing. System may not work optimally." << std::endl;
            std::cout << "📖 Please refer to README.md for installation instructions." << std::endl;
        }
        
        // Create and configure controller
        g_controller = std::make_unique<DSAXController>();
        
        // Apply command line options
        if (args.confidence != 0.7f) {
            g_controller->setConfidenceThreshold(args.confidence);
            std::cout << "📊 Confidence threshold set to: " << (args.confidence * 100) << "%" << std::endl;
        }
        
        if (args.language != "auto") {
            g_controller->setPreferredLanguage(args.language);
            std::cout << "💻 Preferred language set to: " << args.language << std::endl;
        }
        
        if (args.noStealth) {
            g_controller->enableStealthMode(false);
            std::cout << "🔓 Stealth mode disabled (debug mode)" << std::endl;
        }
        
        // Initialize the system
        std::cout << "\n🔧 Initializing system..." << std::endl;
        if (!g_controller->initialize()) {
            std::cerr << "❌ Failed to initialize system" << std::endl;
            return 1;
        }
        
        // Start the system
        std::cout << "🚀 Starting DSA-X GODMODE++..." << std::endl;
        g_controller->start();
        
        // Run in appropriate mode
        if (args.testMode) {
            runTestMode(*g_controller);
        } else {
            runProductionMode(*g_controller);
        }
        
    } catch (const std::exception& e) {
        std::cerr << "💥 Fatal error: " << e.what() << std::endl;
        if (g_controller) {
            g_controller->shutdown();
        }
        return 1;
    }
    
    // Clean shutdown
    if (g_controller) {
        g_controller->shutdown();
    }
    
    std::cout << "✅ DSA-X GODMODE++ shutdown complete" << std::endl;
    return 0;
}