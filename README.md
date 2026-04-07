# 🛡️ Custom Antidetect Browser

A professional antidetect browser that creates isolated browser profiles with realistic fingerprints. Built on [Camoufox](https://github.com/daijro/camoufox) – no compilation required, uses pre‑built binaries.

## 🗂️ Project Structure
## 🗂️ Project Structure

```
custom-antidetect/
├── build/
│   └── requirements.txt          # Python dependencies
├── pythonlib/
│   └── custom_browser/
│       ├── cli.py                # CLI entry point
│       ├── launcher.py           # Browser launch logic (uses Camoufox)
│       ├── profile_manager.py    # Encrypted profile storage
│       └── fingerprint_generator.py (optional)
├── profiles/                     # Encrypted profile files (auto-created)
├── pyproject.toml                # Package configuration
├── setup.py                      # Install script
└── README.md
```

## ✨ Features

- **Multi‑profile management** – Create, store, and launch separate browser identities.
- **Engine‑level fingerprint spoofing** – All modifications happen inside the browser's C++ core, invisible to JavaScript detection (Canvas, WebGL, Navigator, etc.).
- **Proxy per profile** – Assign a different proxy to each profile; automatic timezone & locale spoofing based on proxy IP.
- **Encrypted profile storage** – Profiles are encrypted with AES‑256 (customizable master key).
- **Headless support** – Run browsers in headless mode for automation.
- **CLI & Python API** – Easy command‑line interface or programmatic control.

## 📋 Prerequisites

- **Linux** (recommended – the pre‑built binary is tested on Ubuntu 20.04+)
- **Python 3.9+** and `pip`
- **Virtual environment** (recommended)
- **Internet connection** (to download the Camoufox binary)

> **Note**: Windows and macOS are not officially tested, but the Camoufox binary may work with additional configuration.

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/custom-antidetect.git
cd custom-antidetect
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r build/requirements.txt
```

### 4. Fetch the Camoufox browser binary
```bash
python -m camoufox fetch
```
This downloads the latest Camoufox binary to ~/.cache/camoufox/. The download is about 150 MB.

### 5. Install the CLI globally (optional)
```bash
pip install -e .
```

## 🎮 CLI Usage
All commands are available through python -m custom_browser.cli or custom-browser after installation.

### Create a new profile
```bash
custom-browser create --name "work" --proxy "http://user:pass@proxy-host:port"
```

| Option | Description |
|--------|-------------|
| --name, -n | (Required) Profile name |
| --proxy, -p | Proxy URL (optional). Format: http://user:pass@host:port or socks5://user:pass@host:port |
| --os | Hint for fingerprint OS: windows, macos, linux (default: windows) |
| --custom-fingerprint | Path to a JSON file with fingerprint overrides (advanced) |

### List all profiles
```bash
custom-browser list
```
Example output:
```bash
📋 Available profiles:
------------------------------------------------------------
  ID: 550e8400-e29b-41d4-a716-446655440000
  Name: work
  Created: 2025-04-07T10:30:00
  Proxy: yes
------------------------------------------------------------
```

### Launch a profile
```bash
custom-browser launch work   # by name
# or
custom-browser launch 550e8400-e29b-41d4-a716-446655440000   # by ID

Options:

--headless – Run without a GUI (useful for automation)

--block-images – Block image loading to save bandwidth

--block-webrtc – Disable WebRTC (enabled by default)
```

### Show profile details
```bash
custom-browser info work
```

### Delete a profile
```bash
custom-browser delete work
```

### 🔧 Proxy Configuration
Supported proxy formats
HTTP/HTTPS with or without authentication:
http://proxy-ip:port
http://username:password@proxy-ip:port

SOCKS5:
socks5://username:password@proxy-ip:port

Automatic geo‑spoofing
When you set --proxy, Camoufox automatically:

Uses the proxy’s IP to determine your approximate location

Spoofs timezone, locale, and language to match that location

Works out‑of‑the‑box with geoip=True (default in the launcher)

### Testing your proxy
Before using a proxy in the browser, test it with curl:
```bash
curl -x http://user:pass@proxy-ip:port https://api.ipify.org
```

## 🔐 Profile Encryption
Profiles are stored in profiles/ as .enc files encrypted with AES‑256. The encryption key is derived from:

A hardcoded salt (custom_browser_salt_2024) – change this for production

A master password stored in the environment variable BROWSER_MASTER_KEY

To use a custom master key:

```bash
export BROWSER_MASTER_KEY="your-strong-password-here"
```
If no key is set, a default insecure key is used. Do not share profiles encrypted with the default key – they can be decrypted by anyone.

## ⚠️ Troubleshooting
<h3>camoufox.exceptions.InvalidProxy</h3>
The proxy URL is malformed or the proxy server is unreachable.

Verify the proxy works with curl.

Try creating a profile without --proxy first.

--Browser doesn't launch / binary not found

Run python -m camoufox fetch again.

Check ~/.cache/camoufox/ – if empty, download manually from Camoufox releases and place the binary there.

## 📦 Updating
To update the browser binary:
```bash
python -m camoufox fetch --force   # redownloads the latest
```
To update the Python package:
```bash
pip install -U camoufox
```

## 🙏 Acknowledgements
Camoufox – the core browser with stealth patches

Playwright – browser automation

BrowserForge – realistic fingerprint generation
