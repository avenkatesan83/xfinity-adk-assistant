from pydantic import BaseModel
from typing import Any

class QueryRequest(BaseModel):
    """Schema for the incoming user query."""
    prompt: str
    session_id: str

class QueryResponse(BaseModel):
    """Schema for the outgoing agent response."""
    response: Any