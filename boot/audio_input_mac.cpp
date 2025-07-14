/*
 * DSA-X GODMODE++: Ultra-Stealth AI Assistant
 * Audio Input Capture for macOS (BlackHole Integration)
 * 
 * Implemented by Shwet Raj
 * Debug checkpoint: BlackHole audio routing setup
 */

#include <AudioToolbox/AudioToolbox.h>
#include <CoreAudio/CoreAudio.h>
#include <iostream>
#include <vector>
#include <thread>
#include <atomic>
#include <mutex>

class MacAudioCapture {
private:
    AudioUnit audioUnit;
    std::atomic<bool> isRunning;
    std::vector<float> audioBuffer;
    std::mutex bufferMutex;
    
    // BlackHole device ID (will be auto-detected)
    AudioDeviceID blackholeDevice;
    
    // Audio format configuration
    AudioStreamBasicDescription audioFormat;
    
public:
    MacAudioCapture() : isRunning(false), blackholeDevice(kAudioObjectUnknown) {
        memset(&audioFormat, 0, sizeof(audioFormat));
        audioFormat.mSampleRate = 16000.0;  // 16kHz for Whisper
        audioFormat.mFormatID = kAudioFormatLinearPCM;
        audioFormat.mFormatFlags = kAudioFormatFlagIsFloat | kAudioFormatFlagIsPacked;
        audioFormat.mChannelsPerFrame = 1;  // Mono
        audioFormat.mBitsPerChannel = 32;
        audioFormat.mBytesPerFrame = 4;
        audioFormat.mBytesPerPacket = 4;
        audioFormat.mFramesPerPacket = 1;
    }
    
    ~MacAudioCapture() {
        stop();
        if (audioUnit) {
            AudioUnitUninitialize(audioUnit);
            AudioComponentInstanceDispose(audioUnit);
        }
    }
    
    bool initialize() {
        // Find BlackHole device
        if (!findBlackHoleDevice()) {
            std::cerr << "BlackHole device not found. Please install BlackHole." << std::endl;
            return false;
        }
        
        // Create audio unit
        AudioComponentDescription desc;
        desc.componentType = kAudioUnitType_Output;
        desc.componentSubType = kAudioUnitSubType_HALOutput;
        desc.componentManufacturer = kAudioUnitManufacturer_Apple;
        desc.componentFlags = 0;
        desc.componentFlagsMask = 0;
        
        AudioComponent component = AudioComponentFindNext(nullptr, &desc);
        if (!component) {
            std::cerr << "Failed to find audio component" << std::endl;
            return false;
        }
        
        OSStatus status = AudioComponentInstanceNew(component, &audioUnit);
        if (status != noErr) {
            std::cerr << "Failed to create audio unit: " << status << std::endl;
            return false;
        }
        
        // Enable input on the audio unit
        UInt32 enableInput = 1;
        status = AudioUnitSetProperty(audioUnit, kAudioOutputUnitProperty_EnableIO,
                                    kAudioUnitScope_Input, 1, &enableInput, sizeof(enableInput));
        if (status != noErr) {
            std::cerr << "Failed to enable input: " << status << std::endl;
            return false;
        }
        
        // Set the input device to BlackHole
        status = AudioUnitSetProperty(audioUnit, kAudioOutputUnitProperty_CurrentDevice,
                                    kAudioUnitScope_Global, 0, &blackholeDevice, sizeof(blackholeDevice));
        if (status != noErr) {
            std::cerr << "Failed to set BlackHole device: " << status << std::endl;
            return false;
        }
        
        // Set input audio format
        status = AudioUnitSetProperty(audioUnit, kAudioUnitProperty_StreamFormat,
                                    kAudioUnitScope_Output, 1, &audioFormat, sizeof(audioFormat));
        if (status != noErr) {
            std::cerr << "Failed to set audio format: " << status << std::endl;
            return false;
        }
        
        // Set up input callback
        AURenderCallbackStruct callbackStruct;
        callbackStruct.inputProc = audioCallback;
        callbackStruct.inputProcRefCon = this;
        
        status = AudioUnitSetProperty(audioUnit, kAudioOutputUnitProperty_SetInputCallback,
                                    kAudioUnitScope_Global, 0, &callbackStruct, sizeof(callbackStruct));
        if (status != noErr) {
            std::cerr << "Failed to set input callback: " << status << std::endl;
            return false;
        }
        
        // Initialize the audio unit
        status = AudioUnitInitialize(audioUnit);
        if (status != noErr) {
            std::cerr << "Failed to initialize audio unit: " << status << std::endl;
            return false;
        }
        
        std::cout << "✅ BlackHole audio capture initialized successfully" << std::endl;
        return true;
    }
    
