import unittest
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.code_tools import CodeEditorTool
from tools.research_tools import DocumentAnalyzerTool
from tools.automation_tools import TaskAutomationTool, IncomeAssistantTool
from tools.generation_tools import MediaGeneratorTool
from services.permission_service import permission_service

class TestMonuAdvancedTools(unittest.TestCase):
    def setUp(self):
        # Ensure base user_data directory exists for safe relative file checks
        os.makedirs("user_data", exist_ok=True)
        # Lock session by default
        permission_service.revoke_elevation("default")

    def test_code_editor_tool_permissions(self):
        """Test that CodeEditorTool correctly blocks standard users and allows elevated users."""
        tool = CodeEditorTool()
        
        # 1. Should fail when not elevated
        result = unittest.TestCase().run(tool.execute("default", file_path="test.py", content="print(1)", edit_type="overwrite"))
        # Wait, since tool.execute is an async function, we can run it via asyncio loop or mock it.
        # Let's write a simple async runner or call a synchronous test if we can, or use asyncio to run our tests!
        
    # Since they are async, let's use an async test runner or asyncio.run to execute the tool actions in our test methods.
    
class TestMonuAdvancedToolsAsync(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        os.makedirs("user_data", exist_ok=True)
        permission_service.revoke_elevation("default")

    async def test_code_editor_permissions(self):
        tool = CodeEditorTool()
        
        # 1. Standard mode: Should block
        res = await tool.execute("default", file_path="test_code.py", content="x = 10", edit_type="overwrite")
        self.assertFalse(res["success"])
        self.assertIn("Permission Denied", res["error"])
        
        # 2. Elevated mode: Should write
        permission_service.elevate_session("default")
        res = await tool.execute("default", file_path="test_code.py", content="x = 10", edit_type="overwrite")
        self.assertTrue(res["success"])
        self.assertIn("Successfully edited", res["message"])
        
        # Clean up
        if os.path.exists("user_data/test_code.py"):
            os.remove("user_data/test_code.py")
        permission_service.revoke_elevation("default")

    async def test_document_analyzer(self):
        tool = DocumentAnalyzerTool()
        # Should return failure for missing file gracefully
        res = await tool.execute("default", file_path="non_existent_data.csv")
        self.assertFalse(res["success"])

    async def test_task_automation(self):
        tool = TaskAutomationTool()
        res = await tool.execute("default", task_name="clean logs", parameters={"hours": 24})
        self.assertTrue(res["success"])
        self.assertEqual(res["status"], "registered")
        
        # Clean up config file
        if os.path.exists("user_data/automation_clean_logs.json"):
            os.remove("user_data/automation_clean_logs.json")

    async def test_income_assistant_find_sites(self):
        tool = IncomeAssistantTool()
        res = await tool.execute("default", domain="writing", action_type="find_sites")
        self.assertTrue(res["success"])
        self.assertEqual(res["action"], "find_sites")
        self.assertGreater(len(res["opportunities"]), 0)

    async def test_income_assistant_contract_template(self):
        tool = IncomeAssistantTool()
        res = await tool.execute("default", domain="web development", action_type="freelance_contract_template")
        self.assertTrue(res["success"])
        self.assertEqual(res["action"], "freelance_contract_template")
        self.assertIn("STANDARD FREELANCE SERVICE AGREEMENT", res["template"])

    async def test_media_generator_procedural_svg(self):
        tool = MediaGeneratorTool()
        res = await tool.execute("default", prompt="generate a line chart showing performance improvements", media_type="svg")
        self.assertTrue(res["success"])
        self.assertIn("<svg", res["svg_content"])
        self.assertIn("gen_media_default.svg", res["file_path"])
        
        # Clean up
        if os.path.exists("user_data/gen_media_default.svg"):
            os.remove("user_data/gen_media_default.svg")

if __name__ == "__main__":
    unittest.main()
