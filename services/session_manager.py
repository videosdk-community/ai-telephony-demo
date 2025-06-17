import logging
import asyncio
from typing import Dict, Any, Optional
from videosdk.agents import AgentSession
from ai import get_ai_agent
from config import Config

logger = logging.getLogger(__name__)

class SessionManager:
    """Manages AI agent sessions."""
    
    def __init__(self):
        self.active_sessions: Dict[str, AgentSession] = {}
    
    async def create_session(
        self, 
        room_id: str, 
        call_type: str = "inbound",
        initial_greeting: Optional[str] = None,
        ai_agent_name: str = "gemini"
    ) -> AgentSession:
        """Create and store a new AI agent session."""
        logger.info(f"Creating AI agent session for {call_type} call in room: {room_id}")
        
        try:
            # Get the AI agent
            ai_agent = get_ai_agent(ai_agent_name)
            
            # Prepare context
            context = {
                "call_type": call_type,
            }
            if initial_greeting:
                context["initial_greeting"] = initial_greeting
            
            # Create session
            session = ai_agent.create_session(room_id, context)
            
            # Store the session
            self.active_sessions[room_id] = session
            
            logger.info(f"Session created for room {room_id} using {ai_agent.get_agent_name()}")
            return session
            
        except Exception as e:
            logger.error(f"Error creating AI agent session for room {room_id}: {e}", exc_info=True)
            raise
    
    async def run_session(self, session: AgentSession, room_id: str):
        """Run the agent session and keep it alive."""
        try:
            logger.info(f"Starting session for room {room_id}...")
            await session.start()
            logger.info(f"AI Agent session for room {room_id} has ended.")
        except Exception as session_error:
            logger.error(f"Session error for room {room_id}: {session_error}", exc_info=True)
        finally:
            # Clean up the session
            self.cleanup_session(room_id)
    
    def cleanup_session(self, room_id: str):
        """Clean up a session."""
        if room_id in self.active_sessions:
            del self.active_sessions[room_id]
            logger.info(f"Session cleaned up for room {room_id}")
    
    def get_active_sessions_count(self) -> int:
        """Get the number of active sessions."""
        return len(self.active_sessions)
    
    def get_session_info(self) -> Dict[str, Any]:
        """Get information about all active sessions."""
        session_info = []
        for room_id, session in self.active_sessions.items():
            session_info.append({
                "room_id": room_id,
                "agent_type": session.agent.__class__.__name__,
                "status": "active"
            })
        return session_info 