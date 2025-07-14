/*
 * DSA-X GODMODE++: Ultra-Stealth AI Assistant
 * Main System Controller - Integration Layer
 * 
 * Implemented by Shwet Raj
 * Debug checkpoint: System integration and component orchestration
 */

#include <iostream>
#include <thread>
#include <chrono>
#include <atomic>
#include <queue>
#include <mutex>
#include <condition_variable>
#include <memory>

#ifdef _WIN32
    #include "audio_input_windows.cpp"
    #include "../overlay/overlay_windows.cpp"
#elif __APPLE__
    #include "audio_input_mac.cpp"
    #include "../overlay/overlay_mac.mm"
#endif

#include "whisper_runner.cpp"
#include "../llm/prompt_classifier.cpp"
#include "../llm/answer_generator.cpp"
#include "stealth_enforcer.cpp"
#include "self_healing.cpp"

class DSAXController {
private:
    // Core system components
#ifdef _WIN32
    std::unique_ptr<WindowsAudioCapture> audioCapture;
    std::unique_ptr<WindowsOverlay> overlay;
#elif __APPLE__
    std::unique_ptr<MacAudioCapture> audioCapture;
    std::unique_ptr<StealthOverlayWindow> overlay;
#endif
    
    std::unique_ptr<WhisperRunner> whisperProcessor;
    std::unique_ptr<PromptClassifier> classifier;
    std::unique_ptr<AnswerGenerator> generator;
    std::unique_ptr<StealthEnforcer> stealthSystem;
    std::unique_ptr<SelfHealingSystem> healingSystem;
    
    // System state
    std::atomic<bool> isRunning;
    std::atomic<bool> isProcessing;
    std::thread mainProcessingThread;
    std::thread overlayUpdateThread;
    
    // Data flow queues
    std::queue<std::string> transcriptionQueue;
    std::queue<std::string> responseQueue;
    std::mutex transcriptionMutex;
    std::mutex responseMutex;
    std::condition_variable dataAvailable;
    
    // Configuration
    struct SystemConfig {
        bool enableStealth = true;
        bool enableSelfHealing = true;
        bool enableAudioCapture = true;
        bool enableOverlay = true;
        int processingIntervalMs = 100;
        float confidenceThreshold = 0.7f;
        std::string preferredLanguage = "auto";
    } config;
    
    // Performance metrics
    struct PerformanceMetrics {
        std::chrono::milliseconds audioLatency{0};
        std::chrono::milliseconds sttLatency{0};
        std::chrono::milliseconds aiLatency{0};
        std::chrono::milliseconds totalLatency{0};
        size_t totalQuestions = 0;
        size_t successfulResponses = 0;
        double successRate = 0.0;
    } metrics;
    
public:
    DSAXController() : isRunning(false), isProcessing(false) {
        std::cout << "🚀 Initializing DSA-X GODMODE++ Controller..." << std::endl;
    }
    
    ~DSAXController() {
        shutdown();
    }
    
    bool initialize() {
        std::cout << "🔧 Starting system initialization..." << std::endl;
        
        try {
            // Initialize stealth system first
            if (config.enableStealth) {
                if (!initializeStealth()) {
                    std::cerr << "❌ Failed to initialize stealth system" << std::endl;
                    return false;
                }
            }
            
            // Initialize self-healing system
            if (config.enableSelfHealing) {
                if (!initializeSelfHealing()) {
                    std::cerr << "❌ Failed to initialize self-healing system" << std::endl;
                    return false;
                }
            }
            
            // Initialize audio capture
            if (config.enableAudioCapture) {
                if (!initializeAudioCapture()) {
                    std::cerr << "⚠️  Audio capture failed, will use fallback methods" << std::endl;
                    // Continue without audio capture - fallbacks will handle input
                }
            }
            
            // Initialize STT processor
            if (!initializeSTT()) {
                std::cerr << "❌ Failed to initialize STT processor" << std::endl;
                return false;
            }
            
            // Initialize AI components
            if (!initializeAI()) {
                std::cerr << "❌ Failed to initialize AI components" << std::endl;
                return false;
            }
            
            // Initialize overlay system
            if (config.enableOverlay) {
                if (!initializeOverlay()) {
                    std::cerr << "⚠️  Overlay initialization failed, responses will be console-only" << std::endl;
                    // Continue without overlay - responses can still be generated
                }
            }
            
            std::cout << "✅ System initialization complete!" << std::endl;
            printSystemStatus();
            return true;
            
        } catch (const std::exception& e) {
            std::cerr << "💥 Initialization error: " << e.what() << std::endl;
            return false;
        }
    }
    
