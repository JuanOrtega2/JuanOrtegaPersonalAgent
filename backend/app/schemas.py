from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class AgentState(BaseModel):
    """Estado del agente en LangGraph."""
    query: str
    context: List[str] = []
    response: str = ""
    steps: List[str] = []
    relevant: bool = True

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    steps: List[str]
    context: List[str]
