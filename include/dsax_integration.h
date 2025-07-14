/*
 * DSA-X GODMODE++: Ultra-Stealth AI Assistant
 * System Integration Header
 * 
 * Implemented by Shwet Raj
 * Debug checkpoint: Component integration and API definitions
 */

#pragma once

#include <string>
#include <vector>
#include <memory>
#include <functional>
#include <atomic>
#include <mutex>
#include <map>

// Forward declarations
class DSAXController;
class StealthEnforcer;
class SelfHealingSystem;

// Audio capture interfaces
namespace AudioCapture {
    struct AudioConfig {
        int sampleRate = 16000;
        int channels = 1;
        int bufferSize = 4096;
        std::string deviceName;
        bool enableVAD = true;
        float vadThreshold = 0.01f;
    };
    
    class IAudioCapture {
    public:
        virtual ~IAudioCapture() = default;
        virtual bool initialize(const AudioConfig& config) = 0;
        virtual bool startCapture() = 0;
        virtual void stopCapture() = 0;
        virtual bool isCapturing() const = 0;
        virtual std::vector<float> getLatestAudio() = 0;
        virtual void cleanup() = 0;
    };
    
#ifdef __APPLE__
    class MacAudioCapture : public IAudioCapture {
    public:
        bool initialize(const AudioConfig& config) override;
        bool startCapture() override;
        void stopCapture() override;
        bool isCapturing() const override;
        std::vector<float> getLatestAudio() override;
        void cleanup() override;
    };
#endif
    
#ifdef _WIN32
    class WindowsAudioCapture : public IAudioCapture {
    public:
        bool initialize(const AudioConfig& config) override;
        bool startCapture() override;
        void stopCapture() override;
        bool isCapturing() const override;
        std::vector<float> getLatestAudio() override;
        void cleanup() override;
    };
#endif
}

// Speech-to-text interfaces
namespace SpeechToText {
    struct TranscriptionResult {
        std::string text;
        float confidence;
        std::chrono::steady_clock::time_point timestamp;
        bool isPartial;
    };
    
    struct WhisperConfig {
        std::string modelPath;
        std::string language = "en";
        int numThreads = 4;
        bool enableTimestamps = false;
        float vadThreshold = 0.6f;
        bool enableTranslation = false;
    };
    
    class IWhisperEngine {
    public:
        virtual ~IWhisperEngine() = default;
        virtual bool initialize(const WhisperConfig& config) = 0;
        virtual TranscriptionResult processAudio(const std::vector<float>& audioData) = 0;
        virtual bool isProcessing() const = 0;
        virtual void cleanup() = 0;
    };
    
    class WhisperRunner : public IWhisperEngine {
    public:
        bool initialize(const WhisperConfig& config) override;
        TranscriptionResult processAudio(const std::vector<float>& audioData) override;
        bool isProcessing() const override;
        void cleanup() override;
    };
}

// LLM processing interfaces
namespace LLMProcessing {
    enum class QuestionType {
        UNKNOWN = 0,
        DSA_ARRAY,
        DSA_LINKED_LIST,
        DSA_TREE,
        DSA_GRAPH,
        DSA_DYNAMIC_PROGRAMMING,
        DSA_SORTING,
        DSA_SEARCHING,
        SYSTEM_DESIGN,
        BEHAVIORAL_STAR,
        OOP_DESIGN,
        OS_CONCEPTS,
        DBMS_CONCEPTS,
        NETWORKING,
        CODING_GENERAL
    };
    
    enum class ProgrammingLanguage {
        UNKNOWN = 0,
        JAVA,
        CPP,
        PYTHON,
        JAVASCRIPT,
        CSHARP,
        GO,
        RUST
    };
    
    struct ClassificationResult {
        QuestionType questionType;
        ProgrammingLanguage language;
        float confidence;
        std::vector<std::string> keywords;
        std::string questionText;
    };
    
    struct AnswerResult {
        std::string answer;
        std::string explanation;
        std::string codeExample;
        std::string timeComplexity;
        std::string spaceComplexity;
        std::vector<std::string> hints;
        float confidence;
    };
    