    void start() {
        if (isRunning.load()) {
            std::cout << "⚠️  System already running" << std::endl;
            return;
        }
        
        isRunning = true;
        
        // Start all subsystems
        if (audioCapture) {
            audioCapture->start();
        }
        
        if (whisperProcessor) {
            whisperProcessor->start();
        }
        
        if (stealthSystem) {
            stealthSystem->enable();
        }
        
        if (healingSystem) {
            healingSystem->start();
        }
        
        // Start processing threads
        mainProcessingThread = std::thread(&DSAXController::mainProcessingLoop, this);
        
        if (overlay) {
            overlayUpdateThread = std::thread(&DSAXController::overlayUpdateLoop, this);
        }
        
        std::cout << "🎯 DSA-X GODMODE++ is now ACTIVE and monitoring..." << std::endl;
        std::cout << "📊 Press Ctrl+C to exit safely" << std::endl;
    }
    
    void stop() {
        if (!isRunning.load()) {
            return;
        }
        
        std::cout << "🛑 Initiating graceful shutdown..." << std::endl;
        isRunning = false;
        dataAvailable.notify_all();
        
        // Stop processing threads
        if (mainProcessingThread.joinable()) {
            mainProcessingThread.join();
        }
        
        if (overlayUpdateThread.joinable()) {
            overlayUpdateThread.join();
        }
        
        // Stop all subsystems
        if (audioCapture) {
            audioCapture->stop();
        }
        
        if (whisperProcessor) {
            whisperProcessor->stop();
        }
        
        if (stealthSystem) {
            stealthSystem->disable();
        }
        
        if (healingSystem) {
            healingSystem->stop();
        }
        
        printFinalStatistics();
        std::cout << "✅ Shutdown complete - zero trace maintained" << std::endl;
    }
    
    void shutdown() {
        stop();
        
        // Clean up all components
        audioCapture.reset();
        whisperProcessor.reset();
        classifier.reset();
        generator.reset();
        overlay.reset();
        stealthSystem.reset();
        healingSystem.reset();
    }
    
    // Manual input for testing
    void processManualInput(const std::string& text) {
        if (!isRunning.load()) {
            std::cout << "⚠️  System not running" << std::endl;
            return;
        }
        
        std::lock_guard<std::mutex> lock(transcriptionMutex);
        transcriptionQueue.push(text);
        dataAvailable.notify_one();
        
        std::cout << "📝 Manual input queued: " << text << std::endl;
    }
    
    // Configuration methods
    void setConfidenceThreshold(float threshold) {
        config.confidenceThreshold = std::max(0.0f, std::min(1.0f, threshold));
        if (whisperProcessor) {
            whisperProcessor->setConfidenceThreshold(config.confidenceThreshold);
        }
    }
    
    void setPreferredLanguage(const std::string& language) {
        config.preferredLanguage = language;
    }
    
    void enableStealthMode(bool enable) {
        config.enableStealth = enable;
        if (stealthSystem) {
            if (enable) {
                stealthSystem->enable();
            } else {
                stealthSystem->disable();
            }
        }
    }

private:
    bool initializeStealth() {
        stealthSystem = std::make_unique<StealthEnforcer>();
        if (!stealthSystem->initialize()) {
            return false;
        }
        std::cout << "🥷 Stealth system initialized" << std::endl;
        return true;
    }
    
    bool initializeSelfHealing() {
        healingSystem = std::make_unique<SelfHealingSystem>();
        if (!healingSystem->initialize()) {
            return false;
        }
        std::cout << "🔄 Self-healing system initialized" << std::endl;
        return true;
    }
    
    bool initializeAudioCapture() {
#ifdef _WIN32
        audioCapture = std::make_unique<WindowsAudioCapture>();
#elif __APPLE__
        audioCapture = std::make_unique<MacAudioCapture>();
#endif
        
        if (!audioCapture || !audioCapture->initialize()) {
            return false;
        }
        
        std::cout << "🎵 Audio capture initialized" << std::endl;
        return true;
    }
    
    bool initializeSTT() {
        whisperProcessor = std::make_unique<WhisperRunner>();
        if (!whisperProcessor->initialize()) {
            return false;
        }
        
        whisperProcessor->setConfidenceThreshold(config.confidenceThreshold);
        std::cout << "🎤 STT processor initialized" << std::endl;
        return true;
    }
    
    bool initializeAI() {
        classifier = std::make_unique<PromptClassifier>();
        generator = std::make_unique<AnswerGenerator>();
        
        std::cout << "🧠 AI components initialized" << std::endl;
        return true;
    }
    
    bool initializeOverlay() {
#ifdef _WIN32
        overlay = std::make_unique<WindowsOverlay>();
#elif __APPLE__
        overlay = std::make_unique<StealthOverlayWindow>();
#endif
        
        if (!overlay || !overlay->initialize()) {
            return false;
        }
        
        std::cout << "🖼️  GPU overlay initialized" << std::endl;
        return true;
    }
    
