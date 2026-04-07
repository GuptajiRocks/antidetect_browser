import subprocess, os, json
from .fingerprint_generator import FingerprintGenerator
from .profile_manager import ProfileManager

BROWSER_BINARY_PATH = "./build/camoufox/firefox"

class BrowserLauncher:
    @staticmethod
    def launch(profile_id: str, headless: bool = False):
        profile = ProfileManager.load_profile(profile_id)
        fingerprint = profile.get("fingerprint", FingerprintGenerator.generate_random())
        config_json = json.dumps(fingerprint)
        # Split the config into multiple env vars if it's too long
        chunks = [config_json[i:i+32000] for i in range(0, len(config_json), 32000)]
        env = os.environ.copy()
        for i, chunk in enumerate(chunks):
            env[f"CAMOU_CONFIG_{i+1}"] = chunk
        env["CAMOU_CONFIG_COUNT"] = str(len(chunks))
        cmd = [BROWSER_BINARY_PATH, "--profile", profile_id]
        if headless:
            cmd.append("--headless")
        subprocess.Popen(cmd, env=env)
