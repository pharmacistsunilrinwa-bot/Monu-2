import os
import json
import logging
import sqlite3

class SecureKeyManager:
    """Manages sensitive API keys securely."""
    def __init__(self, storage_path="/data/data/com.termux/files/home/.monu_secrets"):
        self.storage_path = storage_path
        self.logger = logging.getLogger("SecureKeyManager")
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path, mode=0o700)
            self.logger.info("Created secure secrets storage.")
            
        self.db_path = os.path.join(self.storage_path, "system_state.db")
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS task_state
                            (id INTEGER PRIMARY KEY, task_id TEXT, status TEXT, last_updated TIMESTAMP)''')
            conn.execute('''CREATE TABLE IF NOT EXISTS error_logs
                            (id INTEGER PRIMARY KEY, timestamp TIMESTAMP, error_message TEXT, resolved BOOLEAN)''')
            conn.commit()

    def get_keys(self, provider_name):
        path = os.path.join(self.storage_path, f"{provider_name}.json")
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return []

    def add_key(self, provider_name, key):
        # NOTE: Implement encryption here in a production environment
        keys = self.get_keys(provider_name)
        if key not in keys:
            keys.append(key)
            path = os.path.join(self.storage_path, f"{provider_name}.json")
            with open(path, 'w') as f:
                json.dump(keys, f)
            self.logger.info(f"Added key for {provider_name}")
            
    def update_task_state(self, task_id, status):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT OR REPLACE INTO task_state (task_id, status, last_updated) VALUES (?, ?, CURRENT_TIMESTAMP)", (task_id, status))
            conn.commit()

    def log_error(self, message):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO error_logs (timestamp, error_message, resolved) VALUES (CURRENT_TIMESTAMP, ?, 0)", (message,))
            conn.commit()
