import json
import logging
import os
import hashlib
from cryptography.fernet import Fernet # Assuming cryptography is available

class Vault:
    def __init__(self, key_file="monu.key"):
        self.logger = logging.getLogger("Vault")
        if not os.path.exists(key_file):
            key = Fernet.generate_key()
            with open(key_file, "wb") as kf: kf.write(key)
        
        with open(key_file, "rb") as kf:
            self.cipher = Fernet(kf.read())
        self.storage_path = "/data/data/com.termux/files/home/.monu_vault"
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path, mode=0o700)

    def encrypt_and_store(self, key, data):
        encrypted_data = self.cipher.encrypt(data.encode())
        with open(os.path.join(self.storage_path, key), "wb") as f:
            f.write(encrypted_data)
        self.logger.info(f"Encrypted data stored for {key}")

    def decrypt(self, key):
        with open(os.path.join(self.storage_path, key), "rb") as f:
            return self.cipher.decrypt(f.read()).decode()
