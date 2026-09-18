from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    query: str = Field(..., description="The user's query.", example="What is the revenue growth?")
    session_id: Optional[str] = Field("default", description="Session ID for conversation history.", example="session-123")

class Message(BaseModel):
    role: str = Field(..., description="Role of the message sender (user, assistant, system, tool).")
    content: str = Field(..., description="Content of the message.")

class ChatResponse(BaseModel):
    query: str = Field(..., description="The original query.")
    answer: Optional[str] = Field(None, description="The agent's final answer (markdown formatted).")
    plan: List[str] = Field(default_factory=list, description="The agent's execution plan steps.")
    history: List[Dict[str, Any]] = Field(..., description="Conversation history including tool calls.")
