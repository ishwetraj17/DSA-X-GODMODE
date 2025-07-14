/*
 * DSA-X GODMODE++: Ultra-Stealth AI Assistant
 * macOS Metal GPU Overlay System
 * 
 * Implemented by Shwet Raj
 * Debug checkpoint: Metal rendering and stealth overlay display
 */

#import <Foundation/Foundation.h>
#import <AppKit/AppKit.h>
#import <Metal/Metal.h>
#import <MetalKit/MetalKit.h>
#import <CoreGraphics/CoreGraphics.h>
#import <QuartzCore/QuartzCore.h>

#include <string>
#include <vector>
#include <mutex>
#include <atomic>

@interface StealthOverlayWindow : NSWindow
@property (nonatomic, strong) MTKView* metalView;
@property (nonatomic, strong) id<MTLDevice> device;
@property (nonatomic, strong) id<MTLCommandQueue> commandQueue;
@property (nonatomic, strong) id<MTLRenderPipelineState> pipelineState;
@property (nonatomic, strong) id<MTLBuffer> vertexBuffer;
@property (nonatomic, strong) NSString* displayText;
@property (nonatomic, assign) BOOL isVisible;
@end

@interface MetalRenderer : NSObject <MTKViewDelegate>
@property (nonatomic, weak) StealthOverlayWindow* parentWindow;
@property (nonatomic, strong) id<MTLDevice> device;
@property (nonatomic, strong) id<MTLCommandQueue> commandQueue;
@property (nonatomic, strong) id<MTLRenderPipelineState> pipelineState;
@property (nonatomic, strong) id<MTLBuffer> vertexBuffer;
@property (nonatomic, strong) id<MTLTexture> textTexture;
@property (nonatomic, assign) float opacity;
@property (nonatomic, assign) NSRect textBounds;
@end

// Vertex structure for Metal rendering
typedef struct {
    vector_float2 position;
    vector_float2 texCoord;
    vector_float4 color;
} Vertex;

@implementation StealthOverlayWindow

- (instancetype)init {
    // Create window that covers the entire screen
    NSRect screenRect = [[NSScreen mainScreen] frame];
    
    // Initialize as borderless, transparent window
    self = [super initWithContentRect:screenRect
                            styleMask:NSWindowStyleMaskBorderless
                              backing:NSBackingStoreBuffered
                                defer:NO];
    
    if (self) {
        [self setupWindow];
        [self setupMetal];
        [self setupMetalView];
    }
    
    return self;
}

- (void)setupWindow {
    // Configure window for stealth operation
    [self setLevel:NSFloatingWindowLevel + 1];  // Above most windows
    [self setOpaque:NO];
    [self setBackgroundColor:[NSColor clearColor]];
    [self setHasShadow:NO];
    [self setIgnoresMouseEvents:YES];  // Click-through
    [self setAcceptsMouseMovedEvents:NO];
    [self setMovableByWindowBackground:NO];
    [self setHidesOnDeactivate:NO];
    [self setCanHide:NO];
    [self setCollectionBehavior:NSWindowCollectionBehaviorCanJoinAllSpaces |
                                NSWindowCollectionBehaviorStationary |
                                NSWindowCollectionBehaviorIgnoresCycle];
    
    // Hide from dock and app switcher
    [NSApp setActivationPolicy:NSApplicationActivationPolicyAccessory];
    
    self.isVisible = NO;
    self.displayText = @"";
    
    NSLog(@"🖼️  Stealth overlay window configured");
}

- (void)setupMetal {
    // Initialize Metal device
    self.device = MTLCreateSystemDefaultDevice();
    if (!self.device) {
        NSLog(@"❌ Failed to create Metal device");
        return;
    }
    
    // Create command queue
    self.commandQueue = [self.device newCommandQueue];
    if (!self.commandQueue) {
        NSLog(@"❌ Failed to create Metal command queue");
        return;
    }
    
    NSLog(@"✅ Metal device initialized: %@", self.device.name);
}

