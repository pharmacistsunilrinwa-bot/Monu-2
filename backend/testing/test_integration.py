import unittest
import asyncio
from backend.services.orchestration_service import OrchestrationService
from backend.agents.concrete_agents import PlannerAgent

class TestMonuIntegration(unittest.IsolatedAsyncioTestCase):
    async def test_agent_orchestration(self):
        orchestrator = OrchestrationService()
        result = await orchestrator.handle_request("Research project structure")
        self.assertIn("plan", result)

    async def test_planner_agent(self):
        # Mock orchestrator
        class MockOrchestrator:
            provider_registry = type('MockRegistry', (), {'execute_with_failover': lambda self, p, prompt: {"data": "Step 1: Plan"}})()
        
        agent = PlannerAgent("TestPlanner", MockOrchestrator())
        result = await agent.perform({"text": "test task"})
        self.assertEqual(result["plan"], "Step 1: Plan")

if __name__ == '__main__':
    unittest.main()
