import logging

class IncomeOpportunityEngine:
    def __init__(self, memory_service):
        self.memory = memory_service
        self.connectors = []
        self.logger = logging.getLogger("IncomeOpportunityEngine")

    def register_connector(self, connector):
        self.connectors.append(connector)

    async def discover_all(self):
        all_opportunities = []
        for connector in self.connectors:
            try:
                opps = await connector.discover_opportunities()
                all_opportunities.extend(opps)
            except Exception as e:
                self.logger.error(f"Connector {connector.platform_name} failed: {e}")
        
        # Intelligence: Rank opportunities
        return self._rank_opportunities(all_opportunities)

    def _rank_opportunities(self, opportunities):
        # Implementation of ranking logic
        return sorted(opportunities, key=lambda x: x.get("expected_value", 0), reverse=True)
