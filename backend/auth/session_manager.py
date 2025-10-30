import secrets
import time
from typing import Dict, Optional

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, dict] = {}
        self.session_timeout = 24 * 60 * 60
    
    def create_session(self, user_id: str, user_data: dict) -> str:
        session_id = secrets.token_urlsafe(32)
        self.sessions[session_id] = {
            'user_id': user_id,
            'user_data': user_data,
            'created_at': time.time(),
            'last_accessed': time.time()
        }
        return session_id
    
    def get_session(self, session_id: str) -> Optional[dict]:
        session = self.sessions.get(session_id)
        if session:
            if time.time() - session['last_accessed'] > self.session_timeout:
                del self.sessions[session_id]
                return None
            
            session['last_accessed'] = time.time()
            return session
        return None
    
    def delete_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]