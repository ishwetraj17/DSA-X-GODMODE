cmake_minimum_required(VERSION 3.16)
project(DSA-X-GODMODE++ VERSION 1.0.0 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set build type if not specified
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# Compiler-specific options
if(MSVC)
    add_compile_options(/W4)
    add_definitions(-D_WIN32_WINNT=0x0601)  # Windows 7+
else()
    add_compile_options(-Wall -Wextra -pedantic)
endif()

# Platform detection
if(WIN32)
    add_definitions(-DPLATFORM_WINDOWS)
elseif(APPLE)
    add_definitions(-DPLATFORM_MACOS)
elseif(UNIX)
    add_definitions(-DPLATFORM_LINUX)
endif()

# Find required packages
find_package(Threads REQUIRED)

# Platform-specific libraries
if(WIN32)
    # Windows-specific libraries
    set(PLATFORM_LIBS
        ole32
        winmm
        user32
        gdi32
        kernel32
    )
elseif(APPLE)
    # macOS-specific frameworks
    find_library(COREAUDIO_FRAMEWORK CoreAudio)
    find_library(AUDIOTOOLBOX_FRAMEWORK AudioToolbox)
    find_library(COREFOUNDATION_FRAMEWORK CoreFoundation)
    find_library(METAL_FRAMEWORK Metal)
    find_library(METALKIT_FRAMEWORK MetalKit)
    find_library(APPKIT_FRAMEWORK AppKit)
    
    set(PLATFORM_LIBS
        ${COREAUDIO_FRAMEWORK}
        ${AUDIOTOOLBOX_FRAMEWORK}
        ${COREFOUNDATION_FRAMEWORK}
        ${METAL_FRAMEWORK}
        ${METALKIT_FRAMEWORK}
        ${APPKIT_FRAMEWORK}
    )
elseif(UNIX)
    # Linux-specific libraries
    find_package(PkgConfig REQUIRED)
    pkg_check_modules(ALSA REQUIRED alsa)
    
    set(PLATFORM_LIBS
        ${ALSA_LIBRARIES}
        X11
        Xrandr
        Xi
        GL
    )
endif()

# Include directories
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/boot
    ${CMAKE_CURRENT_SOURCE_DIR}/llm
    ${CMAKE_CURRENT_SOURCE_DIR}/overlay
    ${CMAKE_CURRENT_SOURCE_DIR}/stt
    ${CMAKE_CURRENT_SOURCE_DIR}/resume
    ${CMAKE_CURRENT_SOURCE_DIR}/test
)

# Source files - Core system
set(CORE_SOURCES
    boot/dsax_controller.cpp
    llm/prompt_classifier.cpp
    llm/answer_generator.cpp
)

# Platform-specific source files
if(WIN32)
    list(APPEND CORE_SOURCES
        boot/audio_input_windows.cpp
        overlay/overlay_windows.cpp
    )
elseif(APPLE)
    list(APPEND CORE_SOURCES
        boot/audio_input_mac.cpp
        overlay/overlay_mac.mm
    )
    set_source_files_properties(overlay/overlay_mac.mm PROPERTIES COMPILE_FLAGS "-x objective-c++")
endif()

# Whisper.cpp integration (if available)
find_path(WHISPER_INCLUDE_DIR whisper.h PATHS /usr/local/include /opt/homebrew/include)
find_library(WHISPER_LIBRARY whisper PATHS /usr/local/lib /opt/homebrew/lib)

if(WHISPER_INCLUDE_DIR AND WHISPER_LIBRARY)
    message(STATUS "Found Whisper.cpp: ${WHISPER_LIBRARY}")
    list(APPEND CORE_SOURCES boot/whisper_runner.cpp)
    include_directories(${WHISPER_INCLUDE_DIR})
    set(WHISPER_LIBS ${WHISPER_LIBRARY})
    add_definitions(-DWHISPER_AVAILABLE)
else()
    message(WARNING "Whisper.cpp not found - STT functionality will be limited")
    set(WHISPER_LIBS "")
endif()

