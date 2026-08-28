import os
import time
from typing import Set, Dict

class PermissionLevel:
    STANDARD = "STANDARD"  # General chat, searching files, normal analysis, memory queries
    HIGH_SECURITY = "HIGH_SECURITY"  # Run shell commands, delete files, edit code, update keys/secrets

class PermissionService:
    def __init__(self):
        # By default, the owner ID is "default" as seen in the Flutter app. 
        # This is configurable via the environment variable MONU_OWNER_ID.
        self.owner_id = os.getenv("MONU_OWNER_ID", "default")
        
        # High security session token valid for temporary execution of high-security commands
        self._active_sessions: Dict[str, float] = {}  # user_id -> expiration timestamp
        self.session_duration = 300  # 5 minutes default

    def verify_owner(self, user_id: str) -> bool:
        """Verifies if the requester is the absolute owner of this personal server."""
        return user_id == self.owner_id

    def elevate_session(self, user_id: str) -> str:
        """Temporarily elevates the session to high security, returning a simple status message."""
        if not self.verify_owner(user_id):
            raise PermissionError("Access Denied: Only the server owner can elevate permissions.")
            
        self._active_sessions[user_id] = time.time() + self.session_duration
        return "Session successfully elevated to HIGH_SECURITY for 5 minutes."

    def revoke_elevation(self, user_id: str):
        """Revokes any temporary session elevation."""
        if user_id in self._active_sessions:
            del self._active_sessions[user_id]

    def is_session_elevated(self, user_id: str) -> bool:
        """Checks if the user's session is currently elevated to high-security mode."""
        if not self.verify_owner(user_id):
            return False
        expiration = self._active_sessions.get(user_id, 0)
        if time.time() < expiration:
            return True
        # Clean up expired session
        if user_id in self._active_sessions:
            del self._active_sessions[user_id]
        return False

    def check_permission(self, user_id: str, action_level: str, detail: str = "") -> bool:
        """
        Enforces standard and high-security access control.
        If an action requires HIGH_SECURITY, it must either be explicitly authorized via an elevated session.
        """
        if not self.verify_owner(user_id):
            print(f"[PermissionService] Denied user '{user_id}' attempting action: {detail}")
            return False

        if action_level == PermissionLevel.STANDARD:
            return True

        if action_level == PermissionLevel.HIGH_SECURITY:
            if self.is_session_elevated(user_id):
                print(f"[PermissionService] Authorized HIGH_SECURITY action for {user_id}: {detail}")
                return True
            else:
                print(f"[PermissionService] BLOCKED unauthorized HIGH_SECURITY action for {user_id}: {detail}")
                return False

        return False

permission_service = PermissionService()
