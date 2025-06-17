from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from videosdk.agents import AgentSession, RealTimePipeline

class AIAgent(ABC):
    """Base interface for AI agents."""
    
    @abstractmethod
    def create_pipeline(self) -> RealTimePipeline:
        """Create and return the AI pipeline."""
        pass
    
    @abstractmethod
    def create_session(self, room_id: str, context: Dict[str, Any]) -> AgentSession:
        """Create and return an agent session."""
        pass
    
    @abstractmethod
    def get_agent_name(self) -> str:
        """Return the agent name."""
        pass 