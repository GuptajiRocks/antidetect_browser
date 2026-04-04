#!/bin/bash
set -e

echo "Installing system dependencies for Custom Antidetect Browser..."

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected Linux distribution"

    # Check for package manager
    if command -v apt-get &> /dev/null; then
        echo "Using apt-get (Debian/Ubuntu)"
        sudo apt-get update
        sudo apt-get install -y \
            build-essential \
            cmake \
            git \
            python3 \
            python3-pip \
            curl \
            wget \
            unzip \
            libgtk-3-dev \
            libdbus-glib-1-dev \
            libxt-dev \
            libpulse-dev \
            libasound2-dev \
            libx11-xcb-dev \
            libxcb-shm0-dev \
            libxcb-keysyms1-dev \
            libxcb-util0-dev \
            libxcb-randr0-dev \
            libxcb-shape0-dev \
            libxfixes-dev \
            libxrandr-dev \
            libxcomposite-dev \
            libxdamage-dev \
            libxrender-dev \
            libxext-dev \
            libxss-dev \
            libxtst-dev \
            libcups2-dev \
            libavcodec-dev \
            libavformat-dev \
            libavutil-dev \
            libvpx-dev \
            libevent-dev \
            libnotify-dev \
            libsqlite3-dev
    elif command -v yum &> /dev/null; then
        echo "Using yum (RHEL/CentOS/Fedora)"
        sudo yum groupinstall -y "Development Tools"
        sudo yum install -y \
            cmake \
            git \
            python3 \
            python3-pip \
            gtk3-devel \
            dbus-glib-devel \
            libXt-devel \
            pulseaudio-libs-devel \
            alsa-lib-devel \
            libX11-devel \
            libXfixes-devel \
            libXrandr-devel \
            libXcomposite-devel \
            libXdamage-devel \
            libXrender-devel \
            libXext-devel \
            libXScrnSaver-devel \
            libXtst-devel \
            cups-devel \
            libvpx-devel \
            libevent-devel \
            libnotify-devel \
            sqlite-devel
    else
        echo "Unsupported package manager. Please install dependencies manually."
        exit 1
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS"
    if ! command -v brew &> /dev/null; then
        echo "Homebrew not found. Installing..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    brew install cmake git python3
else
    echo "Unsupported operating system: $OSTYPE"
    exit 1
fi

echo "System dependencies installed successfully!"
