import json
import os
import numpy as np
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self):
        self.memory_file = "user_memory.json"
        self.load_memory()
    
    def load_memory(self):
        """Load user memory from JSON file"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r') as f:
                    self.memory = json.load(f)
                logger.info(f"Loaded memory with {len(self.memory)} users")
            else:
                self.memory = {}
                logger.info("Created new memory storage")
        except Exception as e:
            logger.error(f"Error loading memory: {e}")
            self.memory = {}
    
    def save_memory(self):
        """Save user memory to JSON file"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.memory, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error saving memory: {e}")
    
    def get_user_memory(self, user_id: str) -> dict:
        """Get or create user memory"""
        if user_id not in self.memory:
            self.memory[user_id] = {
                "conversations": {},
                "preferences": {},
                "created_at": datetime.now().isoformat(),
                "last_active": datetime.now().isoformat()
            }
            self.save_memory()
        
        # Update last active time
        self.memory[user_id]["last_active"] = datetime.now().isoformat()
        return self.memory[user_id]
    
    def store_interaction(self, user_id: str, session_id: str, user_message: str, 
                         agent_response: str, agent_used: str):
        """Store a conversation interaction"""
        try:
            user_memory = self.get_user_memory(user_id)
            
            if session_id not in user_memory["conversations"]:
                user_memory["conversations"][session_id] = []
            
            interaction = {
                "timestamp": datetime.now().isoformat(),
                "user_message": user_message,
                "agent_response": agent_response,
                "agent_used": agent_used
            }
            
            user_memory["conversations"][session_id].append(interaction)
            self.save_memory()
            logger.info(f"Stored interaction for user {user_id} in session {session_id}")
            
        except Exception as e:
            logger.error(f"Error storing interaction: {e}")
    
    def get_conversation_history(self, user_id: str, session_id: str, limit: int = 10) -> list:
        """Get conversation history for a user session"""
        try:
            user_memory = self.get_user_memory(user_id)
            conversations = user_memory["conversations"].get(session_id, [])
            return conversations[-limit:]
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            return []
    
    def update_user_preferences(self, user_id: str, preferences: dict):
        """Update user preferences"""
        try:
            user_memory = self.get_user_memory(user_id)
            user_memory["preferences"].update(preferences)
            self.save_memory()
            logger.info(f"Updated preferences for user {user_id}")
        except Exception as e:
            logger.error(f"Error updating preferences: {e}")
    
    def get_all_users(self) -> list:
        """Get list of all user IDs"""
        return list(self.memory.keys())
    
    def cleanup_old_sessions(self, days_old: int = 30):
        """Clean up sessions older than specified days"""
        try:
            cutoff_date = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
            cleaned_count = 0
            
            for user_id, user_data in self.memory.items():
                for session_id, conversations in list(user_data["conversations"].items()):
                    if conversations:
                        last_interaction = conversations[-1]["timestamp"]
                        last_timestamp = datetime.fromisoformat(last_interaction).timestamp()
                        
                        if last_timestamp < cutoff_date:
                            del user_data["conversations"][session_id]
                            cleaned_count += 1
            
            self.save_memory()
            logger.info(f"Cleaned up {cleaned_count} old sessions")
            return cleaned_count
            
        except Exception as e:
            logger.error(f"Error cleaning old sessions: {e}")
            return 0