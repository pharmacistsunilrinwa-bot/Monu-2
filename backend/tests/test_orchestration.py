import unittest
import sys
import os

# Ensure backend directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.services.secure_storage_service import secure_storage_service
from backend.services.permission_service import permission_service, PermissionLevel
from backend.services.orchestration_service import orchestration_service

class TestMonuServerSecurityAndOrchestration(unittest.TestCase):
    def test_secure_storage(self):
        """Test encryption and decryption of sensitive data."""
        test_secret = "monu_super_secret_preference"
        encrypted = secure_storage_service.encrypt(test_secret)
        self.assertNotEqual(test_secret, encrypted)
        
        decrypted = secure_storage_service.decrypt(encrypted)
        self.assertEqual(test_secret, decrypted)

    def test_permission_levels(self):
        """Test permission levels, owner check, and session elevation."""
        # 1. Check default owner verification
        self.assertTrue(permission_service.verify_owner("default"))
        self.assertFalse(permission_service.verify_owner("malicious_user"))

        # 2. Check standard permissions (allowed by default for owner)
        self.assertTrue(permission_service.check_permission("default", PermissionLevel.STANDARD, "test standard action"))
        self.assertFalse(permission_service.check_permission("malicious_user", PermissionLevel.STANDARD, "test standard action"))

        # 3. Check high-security permissions (blocked by default, allowed after elevation)
        self.assertFalse(permission_service.check_permission("default", PermissionLevel.HIGH_SECURITY, "test high action"))
        
        # Elevate session
        msg = permission_service.elevate_session("default")
        self.assertIn("elevated", msg.lower())
        self.assertTrue(permission_service.is_session_elevated("default"))
        
        # Now high security action should be permitted
        self.assertTrue(permission_service.check_permission("default", PermissionLevel.HIGH_SECURITY, "test high action"))
        
        # Revoke session elevation
        permission_service.revoke_elevation("default")
        self.assertFalse(permission_service.is_session_elevated("default"))
        self.assertFalse(permission_service.check_permission("default", PermissionLevel.HIGH_SECURITY, "test high action"))

    def test_decision_parsing(self):
        """Test parsing of orchestrator JSON decisions."""
        # Test valid JSON tool action
        valid_json_action = '{"action": "google_search", "arguments": {"query": "test query"}}'
        decision = orchestration_service._parse_decision(valid_json_action)
        self.assertEqual(decision["action"], "google_search")
        self.assertEqual(decision["arguments"]["query"], "test query")

        # Test valid JSON with markdown code blocks (robust extraction)
        markdown_json = '```json\n{"action": "reply", "message": "hello world"}\n```'
        decision = orchestration_service._parse_decision(markdown_json)
        self.assertEqual(decision["action"], "reply")
        self.assertEqual(decision["message"], "hello world")

        # Test invalid JSON fallback to direct reply
        invalid_json = "This is not json at all."
        decision = orchestration_service._parse_decision(invalid_json)
        self.assertEqual(decision["action"], "reply")
        self.assertEqual(decision["message"], invalid_json)

if __name__ == "__main__":
    unittest.main()
