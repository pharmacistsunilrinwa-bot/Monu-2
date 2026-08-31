from abc import ABC, abstractmethod
import logging

class ProviderAdapter(ABC):
    def __init__(self, provider_name, keys):
        self.provider_name = provider_name
        self.keys = keys # List of keys for rotation
        self.current_key_index = 0
        self.logger = logging.getLogger(provider_name)

    @abstractmethod
    def health_check(self):
        pass

    @abstractmethod
    def execute(self, task):
        pass

    def get_key(self):
        return self.keys[self.current_key_index]

    def rotate_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.keys)
        self.logger.info(f"Rotated key for {self.provider_name}")