    class IPromptClassifier {
    public:
        virtual ~IPromptClassifier() = default;
        virtual bool initialize() = 0;
        virtual ClassificationResult classifyQuestion(const std::string& question) = 0;
        virtual void updatePatterns() = 0;
        virtual void cleanup() = 0;
    };
    
    class IAnswerGenerator {
    public:
        virtual ~IAnswerGenerator() = default;
        virtual bool initialize() = 0;
        virtual AnswerResult generateAnswer(const ClassificationResult& classification) = 0;
        virtual void updateTemplates() = 0;
        virtual void cleanup() = 0;
    };
    
    class PromptClassifier : public IPromptClassifier {
    public:
        bool initialize() override;
        ClassificationResult classifyQuestion(const std::string& question) override;
        void updatePatterns() override;
        void cleanup() override;
    };
    
    class AnswerGenerator : public IAnswerGenerator {
    public:
        bool initialize() override;
        AnswerResult generateAnswer(const ClassificationResult& classification) override;
        void updateTemplates() override;
        void cleanup() override;
    };
}

// Overlay system interfaces
namespace OverlaySystem {
    struct OverlayConfig {
        bool enableGPURendering = true;
        bool enableScreenShareInvisibility = true;
        int fadeInMs = 500;
        int fadeOutMs = 300;
        float opacity = 0.8f;
        std::string fontFamily = "Consolas";
        int fontSize = 14;
    };
    
    class IOverlay {
    public:
        virtual ~IOverlay() = default;
        virtual bool initialize(const OverlayConfig& config) = 0;
        virtual void updateDisplay(const std::string& text) = 0;
        virtual void show() = 0;
        virtual void hide() = 0;
        virtual bool isVisible() const = 0;
        virtual void cleanup() = 0;
    };
    
#ifdef __APPLE__
    // Forward declaration for Objective-C++ wrapper
    class StealthOverlayWindow_CPP;
    
    class MacOverlay : public IOverlay {
    private:
        std::unique_ptr<StealthOverlayWindow_CPP> overlay;
    public:
        bool initialize(const OverlayConfig& config) override;
        void updateDisplay(const std::string& text) override;
        void show() override;
        void hide() override;
        bool isVisible() const override;
        void cleanup() override;
    };
#endif
    
#ifdef _WIN32
    class WindowsOverlay : public IOverlay {
    public:
        bool initialize(const OverlayConfig& config) override;
        void updateDisplay(const std::string& text) override;
        void show() override;
        void hide() override;
        bool isVisible() const override;
        void cleanup() override;
    };
#endif
}

// Stealth system interfaces
namespace StealthSystem {
    struct StealthConfig {
        bool enableProcessCloaking = true;
        bool enableAntiDebugging = true;
        bool enableAntiScreenCapture = true;
        bool enableMemoryProtection = true;
        int scanIntervalMs = 1000;
        int maxEvasionAttempts = 3;
    };
    
    struct StealthMetrics {
        uint64_t threatsDetected;
        uint64_t evasionsPerformed;
        uint64_t healthChecks;
        uint64_t successfulRecoveries;
        double systemHealthScore;
    };
    
    class IStealthEnforcer {
    public:
        virtual ~IStealthEnforcer() = default;
        virtual bool initialize(const StealthConfig& config) = 0;
        virtual void start() = 0;
        virtual void stop() = 0;
        virtual bool isActive() const = 0;
        virtual StealthMetrics getMetrics() const = 0;
        virtual void forceStealthCheck() = 0;
    };
    
    class ISelfHealing {
    public:
        virtual ~ISelfHealing() = default;
        virtual bool initialize() = 0;
        virtual void registerComponent(const std::string& name) = 0;
        virtual void updateComponentStatus(const std::string& name, int status) = 0;
        virtual bool performSystemRecovery() = 0;
        virtual void createSystemBackup() = 0;
        virtual void start() = 0;
        virtual void stop() = 0;
    };
}

// Main system controller
namespace DSAXSystem {
    enum class SystemState {
        UNINITIALIZED = 0,
        INITIALIZING,
        READY,
        ACTIVE,
        DEGRADED,
        ERROR,
        SHUTTING_DOWN
    };
    
    struct SystemConfig {
        // Audio configuration
        AudioCapture::AudioConfig audioConfig;
        
        // STT configuration
        SpeechToText::WhisperConfig whisperConfig;
        
