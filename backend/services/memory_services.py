import json
import os
from .base_service import BaseService

class PersistentMemoryService(BaseService):
    def __init__(self, storage_dir="/data/data/com.termux/files/home/.monu_memory"):
        super().__init__("PersistentMemoryService")
        self.storage_dir = storage_dir
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir, mode=0o700)
        self.memory_file = os.path.join(self.storage_dir, "memory.json")
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, 'w') as f: json.dump({}, f)

    def store(self, key, value):
        with open(self.memory_file, 'r+') as f:
            data = json.load(f)
            data[key] = value
            f.seek(0)
            json.dump(data, f)
            f.truncate()

    def retrieve(self, key):
        with open(self.memory_file, 'r') as f:
            return json.load(f).get(key)

class KnowledgeBaseService(BaseService):
    def __init__(self, storage_dir="/data/data/com.termux/files/home/.monu_memory"):
        super().__init__("KnowledgeBaseService")
        self.kb_file = os.path.join(storage_dir, "kb.json")
        if not os.path.exists(self.kb_file):
            with open(self.kb_file, 'w') as f: json.dump([], f)

    def add_fact(self, fact):
        with open(self.kb_file, 'r+') as f:
            data = json.load(f)
            data.append(fact)
            f.seek(0)
            json.dump(data, f)
            f.truncate()

class KnowledgeRetrievalService(BaseService):
    def __init__(self, storage_dir="/data/data/com.termux/files/home/.monu_memory"):
        super().__init__("KnowledgeRetrievalService")
        self.kb_file = os.path.join(storage_dir, "kb.json")

    def query(self, topic):
        with open(self.kb_file, 'r') as f:
            data = json.load(f)
            return [fact for fact in data if topic.lower() in str(fact).lower()]
