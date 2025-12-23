from pydantic import BaseModel
from typing import Any

class SessionResponse(BaseModel):
    """Schema for the new user session response."""
    session_id : str