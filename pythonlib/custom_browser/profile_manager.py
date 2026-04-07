import base64
import json
import os
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

PROFILES_DIR = "profiles"
ENCRYPTION_SALT = b"custom_browser_salt_2024"  # In production, use a secure random salt per user


def _get_cipher() -> Fernet:
    """Derive encryption key from a master password (simplified)."""
    # For real security, prompt for a password or read from env.
    # Here we use a fixed key derived from a hardcoded secret – not secure for sharing.
    # Better: read from environment variable or key file.
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=ENCRYPTION_SALT,
        iterations=100000,
    )
    master_key = os.environ.get("BROWSER_MASTER_KEY", "default_insecure_key_change_me").encode()
    key = base64.urlsafe_b64encode(kdf.derive(master_key))
    return Fernet(key)


class ProfileManager:
    @staticmethod
    def _ensure_dir():
        os.makedirs(PROFILES_DIR, exist_ok=True)

    @staticmethod
    def create_profile(
        name: str, proxy: Optional[Dict[str, str]] = None, custom_fingerprint: Optional[Dict] = None
    ) -> str:
        ProfileManager._ensure_dir()
        profile_id = str(uuid.uuid4())
        profile = {
            "id": profile_id,
            "name": name,
            "proxy": proxy,
            "custom_fingerprint": custom_fingerprint,  # optional overrides
            "created_at": datetime.now().isoformat(),
            "last_used": None,
        }
        cipher = _get_cipher()
        encrypted = cipher.encrypt(json.dumps(profile, indent=2).encode())
        with open(os.path.join(PROFILES_DIR, f"{profile_id}.enc"), "wb") as f:
            f.write(encrypted)
        return profile_id

    @staticmethod
    def load_profile(profile_id: str) -> Dict[str, Any]:
        path = os.path.join(PROFILES_DIR, f"{profile_id}.enc")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Profile {profile_id} not found")
        with open(path, "rb") as f:
            encrypted = f.read()
        cipher = _get_cipher()
        decrypted = cipher.decrypt(encrypted)
        return json.loads(decrypted.decode())

    @staticmethod
    def list_profiles() -> List[Dict[str, Any]]:
        ProfileManager._ensure_dir()
        profiles = []
        for fname in os.listdir(PROFILES_DIR):
            if fname.endswith(".enc"):
                profile_id = fname[:-4]
                try:
                    prof = ProfileManager.load_profile(profile_id)
                    profiles.append(
                        {
                            "id": prof["id"],
                            "name": prof["name"],
                            "created_at": prof.get("created_at"),
                            "has_proxy": prof.get("proxy") is not None,
                        }
                    )
                except Exception as e:
                    print(f"Warning: could not load {profile_id}: {e}")
        return profiles

    @staticmethod
    def delete_profile(profile_id: str) -> bool:
        path = os.path.join(PROFILES_DIR, f"{profile_id}.enc")
        if os.path.exists(path):
            os.remove(path)
            return True
        return False

    @staticmethod
    def update_profile(profile_id: str, updates: Dict) -> bool:
        try:
            prof = ProfileManager.load_profile(profile_id)
            prof.update(updates)
            cipher = _get_cipher()
            encrypted = cipher.encrypt(json.dumps(prof, indent=2).encode())
            with open(os.path.join(PROFILES_DIR, f"{profile_id}.enc"), "wb") as f:
                f.write(encrypted)
            return True
        except Exception:
            return False
