import logging
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name, orchestration_service):
        self.name = name
        self.orchestration = orchestration_service
        self.logger = logging.getLogger(name)

    @abstractmethod
    async def perform(self, task_context):
        pass

class PlannerAgent(BaseAgent):
    async def perform(self, task_context):
        self.logger.info(f"PlannerAgent: Planning task {task_context.get('id')}")
        # Orchestrator calls provider registry (e.g. GEMINI) to generate a plan
        prompt = f"Create a step-by-step plan for: {task_context.get('text')}"
        response = self.orchestration.provider_registry.execute_with_failover("GEMINI", prompt)
        return {"plan": response.get("data", "Generic Plan"), "status": "PLANNED"}

class CoderAgent(BaseAgent):
    async def perform(self, task_context):
        self.logger.info("CoderAgent: Implementing code")
        prompt = f"Write code to implement: {task_context.get('plan')}"
        response = self.orchestration.provider_registry.execute_with_failover("GEMINI", prompt)
        return {"code": response.get("data", "// Generic Code"), "status": "IMPLEMENTED"}

