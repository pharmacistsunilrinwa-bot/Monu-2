import os
import sys
import subprocess
import pkg_resources
from typing import Dict, Any
from backend.tools.base_tool import BaseTool
from backend.services.permission_service import PermissionLevel, permission_service
from backend.services.search_service import search_service

class CheckEnvironmentTool(BaseTool):
    @property
    def name(self) -> str:
        return "check_environment"

    @property
    def description(self) -> str:
        return "Checks existing tools, libraries, Python packages, and system capabilities. Use this first when you are unsure if a package or tool is available."

    @property
    def security_level(self) -> str:
        return PermissionLevel.STANDARD

    @property
    def arguments(self) -> Dict[str, Any]:
        return {
            "query": {
                "type": "string",
                "description": "Optional search query to filter installed libraries/packages (e.g. 'pandas', 'ffmpeg')."
            }
        }

    async def execute(self, user_id: str, **kwargs) -> Dict[str, Any]:
        if not permission_service.check_permission(user_id, self.security_level, f"Execute tool: {self.name}"):
            return {"success": False, "error": "Permission Denied"}
            
        query = kwargs.get("query", "").lower()
        
        # 1. Gather basic python capabilities
        installed_packages = []
        for dist in pkg_resources.working_set:
            if not query or query in dist.project_name.lower():
                installed_packages.append(f"{dist.project_name} ({dist.version})")

        # 2. Check key OS command availability
        key_commands = ["ffmpeg", "git", "curl", "node", "npm", "flutter", "sqlite3"]
        available_commands = {}
        for cmd in key_commands:
            if not query or query in cmd:
                # Check path
                which_cmd = "which" if os.name != "nt" else "where"
                try:
                    result = subprocess.run([which_cmd, cmd], capture_output=True, text=True, check=False)
                    available_commands[cmd] = result.stdout.strip() if result.returncode == 0 else "Not Available"
                except Exception:
                    available_commands[cmd] = "Unknown"

        return {
            "success": True,
            "python_version": sys.version,
            "platform": sys.platform,
            "installed_packages": installed_packages[:50] if not query else installed_packages,
            "available_system_commands": available_commands,
            "message": "Environment successfully checked. Always use standard libraries and tools when available."
        }


class GoogleSearchTool(BaseTool):
    @property
    def name(self) -> str:
        return "google_search"

    @property
    def description(self) -> str:
        return "Searches the web for up-to-date information, research, documentation, or answers using Google Search."

    @property
    def security_level(self) -> str:
        return PermissionLevel.STANDARD

    @property
    def arguments(self) -> Dict[str, Any]:
        return {
            "query": {
                "type": "string",
                "description": "The search query to search on Google."
            }
        }

    async def execute(self, user_id: str, **kwargs) -> Dict[str, Any]:
        if not permission_service.check_permission(user_id, self.security_level, f"Execute tool: {self.name}"):
            return {"success": False, "error": "Permission Denied"}
            
        query = kwargs.get("query")
        if not query:
            return {"success": False, "error": "Missing search query"}

        result = await search_service.web_search(query)
        return {
            "success": True,
            "results": result.get("results", []),
            "error": result.get("error")
        }


class RunShellCommandTool(BaseTool):
    @property
    def name(self) -> str:
        return "run_shell_command"

    @property
    def description(self) -> str:
        return "Executes an arbitrary shell command. This is a HIGH_SECURITY command and requires session elevation."

    @property
    def security_level(self) -> str:
        return PermissionLevel.HIGH_SECURITY

    @property
    def arguments(self) -> Dict[str, Any]:
        return {
            "command": {
                "type": "string",
                "description": "The exact bash shell command to execute."
            }
        }

    async def execute(self, user_id: str, **kwargs) -> Dict[str, Any]:
        command = kwargs.get("command")
        if not command:
            return {"success": False, "error": "Missing command argument"}

        # Perform the actual permission enforcement
        if not permission_service.check_permission(user_id, self.security_level, f"Run Command: {command}"):
            return {
                "success": False, 
                "error": "Permission Denied: Run Shell Command requires high-security permission level. "
                         "Please elevate your session first by asking the owner to authorize/elevate."
            }

        try:
            # Execute safely
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
            return {
                "success": True,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command execution timed out after 60 seconds."}
        except Exception as e:
            return {"success": False, "error": f"Failed to execute command: {str(e)}"}