    void mainProcessingLoop() {
        std::cout << "🔄 Main processing loop started" << std::endl;
        
        while (isRunning.load()) {
            try {
                // Check for audio input
                if (audioCapture && audioCapture->isCapturing()) {
                    processAudioInput();
                }
                
                // Check for STT results
                if (whisperProcessor && whisperProcessor->hasTranscription()) {
                    std::string transcription = whisperProcessor->getTranscription();
                    if (!transcription.empty()) {
                        std::lock_guard<std::mutex> lock(transcriptionMutex);
                        transcriptionQueue.push(transcription);
                        dataAvailable.notify_one();
                    }
                }
                
                // Process transcription queue
                processTranscriptionQueue();
                
                // Small delay to prevent excessive CPU usage
                std::this_thread::sleep_for(std::chrono::milliseconds(config.processingIntervalMs));
                
            } catch (const std::exception& e) {
                std::cerr << "🚨 Processing loop error: " << e.what() << std::endl;
                
                // Trigger self-healing if available
                if (healingSystem) {
                    healingSystem->handleError("MainProcessingLoop", e.what());
                }
                
                // Brief pause before retrying
                std::this_thread::sleep_for(std::chrono::milliseconds(1000));
            }
        }
        
        std::cout << "🔄 Main processing loop ended" << std::endl;
    }
    
    void processAudioInput() {
        if (!audioCapture) return;
        
        auto audioData = audioCapture->getAudioData();
        if (!audioData.empty() && whisperProcessor) {
            auto startTime = std::chrono::steady_clock::now();
            
            whisperProcessor->addAudioData(audioData);
            
            auto endTime = std::chrono::steady_clock::now();
            metrics.audioLatency = std::chrono::duration_cast<std::chrono::milliseconds>(endTime - startTime);
        }
    }
    
    void processTranscriptionQueue() {
        std::unique_lock<std::mutex> lock(transcriptionMutex);
        
        while (!transcriptionQueue.empty()) {
            std::string transcription = transcriptionQueue.front();
            transcriptionQueue.pop();
            lock.unlock();
            
            // Process the transcription
            processQuestion(transcription);
            
            lock.lock();
        }
    }
    
    void processQuestion(const std::string& question) {
        if (question.empty() || question.length() < 3) {
            return; // Skip very short or empty questions
        }
        
        auto startTime = std::chrono::steady_clock::now();
        metrics.totalQuestions++;
        
        try {
            std::cout << "❓ Processing: " << question << std::endl;
            
            // Classify the prompt
            auto classification = classifier->classifyPrompt(question);
            
            auto classificationTime = std::chrono::steady_clock::now();
            
            // Generate answer if confidence is sufficient
            if (classification.confidence >= config.confidenceThreshold) {
                auto answer = generator->generateAnswer(question, classification);
                
                auto generationTime = std::chrono::steady_clock::now();
                
                // Display the response
                displayResponse(question, classification, answer);
                
                auto endTime = std::chrono::steady_clock::now();
                
                // Update metrics
                metrics.sttLatency = std::chrono::duration_cast<std::chrono::milliseconds>(classificationTime - startTime);
                metrics.aiLatency = std::chrono::duration_cast<std::chrono::milliseconds>(generationTime - classificationTime);
                metrics.totalLatency = std::chrono::duration_cast<std::chrono::milliseconds>(endTime - startTime);
                metrics.successfulResponses++;
                metrics.successRate = (double)metrics.successfulResponses / metrics.totalQuestions * 100.0;
                
                std::cout << "⚡ Response generated in " << metrics.totalLatency.count() << "ms" << std::endl;
                
            } else {
                std::cout << "🤔 Low confidence (" << classification.confidence << "), skipping response" << std::endl;
            }
            
        } catch (const std::exception& e) {
            std::cerr << "🚨 Question processing error: " << e.what() << std::endl;
            
            if (healingSystem) {
                healingSystem->handleError("QuestionProcessing", e.what());
            }
        }
    }
    
    void displayResponse(const std::string& question, 
                        const PromptClassifier::ClassificationResult& classification,
                        const AnswerGenerator::GeneratedAnswer& answer) {
        
        // Console output
        std::cout << "\n" << std::string(80, '=') << std::endl;
        std::cout << "🎯 QUESTION TYPE: " << classifier->promptTypeToString(classification.type) << std::endl;
        std::cout << "💻 LANGUAGE: " << answer.language << std::endl;
        std::cout << "📊 CONFIDENCE: " << (classification.confidence * 100) << "%" << std::endl;
        std::cout << std::string(80, '-') << std::endl;
        
        if (!answer.explanation.empty()) {
            std::cout << "📝 EXPLANATION:\n" << answer.explanation << std::endl;
            std::cout << std::string(80, '-') << std::endl;
        }
        
        if (!answer.code.empty()) {
            std::cout << "💻 CODE:\n" << answer.code << std::endl;
            std::cout << std::string(80, '-') << std::endl;
        }
        
        if (!answer.complexity.empty()) {
            std::cout << "⚡ COMPLEXITY: " << answer.complexity << std::endl;
        }
        
        std::cout << std::string(80, '=') << "\n" << std::endl;
        
        // Send to overlay if available
        if (overlay) {
            std::string displayText = formatForOverlay(classification, answer);
            std::lock_guard<std::mutex> lock(responseMutex);
            responseQueue.push(displayText);
        }
    }
    
