"""Fingerprint generation for browser profiles."""

import random
from typing import Any, Dict

from browserforge import FingerprintGenerator as BFGenerator


class FingerprintGenerator:
    """Generates realistic device fingerprints."""

    # Common screen resolutions by platform
    SCREEN_RESOLUTIONS = {
        "windows": [(1920, 1080), (1366, 768), (1536, 864), (1440, 900), (2560, 1440)],
        "macos": [(1920, 1080), (2560, 1600), (1440, 900), (1680, 1050), (3008, 1692)],
        "linux": [(1920, 1080), (1366, 768), (1600, 900), (1280, 720)],
    }

    # Common user agents by platform
    USER_AGENTS = {
        "windows": [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        ],
        "macos": [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:120.0) Gecko/20100101 Firefox/120.0",
        ],
        "linux": [
            "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        ],
    }

    @staticmethod
    def generate_for_os(os_type: str) -> Dict[str, Any]:
        """Generate a realistic fingerprint for the specified OS."""

        # Select random screen resolution
        screen_width, screen_height = random.choice(
            FingerprintGenerator.SCREEN_RESOLUTIONS.get(
                os_type, FingerprintGenerator.SCREEN_RESOLUTIONS["windows"]
            )
        )

        # Select random user agent
        user_agent = random.choice(
            FingerprintGenerator.USER_AGENTS.get(
                os_type, FingerprintGenerator.USER_AGENTS["windows"]
            )
        )

        # Platform string mapping
        platform_map = {"windows": "Win32", "macos": "MacIntel", "linux": "Linux x86_64"}

        # Language mapping (simplified)
        languages = ["en-US", "en-GB", "en-CA"]

        fingerprint = {
            "userAgent": user_agent,
            "platform": platform_map.get(os_type, "Win32"),
            "language": random.choice(languages),
            "languages": [random.choice(languages)],
            "screenWidth": screen_width,
            "screenHeight": screen_height,
            "colorDepth": 24,
            "pixelRatio": 2.0 if random.random() > 0.5 else 1.0,
            "timezone": "America/New_York",  # Should be derived from proxy location
            "timezoneOffset": -300,  # Minutes from UTC
            "hardwareConcurrency": random.choice([4, 6, 8, 12]),
            "deviceMemory": random.choice([4, 8, 16]),
            "webglVendor": "Google Inc. (Intel)",
            "webglRenderer": f"ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "audioContext": {"sampleRate": 44100, "channelCount": 2},
        }

        return fingerprint

    @staticmethod
    def generate_random() -> Dict[str, Any]:
        """Generate a random fingerprint from real-world distribution."""
        # Use browserforge for more realistic distributions
        try:
            bf = BFGenerator()
            return bf.generate()
        except Exception:
            # Fallback to basic generation
            return FingerprintGenerator.generate_for_os(
                random.choice(["windows", "macos", "linux"])
            )

    @staticmethod
    def generate_from_profile(profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fingerprint based on existing profile data."""
        # This would apply transformations to maintain consistency
        return profile_data.get("fingerprint", FingerprintGenerator.generate_random())