    void start() {
        if (!isRunning.load()) {
            isRunning = true;
            OSStatus status = AudioOutputUnitStart(audioUnit);
            if (status == noErr) {
                std::cout << "🎵 BlackHole audio capture started" << std::endl;
            } else {
                std::cerr << "Failed to start audio capture: " << status << std::endl;
                isRunning = false;
            }
        }
    }
    
    void stop() {
        if (isRunning.load()) {
            isRunning = false;
            AudioOutputUnitStop(audioUnit);
            std::cout << "🛑 BlackHole audio capture stopped" << std::endl;
        }
    }
    
    std::vector<float> getAudioData() {
        std::lock_guard<std::mutex> lock(bufferMutex);
        std::vector<float> data = audioBuffer;
        audioBuffer.clear();
        return data;
    }
    
    bool isCapturing() const {
        return isRunning.load();
    }

private:
    bool findBlackHoleDevice() {
        UInt32 propertySize;
        AudioObjectPropertyAddress propertyAddress = {
            kAudioHardwarePropertyDevices,
            kAudioObjectPropertyScopeGlobal,
            kAudioObjectPropertyElementMain
        };
        
        // Get number of devices
        OSStatus status = AudioObjectGetPropertyDataSize(kAudioObjectSystemObject,
                                                        &propertyAddress, 0, nullptr, &propertySize);
        if (status != noErr) return false;
        
        UInt32 deviceCount = propertySize / sizeof(AudioDeviceID);
        std::vector<AudioDeviceID> devices(deviceCount);
        
        // Get device list
        status = AudioObjectGetPropertyData(kAudioObjectSystemObject, &propertyAddress,
                                          0, nullptr, &propertySize, devices.data());
        if (status != noErr) return false;
        
        // Find BlackHole device
        for (const auto& deviceId : devices) {
            CFStringRef deviceName = nullptr;
            propertySize = sizeof(deviceName);
            
            AudioObjectPropertyAddress nameAddress = {
                kAudioDevicePropertyDeviceNameCFString,
                kAudioObjectPropertyScopeGlobal,
                kAudioObjectPropertyElementMain
            };
            
            status = AudioObjectGetPropertyData(deviceId, &nameAddress, 0, nullptr,
                                              &propertySize, &deviceName);
            if (status == noErr && deviceName) {
                char name[256];
                CFStringGetCString(deviceName, name, sizeof(name), kCFStringEncodingUTF8);
                CFRelease(deviceName);
                
                if (strstr(name, "BlackHole")) {
                    blackholeDevice = deviceId;
                    std::cout << "🎯 Found BlackHole device: " << name << std::endl;
                    return true;
                }
            }
        }
        
        return false;
    }
    
    static OSStatus audioCallback(void* inRefCon, 
                                AudioUnitRenderActionFlags* ioActionFlags,
                                const AudioTimeStamp* inTimeStamp,
                                UInt32 inBusNumber,
                                UInt32 inNumberFrames,
                                AudioBufferList* ioData) {
        
        MacAudioCapture* capture = static_cast<MacAudioCapture*>(inRefCon);
        
        // Allocate buffer for input
        AudioBufferList bufferList;
        bufferList.mNumberBuffers = 1;
        bufferList.mBuffers[0].mNumberChannels = 1;
        bufferList.mBuffers[0].mDataByteSize = inNumberFrames * sizeof(float);
        
        std::vector<float> tempBuffer(inNumberFrames);
        bufferList.mBuffers[0].mData = tempBuffer.data();
        
        // Render input audio
        OSStatus status = AudioUnitRender(capture->audioUnit, ioActionFlags, inTimeStamp,
                                        inBusNumber, inNumberFrames, &bufferList);
        
        if (status == noErr && capture->isRunning.load()) {
            // Add audio data to buffer
            std::lock_guard<std::mutex> lock(capture->bufferMutex);
            capture->audioBuffer.insert(capture->audioBuffer.end(), 
                                      tempBuffer.begin(), tempBuffer.end());
            
            // Keep buffer size manageable (5 seconds max)
            const size_t maxBufferSize = 16000 * 5; // 5 seconds at 16kHz
            if (capture->audioBuffer.size() > maxBufferSize) {
                capture->audioBuffer.erase(capture->audioBuffer.begin(),
                                         capture->audioBuffer.begin() + (capture->audioBuffer.size() - maxBufferSize));
            }
        }
        
        return status;
    }
};