import logging
import datetime

class AuditLogger:
    def __init__(self, log_file="/data/data/com.termux/files/home/.monu_audit.log"):
        self.log_file = log_file
        
    def log(self, user, action, status, details=""):
        timestamp = datetime.datetime.utcnow().isoformat()
        entry = f"{timestamp} | USER: {user} | ACTION: {action} | STATUS: {status} | DETAILS: {details}\n"
        with open(self.log_file, "a") as f:
            f.write(entry)
        logging.getLogger("Audit").info(entry.strip())
