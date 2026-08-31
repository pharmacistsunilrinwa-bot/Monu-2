import logging
from .base_tool import BaseTool

class ToolRegistry:
    def __init__(self):
        self.tools = {}
        self.logger = logging.getLogger("ToolRegistry")

    def register(self, tool: BaseTool):
        self.tools[tool.name] = tool
        self.logger.info(f"Registered tool: {tool.name} in category: {tool.category}")

    def get_tool(self, name):
        return self.tools.get(name)

    def find_tool_for_task(self, category):
        for tool in self.tools.values():
            if tool.category == category:
                return tool
        return None
