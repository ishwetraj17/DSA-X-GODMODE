/*
 * DSA-X GODMODE++: Ultra-Stealth AI Assistant
 * Audio Input Capture for Windows (VB-Audio Cable Integration)
 * 
 * Implemented by Shwet Raj
 * Debug checkpoint: VB-Audio Cable integration setup
 */

#include <windows.h>
#include <mmdeviceapi.h>
#include <audioclient.h>
#include <audiopolicy.h>
#include <functiondiscoverykeys_devpkey.h>
#include <iostream>
#include <vector>
#include <thread>
#include <atomic>
#include <mutex>
#include <string>

#pragma comment(lib, "ole32.lib")

const CLSID CLSID_MMDeviceEnumerator = __uuidof(MMDeviceEnumerator);
const IID IID_IMMDeviceEnumerator = __uuidof(IMMDeviceEnumerator);
const IID IID_IAudioClient = __uuidof(IAudioClient);
const IID IID_IAudioCaptureClient = __uuidof(IAudioCaptureClient);

class WindowsAudioCapture {
private:
    IMMDeviceEnumerator* deviceEnumerator;
    IMMDevice* audioDevice;
    IAudioClient* audioClient;
    IAudioCaptureClient* captureClient;
    
    std::atomic<bool> isRunning;
    std::thread captureThread;
    std::vector<float> audioBuffer;
    std::mutex bufferMutex;
    
    std::wstring vbCableDeviceId;
    WAVEFORMATEX* audioFormat;
    
    // Buffer properties
    UINT32 bufferFrameCount;
    REFERENCE_TIME defaultDevicePeriod;
    
public:
    WindowsAudioCapture() : 
        deviceEnumerator(nullptr), 
        audioDevice(nullptr),
        audioClient(nullptr), 
        captureClient(nullptr),
        isRunning(false),
        audioFormat(nullptr),
        bufferFrameCount(0),
        defaultDevicePeriod(0) {
        
        // Initialize COM
        CoInitializeEx(nullptr, COINIT_MULTITHREADED);
    }
    
    ~WindowsAudioCapture() {
        stop();
        cleanup();
        CoUninitialize();
    }
    
    bool initialize() {
        HRESULT hr;
        
        // Create device enumerator
        hr = CoCreateInstance(CLSID_MMDeviceEnumerator, nullptr, CLSCTX_ALL,
                            IID_IMMDeviceEnumerator, (void**)&deviceEnumerator);
        if (FAILED(hr)) {
            std::cerr << "Failed to create device enumerator: " << std::hex << hr << std::endl;
            return false;
        }
        
        // Find VB-Audio Cable device
        if (!findVBCableDevice()) {
            std::cerr << "VB-Audio Cable not found. Please install VB-Audio Cable." << std::endl;
            return false;
        }
        
        // Get the audio device
        hr = deviceEnumerator->GetDevice(vbCableDeviceId.c_str(), &audioDevice);
        if (FAILED(hr)) {
            std::cerr << "Failed to get VB-Audio Cable device: " << std::hex << hr << std::endl;
            return false;
        }
        
        // Activate the audio client
        hr = audioDevice->Activate(IID_IAudioClient, CLSCTX_ALL, nullptr, (void**)&audioClient);
        if (FAILED(hr)) {
            std::cerr << "Failed to activate audio client: " << std::hex << hr << std::endl;
            return false;
        }
        
        // Get the audio format
        hr = audioClient->GetMixFormat(&audioFormat);
        if (FAILED(hr)) {
            std::cerr << "Failed to get audio format: " << std::hex << hr << std::endl;
            return false;
        }
        
        // Modify format for Whisper requirements (16kHz, mono, float)
        audioFormat->wFormatTag = WAVE_FORMAT_IEEE_FLOAT;
        audioFormat->nSamplesPerSec = 16000;
        audioFormat->nChannels = 1;
        audioFormat->wBitsPerSample = 32;
        audioFormat->nBlockAlign = audioFormat->nChannels * (audioFormat->wBitsPerSample / 8);
        audioFormat->nAvgBytesPerSec = audioFormat->nSamplesPerSec * audioFormat->nBlockAlign;
        audioFormat->cbSize = 0;
        
        // Initialize the audio client
        hr = audioClient->Initialize(AUDCLNT_SHAREMODE_SHARED,
                                   AUDCLNT_STREAMFLAGS_LOOPBACK,
                                   10000000,  // 1 second buffer
                                   0,
                                   audioFormat,
                                   nullptr);
        if (FAILED(hr)) {
            std::cerr << "Failed to initialize audio client: " << std::hex << hr << std::endl;
            return false;
        }
        
        // Get buffer frame count
        hr = audioClient->GetBufferSize(&bufferFrameCount);
        if (FAILED(hr)) {
            std::cerr << "Failed to get buffer size: " << std::hex << hr << std::endl;
            return false;
        }
        
        // Get the capture client
        hr = audioClient->GetService(IID_IAudioCaptureClient, (void**)&captureClient);
        if (FAILED(hr)) {
            std::cerr << "Failed to get capture client: " << std::hex << hr << std::endl;
            return false;
        }
        
        std::cout << "✅ VB-Audio Cable capture initialized successfully" << std::endl;
        return true;
    }
    
