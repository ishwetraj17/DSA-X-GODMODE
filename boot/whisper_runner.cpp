/*
 * DSA-X GODMODE++: Ultra-Stealth AI Assistant
 * Whisper.cpp Integration for RAM-Only STT Processing
 * 
 * Implemented by Shwet Raj
 * Debug checkpoint: Whisper model loading and inference
 */

#include <whisper.h>
#include <iostream>
#include <vector>
#include <string>
#include <thread>
#include <atomic>
#include <queue>
#include <mutex>
#include <condition_variable>
#include <memory>
#include <cstring>

class WhisperRunner {
private:
    struct whisper_context* ctx;
    std::atomic<bool> isRunning;
    std::atomic<bool> isProcessing;
    std::thread whisperThread;
    std::queue<std::vector<float>> audioQueue;
    std::queue<std::string> transcriptionQueue;
    std::mutex audioMutex;
    std::mutex transcriptionMutex;
    std::condition_variable audioCondition;
    
    // Whisper model parameters
    whisper_full_params params;
    
    // Confidence threshold for transcription
    float confidenceThreshold;
    
    // Model data (embedded or loaded)
    std::vector<uint8_t> modelData;
    
public:
    WhisperRunner() : ctx(nullptr), isRunning(false), isProcessing(false), confidenceThreshold(0.7f) {
        // Initialize whisper parameters with optimal settings for real-time processing
        params = whisper_full_default_params(WHISPER_SAMPLING_GREEDY);
        params.strategy = WHISPER_SAMPLING_GREEDY;
        params.n_threads = std::min(4, (int)std::thread::hardware_concurrency());
        params.n_max_text_ctx = 16384;
        params.offset_ms = 0;
        params.duration_ms = 0;
        params.translate = false;
        params.no_context = true;
        params.single_segment = false;
        params.print_realtime = false;
        params.print_progress = false;
        params.print_timestamps = false;
        params.print_special = false;
        params.suppress_blank = true;
        params.suppress_non_speech_tokens = true;
        params.temperature = 0.0f;
        params.max_initial_ts = 1.0f;
        params.length_penalty = -1.0f;
        params.temperature_inc = 0.2f;
        params.entropy_thold = 2.4f;
        params.logprob_thold = -1.0f;
        params.no_speech_thold = 0.6f;
        
        // Set language to English for better performance
        params.language = "en";
    }
    
    ~WhisperRunner() {
        stop();
        if (ctx) {
            whisper_free(ctx);
        }
    }
    
    bool initialize() {
        // Load whisper model into RAM (using base model for speed/memory balance)
        if (!loadModelFromMemory()) {
            std::cerr << "Failed to load Whisper model" << std::endl;
            return false;
        }
        
        // Initialize whisper context
        ctx = whisper_init_from_buffer(modelData.data(), modelData.size());
        if (!ctx) {
            std::cerr << "Failed to initialize Whisper context" << std::endl;
            return false;
        }
        
        std::cout << "✅ Whisper.cpp initialized successfully" << std::endl;
        std::cout << "   Model: " << whisper_print_system_info() << std::endl;
        return true;
    }
    
    void start() {
        if (!isRunning.load()) {
            isRunning = true;
            whisperThread = std::thread(&WhisperRunner::processAudioQueue, this);
            std::cout << "🎤 Whisper STT processing started" << std::endl;
        }
    }
    
    void stop() {
        if (isRunning.load()) {
            isRunning = false;
            audioCondition.notify_all();
            
            if (whisperThread.joinable()) {
                whisperThread.join();
            }
            
            std::cout << "🛑 Whisper STT processing stopped" << std::endl;
        }
    }
    
    void addAudioData(const std::vector<float>& audioData) {
        if (!audioData.empty() && isRunning.load()) {
            std::lock_guard<std::mutex> lock(audioMutex);
            audioQueue.push(audioData);
            audioCondition.notify_one();
        }
    }
    
    std::string getTranscription() {
        std::lock_guard<std::mutex> lock(transcriptionMutex);
        if (!transcriptionQueue.empty()) {
            std::string result = transcriptionQueue.front();
            transcriptionQueue.pop();
            return result;
        }
        return "";
    }
    
    bool hasTranscription() const {
        std::lock_guard<std::mutex> lock(transcriptionMutex);
        return !transcriptionQueue.empty();
    }
    
    bool isProcessingAudio() const {
        return isProcessing.load();
    }
    
