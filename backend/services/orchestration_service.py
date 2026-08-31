import logging
from ..agents.concrete_agents import PlannerAgent, CoderAgent
from ..intelligence.research_engine import ResearchEngine
from ..providers.provider_registry import ProviderRegistryService

class OrchestrationService:
    def __init__(self):
        self.logger = logging.getLogger("OrchestrationService")
        self.provider_registry = ProviderRegistryService()
        self.research_engine = ResearchEngine(self.provider_registry)
        self.planner = PlannerAgent("Planner", self)
        self.coder = CoderAgent("Coder", self)
        self.logger.info("MONU Orchestration Service Initialized with Agents.")

    async def handle_request(self, text):
        self.logger.info(f"Processing request: {text}")
        
        # New agent-based workflow
        # 1. Plan
        plan = await self.planner.perform({"text": text})
        
        # 2. Research (if needed)
        if "research" in text.lower():
            research = await self.research_engine.deep_research(text)
            return {"plan": plan, "research": research}
            
        return {"intent": "EXECUTE", "plan": plan}
