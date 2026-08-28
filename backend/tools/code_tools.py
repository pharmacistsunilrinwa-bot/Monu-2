import os
from typing import Dict, Any
from tools.base_tool import BaseTool
from services.permission_service import PermissionLevel, permission_service

class CodeEditorTool(BaseTool):
    @property
    def name(self) -> str:
        return "code_editor"

    @property
    def description(self) -> str:
        return "Edits or writes code to a specified file. This is a HIGH_SECURITY command and requires session elevation."

    @property
    def security_level(self) -> str:
        return PermissionLevel.HIGH_SECURITY

    @property
    def arguments(self) -> Dict[str, Any]:
        return {
            "file_path": {
                "type": "string",
                "description": "Path to the code file, relative to the secure base directory."
            },
            "content": {
                "type": "string",
                "description": "Full new code content or replacement content."
            },
            "edit_type": {
                "type": "string",
                "description": "Type of edit. Either 'overwrite' (full rewrite) or 'append'. Defaults to 'overwrite'.",
                "enum": ["overwrite", "append"]
            }
        }

    async def execute(self, user_id: str, **kwargs) -> Dict[str, Any]:
        file_path = kwargs.get("file_path")
        content = kwargs.get("content", "")
        edit_type = kwargs.get("edit_type", "overwrite")

        if not file_path:
            return {"success": False, "error": "Missing file_path argument"}

        # Check permissions
        if not permission_service.check_permission(user_id, self.security_level, f"Edit code: {file_path} via {edit_type}"):
            return {
                "success": False,
                "error": "Permission Denied: Editing source code files requires HIGH_SECURITY privilege. Please elevate your session."
            }

        # Resolve path securely
        from services.file_manager_service import file_manager_service
        try:
            full_path = file_manager_service._secure_path(file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            mode = "w" if edit_type == "overwrite" else "a"
            with open(full_path, mode, encoding="utf-8") as f:
                f.write(content)

            action_verb = "Overwrote" if edit_type == "overwrite" else "Appended to"
            return {
                "success": True,
                "message": f"Successfully edited file '{file_path}'. {action_verb} code content."
            }
        except Exception as e:
            return {"success": False, "error": f"Failed to edit file: {str(e)}"}
