import subprocess
import logging
from abc import ABC, abstractmethod

class CompilerAdapter(ABC):
    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(name)

    @abstractmethod
    def compile(self, source_path, output_path):
        pass

class GCCAdapter(CompilerAdapter):
    def __init__(self):
        super().__init__("GCCAdapter")

    def compile(self, source_path, output_path):
        # Actual binary tool interaction
        result = subprocess.run(["gcc", source_path, "-o", output_path], capture_output=True)
        if result.returncode == 0:
            return {"status": "SUCCESS"}
        return {"status": "FAILED", "error": result.stderr.decode()}