        // Overlay configuration
        OverlaySystem::OverlayConfig overlayConfig;
        
        // Stealth configuration
        StealthSystem::StealthConfig stealthConfig;
        
        // General settings
        bool enableFallbackSystems = true;
        bool enableLogging = false;
        bool enableMetrics = true;
        std::string logLevel = "INFO";
    };
    
    struct SystemMetrics {
        SystemState currentState;
        std::chrono::steady_clock::time_point startTime;
        uint64_t questionsProcessed;
        uint64_t answersGenerated;
        uint64_t audioFramesProcessed;
        double averageResponseTime;
        double systemCpuUsage;
        double systemMemoryUsage;
        StealthSystem::StealthMetrics stealthMetrics;
    };
    
    class IDSAXController {
    public:
        virtual ~IDSAXController() = default;
        virtual bool initialize(const SystemConfig& config) = 0;
        virtual bool start() = 0;
        virtual void stop() = 0;
        virtual SystemState getState() const = 0;
        virtual SystemMetrics getMetrics() const = 0;
        virtual void processQuestion(const std::string& question) = 0;
        virtual void enableComponent(const std::string& component, bool enable) = 0;
        virtual bool isComponentActive(const std::string& component) const = 0;
    };
    
    class DSAXController : public IDSAXController {
    private:
        std::unique_ptr<AudioCapture::IAudioCapture> audioCapture;
        std::unique_ptr<SpeechToText::IWhisperEngine> whisperEngine;
        std::unique_ptr<LLMProcessing::IPromptClassifier> promptClassifier;
        std::unique_ptr<LLMProcessing::IAnswerGenerator> answerGenerator;
        std::unique_ptr<OverlaySystem::IOverlay> overlay;
        std::unique_ptr<StealthSystem::IStealthEnforcer> stealthEnforcer;
        std::unique_ptr<StealthSystem::ISelfHealing> selfHealing;
        
        std::atomic<SystemState> currentState;
        SystemConfig config;
        SystemMetrics metrics;
        std::mutex systemMutex;
        
        // Processing thread
        std::thread processingThread;
        std::atomic<bool> shouldProcess;
        
    public:
        bool initialize(const SystemConfig& config) override;
        bool start() override;
        void stop() override;
        SystemState getState() const override;
        SystemMetrics getMetrics() const override;
        void processQuestion(const std::string& question) override;
        void enableComponent(const std::string& component, bool enable) override;
        bool isComponentActive(const std::string& component) const override;
        
    private:
        void processingLoop();
        bool initializeComponents();
        void cleanupComponents();
        void updateMetrics();
    };
}

// Factory functions for creating platform-specific implementations
namespace DSAXFactory {
    std::unique_ptr<AudioCapture::IAudioCapture> createAudioCapture();
    std::unique_ptr<SpeechToText::IWhisperEngine> createWhisperEngine();
    std::unique_ptr<LLMProcessing::IPromptClassifier> createPromptClassifier();
    std::unique_ptr<LLMProcessing::IAnswerGenerator> createAnswerGenerator();
    std::unique_ptr<OverlaySystem::IOverlay> createOverlay();
    std::unique_ptr<StealthSystem::IStealthEnforcer> createStealthEnforcer();
    std::unique_ptr<StealthSystem::ISelfHealing> createSelfHealing();
    std::unique_ptr<DSAXSystem::IDSAXController> createDSAXController();
}

// Utility functions
namespace DSAXUtils {
    std::string getSystemInfo();
    std::string getPlatformName();
    bool checkSystemRequirements();
    void setupLogging(const std::string& level);
    void cleanupLogging();
    
    // Memory management utilities
    void secureMemoryZero(void* ptr, size_t size);
    bool isDebuggerPresent();
    bool isScreenRecordingActive();
    
    // Timing utilities
    class HighResolutionTimer {
    public:
        void start();
        void stop();
        double getElapsedMs() const;
        double getElapsedUs() const;
    };
    
    // Configuration management
    class ConfigManager {
    public:
        bool loadConfig(const std::string& filename, DSAXSystem::SystemConfig& config);
        bool saveConfig(const std::string& filename, const DSAXSystem::SystemConfig& config);
        bool validateConfig(const DSAXSystem::SystemConfig& config);
    };
}