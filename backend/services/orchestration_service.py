import json
import re
import traceback
import asyncio
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models import ChatHistory
from backend.services.gemini_service import gemini_service
from backend.services.gemini_logic_service import gemini_logic_service
from backend.services.permission_service import permission_service, PermissionLevel
from backend.services.secure_storage_service import secure_storage_service
from backend.services.task_reporter_service import task_reporter_service
from backend.tools import tools_map, get_tools_schema

class OrchestrationService:
    def __init__(self):
        pass

    async def execute_command(
        self, 
        db: AsyncSession, 
        user_id: str, 
        message: str, 
        context: str = "",
        attachment_bytes: Optional[bytes] = None,
        attachment_mime: Optional[str] = None
    ) -> str:
        """
        The main orchestration entry point. Receives the command, plans actions, 
        runs tools if needed (with permission checks), verifies outcomes, 
        and returns the final result.
        """
        message_lower = message.lower().strip()
        
        # 1. Handle Permission / Elevation Commands
        if message_lower.startswith("elevate session") or message_lower.startswith("authorize high security"):
            try:
                msg = permission_service.elevate_session(user_id)
                return f"🔓 **[SECURITY UPDATE]**\n{msg}"
            except Exception as e:
                return f"🔒 **[SECURITY ERROR]**\n{str(e)}"
                
        if message_lower.startswith("revoke session") or message_lower.startswith("lock session"):
            permission_service.revoke_elevation(user_id)
            return "🔒 **[SECURITY UPDATE]**\nHigh-security session successfully revoked and locked."

        # 2. Setup the Orchestrator loop (Max 5 reasoning steps to avoid infinite loops)
        max_steps = 5
        execution_history: List[Dict[str, Any]] = []
        is_elevated = permission_service.is_session_elevated(user_id)
        
        for step in range(max_steps):
            prompt = self._build_orchestration_prompt(
                message=message,
                context=context,
                tools_schema=get_tools_schema(),
                execution_history=execution_history,
                is_elevated=is_elevated
            )
            
            try:
                # Ask Gemini to decide on the next step
                response_text = await gemini_service.generate_content(prompt)
                decision = self._parse_decision(response_text)
                
                # Check if model chose to direct reply (or if parsing failed)
                action = decision.get("action", "reply")
                
                if action == "reply":
                    # Final output verification before sending back
                    reply_msg = decision.get("message", response_text)
                    
                    # Generate and save factual task report if we executed tools
                    if execution_history:
                        report = task_reporter_service.generate_markdown_report(message, execution_history)
                        reply_msg += report
                        
                        try:
                            await task_reporter_service.save_report(
                                db=db,
                                user_id=user_id,
                                goal=message,
                                steps=execution_history
                            )
                        except Exception as save_err:
                            print(f"[Orchestrator] Error saving task report to DB: {save_err}")
                        
                    return reply_msg
                
                # Check tool availability
                if action not in tools_map:
                    execution_history.append({
                        "tool": action,
                        "success": False,
                        "error": f"Tool '{action}' is missing or not implemented in the current modular system."
                    })
                    continue
                    
                # Execute tool
                tool = tools_map[action]
                tool_args = decision.get("arguments", {})
                
                # Verify permission level first
                has_permission = permission_service.check_permission(
                    user_id=user_id, 
                    action_level=tool.security_level, 
                    detail=f"Executing tool {tool.name} with arguments {tool_args}"
                )
                
                if not has_permission:
                    # Capture actual permission failure - NEVER fake a success report
                    execution_history.append({
                        "tool": action,
                        "success": False,
                        "error": f"Permission Denied. The command requires '{tool.security_level}' permissions. Please elevate your session by asking the owner."
                    })
                    continue
                
                # Run the tool with timeout
                try:
                    tool_result = await asyncio.wait_for(tool.execute(user_id, **tool_args), timeout=30.0)
                    execution_history.append({
                        "tool": action,
                        "success": tool_result.get("success", True),
                        "result": tool_result,
                        "error": tool_result.get("error"),
                        "message": tool_result.get("message", "Executed successfully")
                    })
                except asyncio.TimeoutError:
                    execution_history.append({
                        "tool": action,
                        "success": False,
                        "error": f"Tool execution timed out after 30 seconds."
                    })
                except Exception as tool_err:
                    execution_history.append({
                        "tool": action,
                        "success": False,
                        "error": f"Runtime exception during tool execution: {str(tool_err)}"
                    })
                    
            except Exception as e:
                print(f"[Orchestrator] Error on step {step}: {e}")
                traceback.print_exc()
                # Fallback to direct reasoning chat to preserve service continuity
                return await gemini_logic_service.reasoned_chat(
                    prompt=message,
                    context=context,
                    attachment_bytes=attachment_bytes,
                    attachment_mime=attachment_mime
                )
                
        # If we exhausted steps, generate final report of failed loop
        report = "🔄 **[Orchestrator Limit]** Max reasoning steps reached. Here is the task report:\n"
        for entry in execution_history:
            status_emoji = "✅" if entry["success"] else "❌"
            report += f"- {status_emoji} `{entry['tool']}`: {entry.get('error', 'Success')}\n"
        return report

    def _build_orchestration_prompt(
        self, 
        message: str, 
        context: str, 
        tools_schema: List[Dict[str, Any]], 
        execution_history: List[Dict[str, Any]],
        is_elevated: bool
    ) -> str:
        history_str = json.dumps(execution_history, indent=2) if execution_history else "No tools executed yet in this turn."
        elevation_status = "ELEVATED (HIGH_SECURITY commands allowed)" if is_elevated else "STANDARD (HIGH_SECURITY commands blocked)"
        
        return (
            "You are the central brain of the Monu Personal AI Orchestration Server.\n"
            "Your job is to receive user commands, plan and coordinate tasks, select and execute tools, "
            "and verify tool outputs before replying.\n\n"
            f"**Current Security Context**: User Session is {elevation_status}.\n\n"
            "**Available Tools Schema**:\n"
            f"{json.dumps(tools_schema, indent=2)}\n\n"
            "**Execution History for this request**:\n"
            f"{history_str}\n\n"
            f"**Context History**:\n{context}\n\n"
            f"**User Command**: {message}\n\n"
            "--- INSTRUCTIONS ---\n"
            "1. You can choose to run one of the available tools OR reply directly to the user.\n"
            "2. If you need a tool, you MUST output a valid JSON object matching this schema:\n"
            "{\n"
            "  \"action\": \"tool_name\",\n"
            "  \"arguments\": { ... matching tool schema ... }\n"
            "}\n"
            "3. If you have finished executing tools or don't need any tools, you MUST reply directly to the user using this JSON schema:\n"
            "{\n"
            "  \"action\": \"reply\",\n"
            "  \"message\": \"Your complete Markdown response to the user explaining findings, reports, or suggestions.\"\n"
            "}\n"
            "4. NEVER make up or fake tool results. Always state the honest outcome of actions.\n"
            "5. Make sure your output is purely the JSON block (do not wrap in markdown tags like ```json)."
        )

    def _parse_decision(self, response_text: str) -> Dict[str, Any]:
        """Robust extraction and parsing of JSON decision structure."""
        cleaned_text = response_text.strip()
        if cleaned_text.startswith("```"):
            cleaned_text = re.sub(r"^```[a-zA-Z]*\n?", "", cleaned_text)
            cleaned_text = re.sub(r"\n?```$", "", cleaned_text)
        cleaned_text = cleaned_text.strip()
        
        try:
            return json.loads(cleaned_text)
        except Exception:
            # Fallback if model did not return valid JSON - parse as standard reply
            print(f"[Orchestrator] JSON parsing failed for decision. Raw text: {response_text}")
            return {
                "action": "reply",
                "message": response_text
            }

orchestration_service = OrchestrationService()
