import os
from typing import Dict, Any, List
from backend.tools.base_tool import BaseTool
from backend.services.permission_service import PermissionLevel, permission_service

class TaskAutomationTool(BaseTool):
    @property
    def name(self) -> str:
        return "task_automation"

    @property
    def description(self) -> str:
        return "Coordinates simple automations or registers scheduled tasks inside the system database."

    @property
    def security_level(self) -> str:
        return PermissionLevel.STANDARD

    @property
    def arguments(self) -> Dict[str, Any]:
        return {
            "task_name": {
                "type": "string",
                "description": "Descriptive name of the automation task."
            },
            "parameters": {
                "type": "object",
                "description": "Arbitrary key-value parameters detailing the automation configuration."
            }
        }

    async def execute(self, user_id: str, **kwargs) -> Dict[str, Any]:
        if not permission_service.check_permission(user_id, self.security_level, f"Execute tool: {self.name}"):
            return {"success": False, "error": "Permission Denied"}

        task_name = kwargs.get("task_name")
        parameters = kwargs.get("parameters", {})
        
        if not task_name:
            return {"success": False, "error": "Missing task_name argument"}

        # Simulate task registration or setup securely
        # Always report actual factual success of setting up the automation configuration
        automation_config_file = f"automation_{task_name.lower().replace(' ', '_')}.json"
        from backend.services.file_manager_service import file_manager_service
        try:
            import json
            full_path = file_manager_service._secure_path(automation_config_file)
            with open(full_path, "w") as f:
                json.dump({
                    "task_name": task_name,
                    "parameters": parameters,
                    "status": "registered",
                    "owner": user_id
                }, f, indent=2)
                
            return {
                "success": True,
                "message": f"Successfully registered and saved task automation configuration under '{automation_config_file}'.",
                "task_name": task_name,
                "status": "registered"
            }
        except Exception as e:
            return {"success": False, "error": f"Failed to save automation: {str(e)}"}


class IncomeAssistantTool(BaseTool):
    @property
    def name(self) -> str:
        return "income_assistant"

    @property
    def description(self) -> str:
        return "Assists in lawful monetization strategies, researching micro-task opportunities, or drafting professional freelance templates."

    @property
    def security_level(self) -> str:
        return PermissionLevel.STANDARD

    @property
    def arguments(self) -> Dict[str, Any]:
        return {
            "domain": {
                "type": "string",
                "description": "Skill domain or industry (e.g. 'writing', 'data entries', 'web development', 'translation')."
            },
            "action_type": {
                "type": "string",
                "description": "What to do. Either 'find_sites' (list lawful gig/freelance sites) or 'freelance_contract_template' (generate contract format).",
                "enum": ["find_sites", "freelance_contract_template"]
            }
        }

    async def execute(self, user_id: str, **kwargs) -> Dict[str, Any]:
        if not permission_service.check_permission(user_id, self.security_level, f"Execute tool: {self.name}"):
            return {"success": False, "error": "Permission Denied"}

        domain = kwargs.get("domain", "general").lower()
        action_type = kwargs.get("action_type", "find_sites")

        if action_type == "find_sites":
            # Lawful platforms
            platforms = [
                {"name": "Upwork", "type": "General Freelance", "url": "https://www.upwork.com"},
                {"name": "Fiverr", "type": "Micro-gigs & Tasks", "url": "https://www.fiverr.com"},
                {"name": "Freelancer", "type": "Standard Gigs", "url": "https://www.freelancer.com"},
                {"name": "Toptal", "type": "Premium Tech/Design", "url": "https://www.toptal.com"},
                {"name": "ProBlogger", "type": "Content Creation & Writing", "url": "https://problogger.com/jobs/"}
            ]
            filtered = [p for p in platforms if domain in p["type"].lower() or domain in p["name"].lower() or domain == "general"]
            results = filtered if filtered else platforms
            
            return {
                "success": True,
                "domain": domain,
                "action": "find_sites",
                "opportunities": results,
                "message": "Always prioritize lawful, verified platforms. Never participate in unauthorized, high-risk, or deceptive programs."
            }

        elif action_type == "freelance_contract_template":
            # Generate standard contract template format
            template = (
                "STANDARD FREELANCE SERVICE AGREEMENT\n\n"
                "PARTIES:\n"
                "1. [Client Name] (the 'Client')\n"
                f"2. [Freelancer Name / Monu Owner] (the 'Service Provider')\n\n"
                "SERVICES:\n"
                f"The Service Provider agrees to perform services in the domain of '{domain.upper()}' as detailed in Schedule A.\n\n"
                "PAYMENT & FEES:\n"
                "All fees, milestone payments, and invoice schedules shall be specified before task delivery.\n\n"
                "INTELLECTUAL PROPERTY:\n"
                "Upon final receipt of payment, all intellectual property rights transfer to the Client.\n\n"
                "GOVERNING LAW:\n"
                "This agreement shall be governed by the local laws of the specified jurisdiction."
            )
            return {
                "success": True,
                "domain": domain,
                "action": "freelance_contract_template",
                "template": template,
                "message": "Generated basic standard service agreement structure. Adapt parameters to suit your specific contract."
            }

        return {"success": False, "error": "Invalid action_type specified."}
