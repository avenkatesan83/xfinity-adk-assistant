from pydantic import BaseModel
from typing import Any

class SessionRequest(BaseModel):
    """Schema for the new user session request."""
    user_id: str

class SessionResponse(BaseModel):
    """Schema for the new user session response."""
    session_id : str