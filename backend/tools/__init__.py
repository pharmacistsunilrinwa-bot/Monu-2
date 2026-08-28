from typing import Dict, List, Any
from tools.base_tool import BaseTool
from tools.system_tools import CheckEnvironmentTool, GoogleSearchTool, RunShellCommandTool
from tools.file_tools import ListFilesTool, ReadFileTool, WriteFileTool, DeleteFileTool
from tools.code_tools import CodeEditorTool
from tools.research_tools import DocumentAnalyzerTool
from tools.automation_tools import TaskAutomationTool, IncomeAssistantTool
from tools.generation_tools import MediaGeneratorTool

# Registry of all available Monu tools
_all_tools: List[BaseTool] = [
    CheckEnvironmentTool(),
    GoogleSearchTool(),
    RunShellCommandTool(),
    ListFilesTool(),
    ReadFileTool(),
    WriteFileTool(),
    DeleteFileTool(),
    CodeEditorTool(),
    DocumentAnalyzerTool(),
    TaskAutomationTool(),
    IncomeAssistantTool(),
    MediaGeneratorTool()
]

tools_map: Dict[str, BaseTool] = {tool.name: tool for tool in _all_tools}

def get_tools_schema() -> List[Dict[str, Any]]:
    """Returns a simplified text representation or JSON schema of available tools for the model prompt."""
    schema = []
    for tool in _all_tools:
        schema.append({
            "name": tool.name,
            "description": tool.description,
            "security_level": tool.security_level,
            "arguments": tool.arguments
        })
    return schema
