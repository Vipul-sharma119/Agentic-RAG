from typing import List, Dict, Any
from app.agent.state import Message

class Memory:
    def __init__(self):
        # In-memory storage for now. In prod, use Redis/DB.
        self.conversations: Dict[str, List[Message]] = {}

    def add_message(self, session_id: str, message: Message):
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        self.conversations[session_id].append(message)

    def get_history(self, session_id: str) -> List[Message]:
        return self.conversations.get(session_id, [])

    def clear_history(self, session_id: str):
        if session_id in self.conversations:
            del self.conversations[session_id]

    def get_context_window(self, session_id: str, limit: int = 10) -> List[Message]:
        """
        Returns the last `limit` messages.
        """
        history = self.get_history(session_id)
        return history[-limit:]

# Singleton for in-memory
_memory_instance = Memory()

def get_memory() -> Memory:
    return _memory_instance
