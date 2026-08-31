from abc import ABC, abstractmethod
import logging

class BaseConnector(ABC):
    def __init__(self, platform_name):
        self.platform_name = platform_name
        self.logger = logging.getLogger(f"Connector:{platform_name}")

    @abstractmethod
    async def discover_opportunities(self):
        """Must return list of structured opportunities."""
        pass

    @abstractmethod
    async def submit_proposal(self, opportunity_id, proposal_content):
        """Must require Owner Approval gate in the calling service."""
        pass

class MockMarketplaceConnector(BaseConnector):
    async def discover_opportunities(self):
        self.logger.info("Discovering opportunities from mock source.")
        return [] # Returns empty until configured

    async def submit_proposal(self, opportunity_id, proposal_content):
        self.logger.info(f"Submitting to {opportunity_id}")
        return {"status": "SUCCESS"}
