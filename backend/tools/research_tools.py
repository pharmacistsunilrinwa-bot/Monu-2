import os
from typing import Dict, Any
from tools.base_tool import BaseTool
from services.permission_service import PermissionLevel, permission_service
from services.analysis_service import analysis_service

class DocumentAnalyzerTool(BaseTool):
    @property
    def name(self) -> str:
        return "document_analyzer"

    @property
    def description(self) -> str:
        return "Analyzes structured datasets (such as CSV files) to compute statistics, correlations, column info, and details."

    @property
    def security_level(self) -> str:
        return PermissionLevel.STANDARD

    @property
    def arguments(self) -> Dict[str, Any]:
        return {
            "file_path": {
                "type": "string",
                "description": "Path to the CSV/document file relative to the secure user base directory."
            }
        }

    async def execute(self, user_id: str, **kwargs) -> Dict[str, Any]:
        if not permission_service.check_permission(user_id, self.security_level, f"Execute tool: {self.name}"):
            return {"success": False, "error": "Permission Denied"}

        file_path = kwargs.get("file_path")
        if not file_path:
            return {"success": False, "error": "Missing file_path argument"}

        from services.file_manager_service import file_manager_service
        try:
            full_path = file_manager_service._secure_path(file_path)
            if not os.path.exists(full_path):
                return {"success": False, "error": f"File '{file_path}' does not exist."}

            analysis_result = analysis_service.analyze_csv(full_path)
            return analysis_result
        except Exception as e:
            return {"success": False, "error": f"Failed to analyze document: {str(e)}"}
