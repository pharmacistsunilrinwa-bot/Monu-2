import logging
from ..providers.adapters import GeminiAdapter, CohereAdapter
from .secure_storage_service import SecureKeyManager

class ProviderRegistryService:
    def __init__(self):
        self.key_manager = SecureKeyManager()
        self.adapters = {}
        self.usage_tracking = {}
        self.logger = logging.getLogger("ProviderRegistryService")
        self.initialize_adapters()

    def initialize_adapters(self):
        # Register supported providers
        for name, adapter_class, capabilities in [
            ("GEMINI", GeminiAdapter, ["text_generation", "analysis"]), 
            ("COHERE", CohereAdapter, ["search", "summarization"])
        ]:
            keys = self.key_manager.get_keys(name)
            if keys:
                self.adapters[name] = adapter_class(name, keys)
                self.adapters[name].capabilities = capabilities
                self.usage_tracking[name] = 0
                self.logger.info(f"Initialized {name} adapter")

    def discover_capabilities(self):
        return {name: adapter.capabilities for name, adapter in self.adapters.items()}

    def execute_with_failover(self, provider_name, task):
        if provider_name not in self.adapters:
            return {"status": "ERROR", "message": "Provider not available"}
        
        adapter = self.adapters[provider_name]
        self.usage_tracking[provider_name] += 1
        
        try:
            return adapter.execute(task)
        except Exception as e:
            self.logger.warning(f"Provider {provider_name} failed. Attempting key rotation.")
            adapter.rotate_key()
            return adapter.execute(task)
