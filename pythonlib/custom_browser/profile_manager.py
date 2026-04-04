"""Profile management with encryption and storage."""

import base64
import json
import os
import uuid
from typing import Any, Dict, List, Optional

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2

# Configuration
PROFILES_DIR = "profiles"
ENCRYPTION_SALT = b"custom_browser_salt_2024"  # In production, use a secure random salt


def get_cipher() -> Fernet:
    """Get or create encryption cipher."""
    # In production, derive key from user password or secure keyfile
    # For now, use a deterministic key derived from salt
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=ENCRYPTION_SALT,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(b"secure_master_password"))
    return Fernet(key)


class ProfileManager:
    """Manages browser profiles with encryption."""

    @staticmethod
    def _ensure_profiles_dir():
        """Ensure the profiles directory exists."""
        os.makedirs(PROFILES_DIR, exist_ok=True)

    @staticmethod
    def create_profile(
        name: str, fingerprint: Dict[str, Any], proxy: Optional[Dict[str, str]] = None
    ) -> str:
        """Create a new encrypted profile."""
        ProfileManager._ensure_profiles_dir()

        profile_id = str(uuid.uuid4())
        profile_data = {
            "id": profile_id,
            "name": name,
            "fingerprint": fingerprint,
            "proxy": proxy,
            "created_at": __import__("datetime").datetime.now().isoformat(),
        }

        # Encrypt and save
        json_data = json.dumps(profile_data, indent=2)
        cipher = get_cipher()
        encrypted_data = cipher.encrypt(json_data.encode())

        file_path = os.path.join(PROFILES_DIR, f"{profile_id}.enc")
        with open(file_path, "wb") as f:
            f.write(encrypted_data)

        return profile_id

    @staticmethod
    def load_profile(profile_id: str) -> Dict[str, Any]:
        """Load and decrypt a profile."""
        file_path = os.path.join(PROFILES_DIR, f"{profile_id}.enc")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Profile {profile_id} not found")

        with open(file_path, "rb") as f:
            encrypted_data = f.read()

        cipher = get_cipher()
        decrypted_data = cipher.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode())

    @staticmethod
    def list_profiles() -> List[Dict[str, Any]]:
        """List all available profiles (without full fingerprint details)."""
        ProfileManager._ensure_profiles_dir()
        profiles = []

        for filename in os.listdir(PROFILES_DIR):
            if filename.endswith(".enc"):
                profile_id = filename[:-4]  # Remove .enc extension
                try:
                    profile = ProfileManager.load_profile(profile_id)
                    # Return limited info for listing
                    profiles.append(
                        {
                            "id": profile["id"],
                            "name": profile["name"],
                            "fingerprint": {
                                "platform": profile["fingerprint"].get("platform", "unknown")
                            },
                        }
                    )
                except Exception as e:
                    print(f"Warning: Failed to load profile {profile_id}: {e}")

        return profiles

    @staticmethod
    def delete_profile(profile_id: str) -> bool:
        """Delete a profile."""
        file_path = os.path.join(PROFILES_DIR, f"{profile_id}.enc")
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False

    @staticmethod
    def update_profile(profile_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing profile."""
        try:
            profile = ProfileManager.load_profile(profile_id)
            profile.update(updates)

            # Re-save the profile
            json_data = json.dumps(profile, indent=2)
            cipher = get_cipher()
            encrypted_data = cipher.encrypt(json_data.encode())

            file_path = os.path.join(PROFILES_DIR, f"{profile_id}.enc")
            with open(file_path, "wb") as f:
                f.write(encrypted_data)
            return True
        except Exception:
            return False
