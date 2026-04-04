# Custom Antidetect Browser

A professional antidetect browser with C++-level fingerprint spoofing, built on top of Camoufox.

## Features

- **C++-Level Spoofing**: All fingerprint modifications occur at the browser engine level, making them invisible to JavaScript detection
- **Encrypted Profile Storage**: Browser profiles are stored with AES-256 encryption
- **Realistic Fingerprints**: Generated from statistical distributions of real devices
- **Proxy Support**: Per-profile proxy configuration
- **Cross-Platform**: Builds for Linux, Windows, and macOS

## Prerequisites

- Linux OS (build requirement - WSL will not work)
- Python 3.9+
- C++ build tools (gcc/clang)
- CMake 3.15+
- Git

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/custom-antidetect
cd custom-antidetect
