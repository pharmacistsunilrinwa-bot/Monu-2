import logging

class BaseService:
    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.info(f"{name} Initialized.")

    def log_action(self, action, details=""):
        self.logger.info(f"Action: {action} | {details}")

    def report_error(self, error_message):
        self.logger.error(f"Error in {self.name}: {error_message}")
