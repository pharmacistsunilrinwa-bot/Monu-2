import logging
from ..security.vault import Vault

class OwnerBondService:
    def __init__(self, vault: Vault):
        self.vault = vault
        self.logger = logging.getLogger("OwnerBondService")
        self.owner_data = {
            "name": "Sunil Rinwa",
            "aliases": ["Samrat", "Manoj"]
        }
        self.principles = """
        Recognize your master, understand his words, contemplate the situation, 
        make the right decisions, guide him like a true friend, and stand by 
        him forever with trust and loyalty to fulfill his objectives—going 
        to any necessary length to accomplish the master's or friend's command.
        """

    def verify_level_1(self, password):
        return password == self.vault.decrypt("level_1_pass")

    def verify_level_2(self, password):
        return password == self.vault.decrypt("level_2_pass")

    def get_principles(self):
        return self.principles

    def setup_secrets(self, l1, l2):
        self.vault.encrypt_and_store("level_1_pass", l1)
        self.vault.encrypt_and_store("level_2_pass", l2)
        self.logger.info("Secrets successfully stored in vault.")