    void start() {
        if (!isRunning.load()) {
            isRunning = true;
            
            HRESULT hr = audioClient->Start();
            if (SUCCEEDED(hr)) {
                captureThread = std::thread(&WindowsAudioCapture::captureLoop, this);
                std::cout << "🎵 VB-Audio Cable capture started" << std::endl;
            } else {
                std::cerr << "Failed to start audio capture: " << std::hex << hr << std::endl;
                isRunning = false;
            }
        }
    }
    
    void stop() {
        if (isRunning.load()) {
            isRunning = false;
            
            if (captureThread.joinable()) {
                captureThread.join();
            }
            
            if (audioClient) {
                audioClient->Stop();
            }
            
            std::cout << "🛑 VB-Audio Cable capture stopped" << std::endl;
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
    bool findVBCableDevice() {
        HRESULT hr;
        IMMDeviceCollection* deviceCollection = nullptr;
        
        // Enumerate audio devices
        hr = deviceEnumerator->EnumAudioEndpoints(eRender, DEVICE_STATE_ACTIVE, &deviceCollection);
        if (FAILED(hr)) {
            std::cerr << "Failed to enumerate audio endpoints: " << std::hex << hr << std::endl;
            return false;
        }
        
        UINT deviceCount;
        hr = deviceCollection->GetCount(&deviceCount);
        if (FAILED(hr)) {
            deviceCollection->Release();
            return false;
        }
        
        // Search for VB-Audio Cable
        for (UINT i = 0; i < deviceCount; i++) {
            IMMDevice* device = nullptr;
            hr = deviceCollection->Item(i, &device);
            if (FAILED(hr)) continue;
            
            // Get device ID
            LPWSTR deviceId = nullptr;
            hr = device->GetId(&deviceId);
            if (FAILED(hr)) {
                device->Release();
                continue;
            }
            
            // Get device properties
            IPropertyStore* propertyStore = nullptr;
            hr = device->OpenPropertyStore(STGM_READ, &propertyStore);
            if (SUCCEEDED(hr)) {
                PROPVARIANT variantName;
                PropVariantInit(&variantName);
                
                hr = propertyStore->GetValue(PKEY_Device_FriendlyName, &variantName);
                if (SUCCEEDED(hr)) {
                    std::wstring deviceName = variantName.pwszVal;
                    
                    // Check if this is VB-Audio Cable
                    if (deviceName.find(L"CABLE") != std::wstring::npos ||
                        deviceName.find(L"VB-Audio") != std::wstring::npos) {
                        vbCableDeviceId = deviceId;
                        
                        // Convert to narrow string for console output
                        std::string narrowName(deviceName.begin(), deviceName.end());
                        std::cout << "🎯 Found VB-Audio Cable: " << narrowName << std::endl;
                        
                        PropVariantClear(&variantName);
                        propertyStore->Release();
                        device->Release();
                        CoTaskMemFree(deviceId);
                        deviceCollection->Release();
                        return true;
                    }
                }
                
                PropVariantClear(&variantName);
                propertyStore->Release();
            }
            
            device->Release();
            CoTaskMemFree(deviceId);
        }
        
        deviceCollection->Release();
        return false;
    }
    
    void captureLoop() {
        HRESULT hr;
        UINT32 packetLength = 0;
        
        while (isRunning.load()) {
            Sleep(10); // Small delay to prevent excessive CPU usage
            
            hr = captureClient->GetNextPacketSize(&packetLength);
            if (FAILED(hr)) {
                std::cerr << "Failed to get packet size: " << std::hex << hr << std::endl;
                break;
            }
            
            while (packetLength != 0) {
                BYTE* audioData = nullptr;
                UINT32 framesAvailable = 0;
                DWORD flags = 0;
                
                hr = captureClient->GetBuffer(&audioData, &framesAvailable, &flags, nullptr, nullptr);
                if (FAILED(hr)) {
                    std::cerr << "Failed to get buffer: " << std::hex << hr << std::endl;
                    break;
                }
                
                if (!(flags & AUDCLNT_BUFFERFLAGS_SILENT)) {
                    // Process audio data
                    float* floatData = reinterpret_cast<float*>(audioData);
                    size_t sampleCount = framesAvailable * audioFormat->nChannels;
                    
                    // Convert to mono if needed and add to buffer
                    std::lock_guard<std::mutex> lock(bufferMutex);
                    
                    if (audioFormat->nChannels == 1) {
                        // Already mono
                        audioBuffer.insert(audioBuffer.end(), floatData, floatData + sampleCount);
                    } else {
                        // Convert to mono by averaging channels
                        for (UINT32 frame = 0; frame < framesAvailable; frame++) {
                            float monoSample = 0.0f;
                            for (UINT32 channel = 0; channel < audioFormat->nChannels; channel++) {
                                monoSample += floatData[frame * audioFormat->nChannels + channel];
                            }
                            audioBuffer.push_back(monoSample / audioFormat->nChannels);
                        }
                    }
                    
                    // Keep buffer size manageable (5 seconds max)
                    const size_t maxBufferSize = 16000 * 5; // 5 seconds at 16kHz
                    if (audioBuffer.size() > maxBufferSize) {
                        audioBuffer.erase(audioBuffer.begin(),
                                        audioBuffer.begin() + (audioBuffer.size() - maxBufferSize));
                    }
                }
                
                hr = captureClient->ReleaseBuffer(framesAvailable);
                if (FAILED(hr)) {
                    std::cerr << "Failed to release buffer: " << std::hex << hr << std::endl;
                    break;
                }
                
                hr = captureClient->GetNextPacketSize(&packetLength);
                if (FAILED(hr)) {
                    std::cerr << "Failed to get next packet size: " << std::hex << hr << std::endl;
                    break;
                }
            }
        }
    }
    
    void cleanup() {
        if (captureClient) {
            captureClient->Release();
            captureClient = nullptr;
        }
        
        if (audioClient) {
            audioClient->Release();
            audioClient = nullptr;
        }
        
        if (audioDevice) {
            audioDevice->Release();
            audioDevice = nullptr;
        }
        
        if (deviceEnumerator) {
            deviceEnumerator->Release();
            deviceEnumerator = nullptr;
        }
        
        if (audioFormat) {
            CoTaskMemFree(audioFormat);
            audioFormat = nullptr;
        }
    }
};