- (void)setupMetalView {
    // Create MTKView
    self.metalView = [[MTKView alloc] initWithFrame:self.contentView.bounds
                                             device:self.device];
    
    if (!self.metalView) {
        NSLog(@"❌ Failed to create MTKView");
        return;
    }
    
    // Configure MTKView for transparency and performance
    self.metalView.colorPixelFormat = MTLPixelFormatBGRA8Unorm;
    self.metalView.clearColor = MTLClearColorMake(0.0, 0.0, 0.0, 0.0);  // Transparent
    self.metalView.framebufferOnly = YES;  // Optimization
    self.metalView.autoResizeDrawable = YES;
    self.metalView.enableSetNeedsDisplay = NO;
    self.metalView.paused = YES;  // Manual control
    
    // Create renderer
    MetalRenderer* renderer = [[MetalRenderer alloc] init];
    renderer.parentWindow = self;
    renderer.device = self.device;
    renderer.commandQueue = self.commandQueue;
    
    self.metalView.delegate = renderer;
    
    // Add to window
    [self.contentView addSubview:self.metalView];
    
    // Setup shaders and pipeline
    [self setupRenderPipeline];
    
    NSLog(@"✅ Metal view configured");
}

- (void)setupRenderPipeline {
    NSError* error = nil;
    
    // Metal shader source (embedded)
    NSString* shaderSource = @R"(
        #include <metal_stdlib>
        using namespace metal;
        
        struct VertexIn {
            float2 position [[attribute(0)]];
            float2 texCoord [[attribute(1)]];
            float4 color [[attribute(2)]];
        };
        
        struct VertexOut {
            float4 position [[position]];
            float2 texCoord;
            float4 color;
        };
        
        vertex VertexOut vertex_main(VertexIn in [[stage_in]]) {
            VertexOut out;
            out.position = float4(in.position, 0.0, 1.0);
            out.texCoord = in.texCoord;
            out.color = in.color;
            return out;
        }
        
        fragment float4 fragment_main(VertexOut in [[stage_in]],
                                     texture2d<float> texture [[texture(0)]],
                                     sampler texSampler [[sampler(0)]]) {
            float4 texColor = texture.sample(texSampler, in.texCoord);
            return texColor * in.color;
        }
    )";
    
    // Compile shaders
    id<MTLLibrary> library = [self.device newLibraryWithSource:shaderSource
                                                       options:nil
                                                         error:&error];
    
    if (!library || error) {
        NSLog(@"❌ Failed to compile shaders: %@", error.localizedDescription);
        return;
    }
    
    id<MTLFunction> vertexFunction = [library newFunctionWithName:@"vertex_main"];
    id<MTLFunction> fragmentFunction = [library newFunctionWithName:@"fragment_main"];
    
    // Create render pipeline descriptor
    MTLRenderPipelineDescriptor* pipelineDescriptor = [[MTLRenderPipelineDescriptor alloc] init];
    pipelineDescriptor.vertexFunction = vertexFunction;
    pipelineDescriptor.fragmentFunction = fragmentFunction;
    pipelineDescriptor.colorAttachments[0].pixelFormat = self.metalView.colorPixelFormat;
    
    // Enable alpha blending for transparency
    pipelineDescriptor.colorAttachments[0].blendingEnabled = YES;
    pipelineDescriptor.colorAttachments[0].rgbBlendOperation = MTLBlendOperationAdd;
    pipelineDescriptor.colorAttachments[0].alphaBlendOperation = MTLBlendOperationAdd;
    pipelineDescriptor.colorAttachments[0].sourceRGBBlendFactor = MTLBlendFactorSourceAlpha;
    pipelineDescriptor.colorAttachments[0].sourceAlphaBlendFactor = MTLBlendFactorSourceAlpha;
    pipelineDescriptor.colorAttachments[0].destinationRGBBlendFactor = MTLBlendFactorOneMinusSourceAlpha;
    pipelineDescriptor.colorAttachments[0].destinationAlphaBlendFactor = MTLBlendFactorOneMinusSourceAlpha;
    
    // Create pipeline state
    self.pipelineState = [self.device newRenderPipelineStateWithDescriptor:pipelineDescriptor
                                                                      error:&error];
    
    if (!self.pipelineState || error) {
        NSLog(@"❌ Failed to create render pipeline: %@", error.localizedDescription);
        return;
    }
    
    NSLog(@"✅ Metal render pipeline created");
}

