from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class Message(BaseModel):
    role: str
    content: str

class AgentState(BaseModel):
    query: str
    history: List[Message] = Field(default_factory=list)
    context: List[Dict[str, Any]] = Field(default_factory=list, description="Retrieved documents")
    plan: List[str] = Field(default_factory=list, description="List of steps")
    current_step: Optional[str] = None
    scratchpad: Dict[str, Any] = Field(default_factory=dict, description="Intermediate results")
    final_answer: Optional[str] = None
