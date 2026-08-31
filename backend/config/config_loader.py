import json
import os

class Config:
    _config = None
    
    @classmethod
    def load(cls):
        if cls._config is None:
            path = os.path.join(os.path.dirname(__file__), 'settings.json')
            with open(path, 'r') as f:
                cls._config = json.load(f)
        return cls._config

    @classmethod
    def get(cls, key):
        return cls.load().get(key)
