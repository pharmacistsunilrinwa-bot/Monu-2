from abc import ABC, abstractmethod
from typing import Dict, Any
from services.permission_service import PermissionLevel

class BaseTool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """The identifier of the tool (e.g., 'run_shell_command')."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """A brief description of what the tool does and when to use it."""
        pass

    @property
    @abstractmethod
    def security_level(self) -> str:
        """The required security level to execute this tool."""
        pass

    @property
    @abstractmethod
    def arguments(self) -> Dict[str, Any]:
        """A schema describing the tool's expected arguments (for LLM tool calling context)."""
        pass

    @abstractmethod
    async def execute(self, user_id: str, **kwargs) -> Dict[str, Any]:
        """Executes the tool with given arguments. Returns a structured result."""
        pass