- (BOOL)initialize {
    if (!self.device || !self.commandQueue || !self.pipelineState) {
        NSLog(@"❌ Metal initialization incomplete");
        return NO;
    }
    
    NSLog(@"✅ StealthOverlayWindow initialized successfully");
    return YES;
}

- (void)updateDisplay:(NSString*)text {
    if (!text || text.length == 0) {
        [self hideOverlay];
        return;
    }
    
    self.displayText = text;
    [self createTextTexture];
    [self showOverlay];
    [self.metalView setNeedsDisplay:YES];
}

- (void)createTextTexture {
    if (!self.displayText || self.displayText.length == 0) {
        return;
    }
    
    // Create attributed string with styling
    NSMutableDictionary* attributes = [NSMutableDictionary dictionary];
    
    // Font configuration
    NSFont* font = [NSFont fontWithName:@"Menlo" size:14.0];
    if (!font) {
        font = [NSFont systemFontOfSize:14.0];
    }
    attributes[NSFontAttributeName] = font;
    
    // Text color (green on dark background for readability)
    attributes[NSForegroundColorAttributeName] = [NSColor colorWithRed:0.0 green:1.0 blue:0.3 alpha:0.9];
    
    // Background and styling
    attributes[NSBackgroundColorAttributeName] = [NSColor colorWithRed:0.0 green:0.0 blue:0.0 alpha:0.7];
    
    NSAttributedString* attributedText = [[NSAttributedString alloc] initWithString:self.displayText
                                                                         attributes:attributes];
    
    // Calculate text size
    NSSize textSize = [attributedText size];
    textSize.width += 20;  // Padding
    textSize.height += 10;
    
    // Create image context
    NSImage* textImage = [[NSImage alloc] initWithSize:textSize];
    [textImage lockFocus];
    
    // Clear background
    [[NSColor clearColor] set];
    NSRectFill(NSMakeRect(0, 0, textSize.width, textSize.height));
    
    // Draw text
    [attributedText drawAtPoint:NSMakePoint(10, 5)];
    
    [textImage unlockFocus];
    
    // Convert to Metal texture (implementation would continue here)
    NSLog(@"📝 Text texture created for: %.50@...", self.displayText);
}

- (void)showOverlay {
    if (!self.isVisible) {
        self.isVisible = YES;
        [self orderFront:nil];
        [self.metalView setPaused:NO];
        NSLog(@"👁️  Overlay shown");
    }
}

- (void)hideOverlay {
    if (self.isVisible) {
        self.isVisible = NO;
        [self orderOut:nil];
        [self.metalView setPaused:YES];
        NSLog(@"🙈 Overlay hidden");
    }
}

- (void)cleanup {
    [self hideOverlay];
    self.metalView.delegate = nil;
    [self.metalView removeFromSuperview];
    self.metalView = nil;
    self.device = nil;
    self.commandQueue = nil;
    self.pipelineState = nil;
    NSLog(@"🧹 Overlay cleanup complete");
}

@end

@implementation MetalRenderer

- (void)mtkView:(MTKView*)view drawableSizeWillChange:(CGSize)size {
    // Handle resize if needed
    NSLog(@"🔄 Metal view resized: %.0fx%.0f", size.width, size.height);
}

