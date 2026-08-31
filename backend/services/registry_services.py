from .base_service import BaseService

class CapabilityDiscoveryService(BaseService):
    def __init__(self):
        super().__init__("CapabilityDiscoveryService")
    def discover(self): return []

class ToolRegistryService(BaseService):
    def __init__(self):
        super().__init__("ToolRegistryService")
    def register(self, tool): pass

class ProviderRegistryService(BaseService):
    def __init__(self):
        super().__init__("ProviderRegistryService")
    def register(self, provider): pass
