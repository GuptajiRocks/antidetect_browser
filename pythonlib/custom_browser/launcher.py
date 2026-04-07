import os
from typing import Any, Dict, Optional

from camoufox.sync_api import Camoufox


class BrowserLauncher:
    @staticmethod
    def launch(
        profile_data: Dict[str, Any],
        headless: bool = False,
        block_images: bool = False,
        block_webrtc: bool = True,
    ) -> None:
        proxy_config = profile_data.get("proxy")
        proxy = None
        if proxy_config and "url" in proxy_config:
            proxy = {"server": proxy_config["url"]}

        custom_fingerprint = profile_data.get("custom_fingerprint", {})

        with Camoufox(
            headless=headless,
            proxy=proxy,
            geoip=True,
            block_images=block_images,
            block_webrtc=block_webrtc,
            config=custom_fingerprint if custom_fingerprint else None,
        ) as browser:
            page = browser.new_page()
            # Optionally open a default URL or let the user interact
            page.goto("https://pixelscan.net")
            print("Browser launched. Press Ctrl+C to exit.")
            try:
                # Keep browser open until user interrupts
                import time

                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nClosing browser...")
