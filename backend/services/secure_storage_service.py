import os
from cryptography.fernet import Fernet

class SecureStorageService:
    def __init__(self):
        self.key_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "secure_key.key")
        self.fernet = self._init_fernet()

    def _init_fernet(self) -> Fernet:
        """Initializes the Fernet encryption cipher using an env variable or a local key file."""
        # 1. Try to read from environment variable
        key = os.getenv("MONU_SECURE_KEY")
        
        if key:
            try:
                return Fernet(key.encode())
            except Exception as e:
                print(f"[SecureStorageService] Invalid MONU_SECURE_KEY environment variable: {e}. Falling back to file.")

        # 2. Try to read from local key file
        if os.path.exists(self.key_file_path):
            try:
                with open(self.key_file_path, "rb") as key_file:
                    key_bytes = key_file.read()
                    return Fernet(key_bytes)
            except Exception as e:
                print(f"[SecureStorageService] Error reading key file: {e}. Generating new key.")

        # 3. Generate a new key and save it securely
        new_key_bytes = Fernet.generate_key()
        try:
            with open(self.key_file_path, "wb") as key_file:
                key_file.write(new_key_bytes)
            # Set read/write permissions only for owner
            os.chmod(self.key_file_path, 0o600)
            print(f"[SecureStorageService] Created new encryption key at {self.key_file_path}")
        except Exception as e:
            print(f"[SecureStorageService] Failed to write key file securely: {e}")
            
        return Fernet(new_key_bytes)

    def encrypt(self, plain_text: str) -> str:
        """Encrypts plain text and returns a URL-safe base64 encoded string."""
        if not plain_text:
            return ""
        try:
            encrypted_bytes = self.fernet.encrypt(plain_text.encode())
            return encrypted_bytes.decode()
        except Exception as e:
            print(f"[SecureStorageService] Encryption failed: {e}")
            raise ValueError("Failed to encrypt data securely.")

    def decrypt(self, encrypted_text: str) -> str:
        """Decrypts a Fernet encrypted string back to plain text."""
        if not encrypted_text:
            return ""
        try:
            decrypted_bytes = self.fernet.decrypt(encrypted_text.encode())
            return decrypted_bytes.decode()
        except Exception as e:
            print(f"[SecureStorageService] Decryption failed: {e}")
            raise ValueError("Failed to decrypt data securely. Key might be invalid or data was tampered with.")

secure_storage_service = SecureStorageService()
