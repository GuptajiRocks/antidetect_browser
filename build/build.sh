#!/bin/bash
set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}=== Custom Antidetect Browser Build System ===${NC}"

CAMOUFOX_REPO="https://github.com/daijro/camoufox.git"
CAMOUFOX_DIR="src/firefox-source"
BUILD_TARGET=${1:-"linux"}
BUILD_ARCH=${2:-"x86_64"}

print_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
print_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    print_error "Camoufox build system requires Linux (WSL will not work)"
    exit 1
fi

# Handle existing directory that may not be a git repo
if [ -d "$CAMOUFOX_DIR" ]; then
    if [ -d "$CAMOUFOX_DIR/.git" ]; then
        print_info "Camoufox repository exists, updating..."
        cd "$CAMOUFOX_DIR"
        git pull
        cd ../..
    else
        print_warn "$CAMOUFOX_DIR exists but is not a git repository. Removing and re-cloning..."
        rm -rf "$CAMOUFOX_DIR"
        print_info "Cloning Camoufox repository..."
        mkdir -p "$(dirname "$CAMOUFOX_DIR")"
        git clone --depth 1 "$CAMOUFOX_REPO" "$CAMOUFOX_DIR"
    fi
else
    print_info "Cloning Camoufox repository..."
    mkdir -p "$(dirname "$CAMOUFOX_DIR")"
    git clone --depth 1 "$CAMOUFOX_REPO" "$CAMOUFOX_DIR"
fi

# Copy custom C++ patches
if [ -d "src/camoucfg" ]; then
    print_info "Copying custom MaskConfig files..."
    cp src/camoucfg/MaskConfig.hpp "$CAMOUFOX_DIR/camoucfg/" 2>/dev/null || mkdir -p "$CAMOUFOX_DIR/camoucfg" && cp src/camoucfg/MaskConfig.hpp "$CAMOUFOX_DIR/camoucfg/"
    cp src/camoucfg/MaskConfig.cpp "$CAMOUFOX_DIR/camoucfg/" 2>/dev/null || cp src/camoucfg/MaskConfig.cpp "$CAMOUFOX_DIR/camoucfg/"
    print_info "Custom MaskConfig files integrated"
else
    print_warn "No custom patches found in src/camoucfg/"
fi

# Install system build dependencies (optional - uncomment if needed)
# print_info "Installing build dependencies..."
# cd "$CAMOUFOX_DIR"
# make dir

# Bootstrap and build
cd "$CAMOUFOX_DIR"
if [ ! -f ".bootstrapped" ]; then
    print_info "Bootstrapping build system (first time only)..."
    make bootstrap
    touch .bootstrapped
else
    print_info "Build system already bootstrapped"
fi

print_info "Building Camoufox for $BUILD_TARGET/$BUILD_ARCH..."
python3 multibuild.py --target "$BUILD_TARGET" --arch "$BUILD_ARCH"

cd ../..
print_info "Installing Python dependencies..."
pip install -r build/requirements.txt

print_info "Downloading Playwright browsers..."
playwright install firefox

echo -e "${GREEN}=== Build completed successfully! ===${NC}"
echo ""
echo "Next steps:"
echo "1. Run 'python -m custom_browser.cli' to start the profile manager"
echo "2. Or use the Python API directly"
