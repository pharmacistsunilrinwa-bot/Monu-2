import json
import os
import logging

class EconomicMemoryService:
    def __init__(self, storage_dir="/data/data/com.termux/files/home/.monu_economy"):
        self.storage_dir = storage_dir
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir, mode=0o700)
        self.stats_file = os.path.join(self.storage_dir, "stats.json")
        if not os.path.exists(self.stats_file):
            with open(self.stats_file, 'w') as f: json.dump({"revenue": 0.0, "costs": 0.0, "tasks": []}, f)

    def log_task(self, task_data):
        with open(self.stats_file, 'r+') as f:
            data = json.load(f)
            data["tasks"].append(task_data)
            data["revenue"] += task_data.get("payment", 0)
            data["costs"] += task_data.get("costs", 0)
            f.seek(0)
            json.dump(data, f)
            f.truncate()

    def get_stats(self):
        with open(self.stats_file, 'r') as f:
            return json.load(f)
