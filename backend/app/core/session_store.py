"""
In-memory session store for conversation persistence.
For production, replace with Redis or a database-backed store.
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field
import logging
import threading

logger = logging.getLogger(__name__)


class SessionMessage(BaseModel):
    role: str
    content: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SessionData(BaseModel):
    session_id: str
    messages: List[SessionMessage] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SessionStore:
    """Thread-safe in-memory session store."""
    
    def __init__(self):
        self._sessions: Dict[str, SessionData] = {}
        self._lock = threading.Lock()
    
    def get_or_create(self, session_id: str) -> SessionData:
        with self._lock:
            if session_id not in self._sessions:
                self._sessions[session_id] = SessionData(session_id=session_id)
                logger.info(f"Created new session: {session_id}")
            return self._sessions[session_id]
    
    def add_messages(self, session_id: str, messages: List[Dict[str, str]]) -> None:
        with self._lock:
            session = self._sessions.get(session_id)
            if session:
                for msg in messages:
                    session.messages.append(SessionMessage(
                        role=msg["role"],
                        content=msg["content"]
                    ))
                session.updated_at = datetime.now(timezone.utc).isoformat()
    
    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        with self._lock:
            session = self._sessions.get(session_id)
            if not session:
                return []
            return [{"role": m.role, "content": m.content} for m in session.messages]
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        with self._lock:
            result = []
            for sid, session in self._sessions.items():
                # Get preview from first user message
                preview = ""
                for msg in session.messages:
                    if msg.role == "user":
                        preview = msg.content[:100]
                        break
                
                result.append({
                    "session_id": sid,
                    "preview": preview or "Empty session",
                    "message_count": len(session.messages),
                    "created_at": session.created_at,
                    "updated_at": session.updated_at,
                })
            
            # Sort by updated_at descending
            result.sort(key=lambda x: x["updated_at"], reverse=True)
            return result
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            session = self._sessions.get(session_id)
            if not session:
                return None
            return {
                "session_id": session.session_id,
                "messages": [m.dict() for m in session.messages],
                "created_at": session.created_at,
                "updated_at": session.updated_at,
            }
    
    def delete_session(self, session_id: str) -> bool:
        with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
                logger.info(f"Deleted session: {session_id}")
                return True
            return False


# Singleton
_session_store: Optional[SessionStore] = None

def get_session_store() -> SessionStore:
    global _session_store
    if _session_store is None:
        _session_store = SessionStore()
    return _session_store
