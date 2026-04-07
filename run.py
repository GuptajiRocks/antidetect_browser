#!/usr/bin/env python3
from pythonlib.custom_browser.launcher import BrowserLauncher

if __name__ == "__main__":
    # Minimal profile data (no custom fingerprint needed)
    profile = {
        "name": "test",
        "proxy": None,   # or {"url": "http://user:pass@host:port"}
    }
    BrowserLauncher.launch(profile, headless=False)
