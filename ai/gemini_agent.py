from typing import Dict, Any
from videosdk.agents import AgentSession, RealTimePipeline
from videosdk.plugins.google import GeminiRealtime, GeminiLiveConfig
from .base_agent import AIAgent
from voice_agent import VoiceAgent
from config import Config

class GeminiAgent(AIAgent):
    """Gemini AI agent implementation."""
    
    def create_pipeline(self) -> RealTimePipeline:
        """Create and return the Gemini pipeline."""
        model = GeminiRealtime(
            model="gemini-2.0-flash-live-001",
            api_key=Config.GOOGLE_API_KEY,
            config=GeminiLiveConfig(
                voice="Leda",
                response_modalities=["AUDIO"],
            )
        )
        return RealTimePipeline(model=model)
    
    def create_session(self, room_id: str, context: Dict[str, Any]) -> AgentSession:
        """Create and return a Gemini agent session."""
        pipeline = self.create_pipeline()
        
        # Context for the agent
        agent_context = {
            "name": "VideoSDK Gemini Agent",
            "meetingId": room_id,
            "videosdk_auth": Config.VIDEOSDK_AUTH_TOKEN,
            **context
        }
        
        session = AgentSession(
            agent=VoiceAgent(context=agent_context),
            pipeline=pipeline,
            context=agent_context
        )
        
        return session
    
    def get_agent_name(self) -> str:
        """Return the agent name."""
        return "gemini" 