    std::string formatForOverlay(const PromptClassifier::ClassificationResult& classification,
                               const AnswerGenerator::GeneratedAnswer& answer) {
        std::ostringstream formatted;
        
        formatted << classifier->promptTypeToString(classification.type) << " | " << answer.language << "\n";
        
        if (!answer.explanation.empty()) {
            // Take first few lines for overlay
            std::istringstream explanationStream(answer.explanation);
            std::string line;
            int lineCount = 0;
            while (std::getline(explanationStream, line) && lineCount < 5) {
                formatted << line << "\n";
                lineCount++;
            }
        }
        
        if (!answer.code.empty()) {
            formatted << "\nCODE:\n";
            // Take first few lines of code
            std::istringstream codeStream(answer.code);
            std::string line;
            int lineCount = 0;
            while (std::getline(codeStream, line) && lineCount < 10) {
                formatted << line << "\n";
                lineCount++;
            }
        }
        
        return formatted.str();
    }
    
    void overlayUpdateLoop() {
        std::cout << "🖼️  Overlay update loop started" << std::endl;
        
        while (isRunning.load()) {
            try {
                std::unique_lock<std::mutex> lock(responseMutex);
                
                if (!responseQueue.empty()) {
                    std::string response = responseQueue.front();
                    responseQueue.pop();
                    lock.unlock();
                    
                    if (overlay) {
                        overlay->updateDisplay(response);
                    }
                } else {
                    lock.unlock();
                    std::this_thread::sleep_for(std::chrono::milliseconds(50));
                }
                
            } catch (const std::exception& e) {
                std::cerr << "🚨 Overlay update error: " << e.what() << std::endl;
                std::this_thread::sleep_for(std::chrono::milliseconds(1000));
            }
        }
        
        std::cout << "🖼️  Overlay update loop ended" << std::endl;
    }
    
    void printSystemStatus() {
        std::cout << "\n" << std::string(60, '=') << std::endl;
        std::cout << "🏆 DSA-X GODMODE++ SYSTEM STATUS" << std::endl;
        std::cout << std::string(60, '=') << std::endl;
        std::cout << "🎵 Audio Capture: " << (audioCapture ? "✅ ENABLED" : "❌ DISABLED") << std::endl;
        std::cout << "🎤 STT Processor: " << (whisperProcessor ? "✅ ENABLED" : "❌ DISABLED") << std::endl;
        std::cout << "🧠 AI Engine: " << (classifier && generator ? "✅ ENABLED" : "❌ DISABLED") << std::endl;
        std::cout << "🖼️  GPU Overlay: " << (overlay ? "✅ ENABLED" : "❌ DISABLED") << std::endl;
        std::cout << "🥷 Stealth Mode: " << (stealthSystem ? "✅ ENABLED" : "❌ DISABLED") << std::endl;
        std::cout << "🔄 Self-Healing: " << (healingSystem ? "✅ ENABLED" : "❌ DISABLED") << std::endl;
        std::cout << "📊 Confidence Threshold: " << (config.confidenceThreshold * 100) << "%" << std::endl;
        std::cout << std::string(60, '=') << "\n" << std::endl;
    }
    
    void printFinalStatistics() {
        std::cout << "\n" << std::string(60, '=') << std::endl;
        std::cout << "📊 FINAL PERFORMANCE STATISTICS" << std::endl;
        std::cout << std::string(60, '=') << std::endl;
        std::cout << "Total Questions Processed: " << metrics.totalQuestions << std::endl;
        std::cout << "Successful Responses: " << metrics.successfulResponses << std::endl;
        std::cout << "Success Rate: " << std::fixed << std::setprecision(1) << metrics.successRate << "%" << std::endl;
        std::cout << "Average Audio Latency: " << metrics.audioLatency.count() << "ms" << std::endl;
        std::cout << "Average STT Latency: " << metrics.sttLatency.count() << "ms" << std::endl;
        std::cout << "Average AI Latency: " << metrics.aiLatency.count() << "ms" << std::endl;
        std::cout << "Average Total Latency: " << metrics.totalLatency.count() << "ms" << std::endl;
        std::cout << std::string(60, '=') << "\n" << std::endl;
    }
};