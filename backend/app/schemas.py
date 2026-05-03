from typing import List

from pydantic import BaseModel


class AgentState(BaseModel):
    """Internal state of the agent within the LangGraph workflow."""

    query: str
    context: List[str] = []
    response: str = ""
    steps: List[str] = []
    relevant: bool = True


class ChatRequest(BaseModel):
    """Request schema for the chat endpoint."""

    message: str


class ChatResponse(BaseModel):
    """Response schema for the chat endpoint containing the agent's answer and metadata."""

    response: str
    steps: List[str]
    context: List[str]
