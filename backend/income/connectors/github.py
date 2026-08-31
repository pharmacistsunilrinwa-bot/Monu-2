import aiohttp
import logging
from .base import BaseConnector
from ...security.secure_storage_service import SecureKeyManager

class GithubOpportunityConnector(BaseConnector):
    def __init__(self):
        super().__init__("GitHub")
        self.key_manager = SecureKeyManager()
        self.keys = self.key_manager.get_keys("GITHUB_KEY")
        self.api_url = "https://api.github.com/repos"

    async def discover_opportunities(self):
        if not self.keys: return []
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"token {self.keys[0]}"}
            async with session.get(f"{self.api_url}/search/issues?q=is:issue+is:open+label:good-first-issue", headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return [{"id": item["id"], "desc": item["title"], "url": item["url"], "expected_value": 0} for item in data.get("items", [])]
        return []

    async def submit_proposal(self, opportunity_url, proposal_content):
        if not self.keys: return {"status": "FAILED", "error": "No API Key"}
        
        # Example: Post a comment on the issue as a proposal
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"token {self.keys[0]}"}
            async with session.post(f"{opportunity_url}/comments", json={"body": proposal_content}, headers=headers) as resp:
                return {"status": "SUCCESS" if resp.status == 201 else "FAILED", "code": resp.status}