- (void)drawInMTKView:(MTKView*)view {
    if (!self.parentWindow.isVisible || !self.parentWindow.displayText) {
        return;
    }
    
    // Create command buffer
    id<MTLCommandBuffer> commandBuffer = [self.commandQueue commandBuffer];
    
    // Get render pass descriptor
    MTLRenderPassDescriptor* renderPassDescriptor = view.currentRenderPassDescriptor;
    if (!renderPassDescriptor) {
        return;
    }
    
    // Create render encoder
    id<MTLRenderCommandEncoder> renderEncoder = [commandBuffer renderCommandEncoderWithDescriptor:renderPassDescriptor];
    
    // Set pipeline state
    [renderEncoder setRenderPipelineState:self.parentWindow.pipelineState];
    
    // Render text quad (implementation would continue with actual rendering)
    
    [renderEncoder endEncoding];
    
    // Present drawable
    [commandBuffer presentDrawable:view.currentDrawable];
    [commandBuffer commit];
}

@end

// C++ wrapper class for integration
class StealthOverlayWindow_CPP {
private:
    StealthOverlayWindow* overlay;
    std::mutex updateMutex;
    std::atomic<bool> isInitialized;
    
public:
    StealthOverlayWindow_CPP() : overlay(nil), isInitialized(false) {
    }
    
    ~StealthOverlayWindow_CPP() {
        cleanup();
    }
    
    bool initialize() {
        @autoreleasepool {
            overlay = [[StealthOverlayWindow alloc] init];
            if (overlay && [overlay initialize]) {
                isInitialized = true;
                NSLog(@"✅ C++ wrapper initialized");
                return true;
            }
            NSLog(@"❌ C++ wrapper initialization failed");
            return false;
        }
    }
    
    void updateDisplay(const std::string& text) {
        if (!isInitialized.load() || !overlay) {
            return;
        }
        
        std::lock_guard<std::mutex> lock(updateMutex);
        
        @autoreleasepool {
            NSString* nsText = [NSString stringWithUTF8String:text.c_str()];
            dispatch_async(dispatch_get_main_queue(), ^{
                [overlay updateDisplay:nsText];
            });
        }
    }
    
    void hide() {
        if (!isInitialized.load() || !overlay) {
            return;
        }
        
        dispatch_async(dispatch_get_main_queue(), ^{
            [overlay hideOverlay];
        });
    }
    
    void show() {
        if (!isInitialized.load() || !overlay) {
            return;
        }
        
        dispatch_async(dispatch_get_main_queue(), ^{
            [overlay showOverlay];
        });
    }
    
    void cleanup() {
        if (overlay) {
            dispatch_sync(dispatch_get_main_queue(), ^{
                [overlay cleanup];
                overlay = nil;
            });
            isInitialized = false;
        }
    }
    
    bool isVisible() const {
        if (!isInitialized.load() || !overlay) {
            return false;
        }
        return overlay.isVisible;
    }
};

// C interface for C++ integration
extern "C" {
    StealthOverlayWindow_CPP* createStealthOverlay() {
        return new StealthOverlayWindow_CPP();
    }
    
    bool initializeStealthOverlay(StealthOverlayWindow_CPP* overlay) {
        return overlay ? overlay->initialize() : false;
    }
    
    void updateStealthOverlay(StealthOverlayWindow_CPP* overlay, const char* text) {
        if (overlay && text) {
            overlay->updateDisplay(std::string(text));
        }
    }
    
    void hideStealthOverlay(StealthOverlayWindow_CPP* overlay) {
        if (overlay) {
            overlay->hide();
        }
    }
    
    void showStealthOverlay(StealthOverlayWindow_CPP* overlay) {
        if (overlay) {
            overlay->show();
        }
    }
    
    void destroyStealthOverlay(StealthOverlayWindow_CPP* overlay) {
        delete overlay;
    }
}