    void setConfidenceThreshold(float threshold) {
        confidenceThreshold = std::max(0.0f, std::min(1.0f, threshold));
    }

private:
    bool loadModelFromMemory() {
        // In a real implementation, you would either:
        // 1. Embed the model as a resource
        // 2. Download it at runtime
        // 3. Load from a bundled file
        
        // For this demo, we'll simulate loading a base model
        // In production, you'd want to bundle the actual GGUF model file
        
        std::cout << "📥 Loading Whisper base model..." << std::endl;
        
        // Try to load from common model paths
        std::vector<std::string> modelPaths = {
            "models/ggml-base.bin",
            "models/ggml-base.en.bin", 
            "../models/ggml-base.bin",
            "whisper-base.bin",
            "ggml-base.bin"
        };
        
        for (const auto& path : modelPaths) {
            if (loadModelFromFile(path)) {
                std::cout << "✅ Loaded model from: " << path << std::endl;
                return true;
            }
        }
        
        // If no model found, create a placeholder that indicates missing model
        std::cerr << "⚠️  No Whisper model found. Please place a model file in one of:" << std::endl;
        for (const auto& path : modelPaths) {
            std::cerr << "   " << path << std::endl;
        }
        std::cerr << "   Download from: https://huggingface.co/ggerganov/whisper.cpp" << std::endl;
        
        return false;
    }
    
    bool loadModelFromFile(const std::string& path) {
        FILE* file = fopen(path.c_str(), "rb");
        if (!file) {
            return false;
        }
        
        // Get file size
        fseek(file, 0, SEEK_END);
        size_t fileSize = ftell(file);
        fseek(file, 0, SEEK_SET);
        
        if (fileSize == 0) {
            fclose(file);
            return false;
        }
        
        // Load model data into memory
        modelData.resize(fileSize);
        size_t bytesRead = fread(modelData.data(), 1, fileSize, file);
        fclose(file);
        
        return bytesRead == fileSize;
    }
    
    void processAudioQueue() {
        while (isRunning.load()) {
            std::unique_lock<std::mutex> lock(audioMutex);
            audioCondition.wait(lock, [this] { return !audioQueue.empty() || !isRunning.load(); });
            
            if (!isRunning.load()) break;
            
            if (!audioQueue.empty()) {
                std::vector<float> audioData = audioQueue.front();
                audioQueue.pop();
                lock.unlock();
                
                // Process audio chunk
                processAudioChunk(audioData);
            }
        }
    }
    
    void processAudioChunk(const std::vector<float>& audioData) {
        if (!ctx || audioData.empty()) return;
        
        isProcessing = true;
        
        // Ensure audio data is the right size for processing
        const size_t minSamples = 1600; // 0.1 seconds at 16kHz
        if (audioData.size() < minSamples) {
            isProcessing = false;
            return;
        }
        
        // Process audio with Whisper
        int result = whisper_full(ctx, params, audioData.data(), (int)audioData.size());
        
        if (result == 0) {
            // Extract transcription
            const int n_segments = whisper_full_n_segments(ctx);
            std::string fullTranscription;
            
            for (int i = 0; i < n_segments; ++i) {
                const char* text = whisper_full_get_segment_text(ctx, i);
                
                // Get confidence score (probability)
                const float confidence = std::exp(whisper_full_get_segment_p(ctx, i));
                
                // Only add text that meets confidence threshold
                if (confidence >= confidenceThreshold && text && strlen(text) > 0) {
                    std::string segmentText = text;
                    
                    // Clean up text
                    segmentText = cleanTranscriptionText(segmentText);
                    
                    if (!segmentText.empty()) {
                        if (!fullTranscription.empty()) {
                            fullTranscription += " ";
                        }
                        fullTranscription += segmentText;
                    }
                }
            }
            
            // Add to transcription queue if we have meaningful text
            if (!fullTranscription.empty() && fullTranscription.length() > 2) {
                std::lock_guard<std::mutex> lock(transcriptionMutex);
                transcriptionQueue.push(fullTranscription);
                
                // Keep queue size manageable
                while (transcriptionQueue.size() > 10) {
                    transcriptionQueue.pop();
                }
                
                std::cout << "🎯 Transcribed: " << fullTranscription << std::endl;
            }
        } else {
            std::cerr << "Whisper processing failed with code: " << result << std::endl;
        }
        
        isProcessing = false;
    }
    
    std::string cleanTranscriptionText(const std::string& text) {
        std::string cleaned = text;
        
        // Remove leading/trailing whitespace
        size_t start = cleaned.find_first_not_of(" \t\n\r");
        if (start == std::string::npos) return "";
        size_t end = cleaned.find_last_not_of(" \t\n\r");
        cleaned = cleaned.substr(start, end - start + 1);
        
        // Remove common STT artifacts
        if (cleaned == "." || cleaned == "," || cleaned == "?" || cleaned == "!" ||
            cleaned == "the" || cleaned == "a" || cleaned == "an" ||
            cleaned.length() < 2) {
            return "";
        }
        
        // Convert to lowercase for consistency
        std::transform(cleaned.begin(), cleaned.end(), cleaned.begin(), ::tolower);
        
        return cleaned;
    }
    
    static void whisperCallback(struct whisper_context* ctx, 
                               struct whisper_state* state, 
                               int n_new, 
                               void* user_data) {
        // Real-time callback for streaming (optional)
        // Can be used for live transcription updates
    }
};