from .base_service import BaseService

class SkillProcedureMemoryService(BaseService):
    def __init__(self):
        super().__init__("SkillProcedureMemoryService")
        self.skills = {}
    def store_skill(self, name, procedure): self.skills[name] = procedure
    def get_skill(self, name): return self.skills.get(name)

class ContextManagementService(BaseService):
    def __init__(self):
        super().__init__("ContextManagementService")
        self.context = {}
    def update_context(self, key, value): self.context[key] = value
    def get_context(self, key): return self.context.get(key)
