import logging
from abc import ABC, abstractmethod

class BaseTool(ABC):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.logger = logging.getLogger(name)

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    def log_tool_action(self, action, details=""):
        self.logger.info(f"Tool: {self.name} | Action: {action} | Details: {details}")
