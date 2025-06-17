from .base_agent import AIAgent
from .gemini_agent import GeminiAgent

def get_ai_agent(agent_name: str = "gemini") -> AIAgent:
    """Factory function to get the appropriate AI agent."""
    agents = {
        "gemini": GeminiAgent,
    }
    
    if agent_name not in agents:
        raise ValueError(f"Unsupported AI agent: {agent_name}. Available agents: {list(agents.keys())}")
    
    return agents[agent_name]()

__all__ = ["AIAgent", "GeminiAgent", "get_ai_agent"] 