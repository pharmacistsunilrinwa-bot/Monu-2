import os
from typing import Dict, Any
from tools.base_tool import BaseTool
from services.permission_service import PermissionLevel, permission_service
from services.file_manager_service import file_manager_service

class ListFilesTool(BaseTool):
    @property
    def name(self) -> str:
        return "list_files"

    @property
    def description(self) -> str:
        return "Lists files within the authorized secure user directory."

    @property
    def security_level(self) -> str:
        return PermissionLevel.STANDARD

    @property
    def arguments(self) -> Dict[str, Any]:
        return {
            "path": {
                "type": "string",
                "description": "Optional subdirectory path relative to the base user directory (default: root)."
            }
        }

    async def execute(self, user_id: str, **kwargs) -> Dict[str, Any]:
        if not permission_service.check_permission(user_id, self.security_level, f"Execute tool: {self.name}"):
            return {"success": False, "error": "Permission Denied"}
            
        path = kwargs.get("path", "")
        try:
            files = file_manager_service.list_files(path)
            return {"success": True, "files": files}
        except Exception as e:
            return {"success": False, "error": str(e)}


class ReadFileTool(BaseTool):
    @property
    def name(self) -> str:
        return "read_file"

    @property
    def description(self) -> str:
        return "Reads the contents of a specific file in the secure user directory."

    @property
    def security_level(self) -> str:
        return PermissionLevel.STANDARD

    @property
    def arguments(self) -> Dict[str, Any]:
        return {
            "file_path": {
                "type": "string",
                "description": "The path to the file to read, relative to the secure base directory."
            }
        }

    async def execute(self, user_id: str, **kwargs) -> Dict[str, Any]:
        if not permission_service.check_permission(user_id, self.security_level, f"Execute tool: {self.name}"):
            return {"success": False, "error": "Permission Denied"}
            
        file_path = kwargs.get("file_path")
        if not file_path:
            return {"success": False, "error": "Missing file_path argument"}

        try:
            full_path = file_manager_service._secure_path(file_path)
            if not os.path.exists(full_path):
                return {"success": False, "error": f"File '{file_path}' does not exist."}
                
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            return {"success": True, "content": content}
        except Exception as e:
            return {"success": False, "error": str(e)}


class WriteFileTool(BaseTool):
    @property
    def name(self) -> str:
        return "write_file"

    @property
    def description(self) -> str:
        return "Writes content to a file in the secure user directory."

    @property
    def security_level(self) -> str:
        return PermissionLevel.STANDARD

    @property
    def arguments(self) -> Dict[str, Any]:
        return {
            "file_path": {
                "type": "string",
                "description": "The path to the file to write, relative to the secure base directory."
            },
            "content": {
                "type": "string",
                "description": "The text content to write into the file."
            }
        }

    async def execute(self, user_id: str, **kwargs) -> Dict[str, Any]:
        if not permission_service.check_permission(user_id, self.security_level, f"Execute tool: {self.name}"):
            return {"success": False, "error": "Permission Denied"}
            
        file_path = kwargs.get("file_path")
        content = kwargs.get("content", "")
        if not file_path:
            return {"success": False, "error": "Missing file_path argument"}

        try:
            full_path = file_manager_service._secure_path(file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            return {"success": True, "message": f"Successfully wrote to file '{file_path}'."}
        except Exception as e:
            return {"success": False, "error": str(e)}


class DeleteFileTool(BaseTool):
    @property
    def name(self) -> str:
        return "delete_file"

    @property
    def description(self) -> str:
        return "Deletes a file or directory. This is a HIGH_SECURITY command and requires session elevation."

    @property
    def security_level(self) -> str:
        return PermissionLevel.HIGH_SECURITY

    @property
    def arguments(self) -> Dict[str, Any]:
        return {
            "file_path": {
                "type": "string",
                "description": "The path to the file or directory to delete, relative to the secure base directory."
            }
        }

    async def execute(self, user_id: str, **kwargs) -> Dict[str, Any]:
        file_path = kwargs.get("file_path")
        if not file_path:
            return {"success": False, "error": "Missing file_path argument"}

        if not permission_service.check_permission(user_id, self.security_level, f"Delete File/Folder: {file_path}"):
            return {
                "success": False, 
                "error": "Permission Denied: Deleting files requires high-security permission level. "
                         "Please elevate your session first."
            }

        try:
            msg = file_manager_service.delete_file(file_path)
            return {"success": True, "message": msg}
        except Exception as e:
            return {"success": False, "error": str(e)}
