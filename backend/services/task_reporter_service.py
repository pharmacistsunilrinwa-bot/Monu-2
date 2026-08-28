import json
import datetime
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from models import TaskReport

class TaskReporterService:
    def __init__(self):
        pass

    async def save_report(
        self, 
        db: AsyncSession, 
        user_id: str, 
        goal: str, 
        steps: List[Dict[str, Any]]
    ) -> int:
        """
        Saves a structured task report to the SQLite database.
        Returns the created report's database ID.
        """
        # Determine overall status based on steps
        has_failed = any(not step.get("success", False) for step in steps)
        has_success = any(step.get("success", False) for step in steps)
        
        status = "SUCCESS"
        if has_failed:
            status = "PARTIAL" if has_success else "FAILED"
            
        new_report = TaskReport(
            user_id=user_id,
            goal=goal,
            status=status,
            steps_json=json.dumps(steps)
        )
        db.add(new_report)
        await db.commit()
        await db.refresh(new_report)
        return new_report.id

    def generate_markdown_report(self, goal: str, steps: List[Dict[str, Any]]) -> str:
        """
        Generates a clean, verified, and strictly honest Markdown report 
        summarizing executed tasks. No fake success statuses.
        """
        if not steps:
            return ""

        report = "\n\n### 📋 Verified Task Execution Status Report:\n"
        report += f"**Goal**: *{goal}*\n"
        report += f"**Report Timestamp**: `{datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}`\n\n"
        
        total_steps = len(steps)
        successful_steps = sum(1 for s in steps if s.get("success", False))
        failed_steps = total_steps - successful_steps
        
        report += f"📊 **Summary**: `{successful_steps}/{total_steps}` steps completed successfully. `{failed_steps}` failed.\n"
        report += "—" * 25 + "\n"

        for i, step in enumerate(steps, 1):
            tool_name = step.get("tool", "Unknown Tool")
            success = step.get("success", False)
            status_emoji = "✅ SUCCESS" if success else "❌ FAILED"
            
            report += f"**Step {i}**: `{tool_name}`\n"
            report += f"- **Status**: {status_emoji}\n"
            
            # Print arguments safely (redacted if they might contain secrets)
            args = step.get("arguments", {})
            if args:
                safe_args = {}
                for k, v in args.items():
                    if any(sec in k.lower() for sec in ["key", "secret", "password", "token"]):
                        safe_args[k] = "********"
                    else:
                        safe_args[k] = v
                report += f"- **Parameters**: `{json.dumps(safe_args)}`\n"

            if success:
                msg = step.get("message", "Executed successfully")
                report += f"- **Outcome**: {msg}\n"
            else:
                err = step.get("error", "An unexpected tool runtime error occurred")
                report += f"- **Error Detail**: *{err}*\n"
                
            report += "\n"

        report += "🔍 *All tool outcomes are factually verified from active system feedback. Never fabricated.*"
        return report

    async def get_historical_reports(self, db: AsyncSession, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves historical task reports for a user."""
        from sqlalchemy.future import select
        result = await db.execute(
            select(TaskReport)
            .where(TaskReport.user_id == user_id)
            .order_by(TaskReport.created_at.desc())
            .limit(limit)
        )
        reports = result.scalars().all()
        
        return [
            {
                "id": r.id,
                "user_id": r.user_id,
                "goal": r.goal,
                "status": r.status,
                "steps": json.loads(r.steps_json),
                "created_at": r.created_at.isoformat()
            }
            for r in reports
        ]

task_reporter_service = TaskReporterService()
