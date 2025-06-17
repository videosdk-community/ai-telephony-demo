from typing import Optional
from pydantic import BaseModel

class OutboundCallRequest(BaseModel):
    """Request model for initiating outbound calls."""
    to_number: str
    initial_greeting: Optional[str] = None

class CallResponse(BaseModel):
    """Response model for call operations."""
    message: str
    twilio_call_sid: Optional[str] = None
    videosdk_room_id: Optional[str] = None

class SessionInfo(BaseModel):
    """Model for session information."""
    room_id: str
    call_type: str
    agent_type: str
    status: str 