# OpenCV (for OCR preprocessing)
find_package(OpenCV QUIET)
if(OpenCV_FOUND)
    message(STATUS "Found OpenCV: ${OpenCV_VERSION}")
    add_definitions(-DOPENCV_AVAILABLE)
    set(OPENCV_LIBS ${OpenCV_LIBS})
else()
    message(WARNING "OpenCV not found - OCR preprocessing will be limited")
    set(OPENCV_LIBS "")
endif()

# Main executable
add_executable(dsax-godmode main.cpp ${CORE_SOURCES})

# Link libraries
target_link_libraries(dsax-godmode 
    ${CMAKE_THREAD_LIBS_INIT}
    ${PLATFORM_LIBS}
    ${WHISPER_LIBS}
    ${OPENCV_LIBS}
)

# Compiler-specific optimizations
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    if(MSVC)
        target_compile_options(dsax-godmode PRIVATE /O2 /Ob2)
    else()
        target_compile_options(dsax-godmode PRIVATE -O3 -march=native -DNDEBUG)
    endif()
endif()

# Runtime path for dynamic libraries
if(APPLE)
    set_target_properties(dsax-godmode PROPERTIES
        INSTALL_RPATH "@executable_path"
        BUILD_WITH_INSTALL_RPATH TRUE
    )
elseif(UNIX)
    set_target_properties(dsax-godmode PROPERTIES
        INSTALL_RPATH "$ORIGIN"
        BUILD_WITH_INSTALL_RPATH TRUE
    )
endif()

# Installation
install(TARGETS dsax-godmode
    RUNTIME DESTINATION bin
)

# Copy Python fallback scripts
install(FILES
    stt/fallback_clipboard.py
    stt/fallback_ocr.py
    DESTINATION bin
    PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE
)

# Copy launch scripts
if(WIN32)
    install(FILES run_win.bat DESTINATION bin)
elseif(APPLE)
    install(FILES run_mac.command DESTINATION bin
        PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE)
endif()

# Copy documentation
install(FILES
    README.md
    PROJECT_OVERVIEW.md
    IMPLEMENTATION_STATUS.md
    DESTINATION share/doc/dsax-godmode
)

# Print build information
message(STATUS "")
message(STATUS "DSA-X GODMODE++ Build Configuration:")
message(STATUS "  Version: ${PROJECT_VERSION}")
message(STATUS "  Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "  Platform: ${CMAKE_SYSTEM_NAME}")
message(STATUS "  C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "  Compiler: ${CMAKE_CXX_COMPILER_ID} ${CMAKE_CXX_COMPILER_VERSION}")
message(STATUS "  Whisper.cpp: ${WHISPER_LIBRARY}")
message(STATUS "  OpenCV: ${OpenCV_VERSION}")
message(STATUS "")

# Custom targets for easy building
add_custom_target(run-test
    COMMAND $<TARGET_FILE:dsax-godmode> --test
    DEPENDS dsax-godmode
    COMMENT "Running DSA-X GODMODE++ in test mode"
)

add_custom_target(run-debug
    COMMAND $<TARGET_FILE:dsax-godmode> --no-stealth --verbose
    DEPENDS dsax-godmode
    COMMENT "Running DSA-X GODMODE++ in debug mode"
)

# Packaging
include(CPack)
set(CPACK_PACKAGE_NAME "DSA-X-GODMODE++")
set(CPACK_PACKAGE_VERSION ${PROJECT_VERSION})
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Ultra-Stealth AI Assistant for Technical Interviews")
set(CPACK_PACKAGE_VENDOR "Shwet Raj")
set(CPACK_PACKAGE_CONTACT "elite.systems.architect@example.com")

if(WIN32)
    set(CPACK_GENERATOR "ZIP;NSIS")
    set(CPACK_NSIS_DISPLAY_NAME "DSA-X GODMODE++")
    set(CPACK_NSIS_HELP_LINK "https://github.com/ishwetraj17/DSA-X-GODMODE")
elseif(APPLE)
    set(CPACK_GENERATOR "ZIP;DragNDrop")
elseif(UNIX)
    set(CPACK_GENERATOR "ZIP;TGZ;DEB")
    set(CPACK_DEBIAN_PACKAGE_MAINTAINER "Shwet Raj")
    set(CPACK_DEBIAN_PACKAGE_SECTION "utils")
endif()