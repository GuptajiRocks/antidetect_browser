FROM ubuntu:22.04

# Install build dependencies
RUN apt-get update && apt-get install -y \
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
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r build/requirements.txt

# Make build script executable
RUN chmod +x build/build.sh

# Build the browser
RUN ./build/build.sh

CMD ["python3", "-m", "custom_browser.cli"]
