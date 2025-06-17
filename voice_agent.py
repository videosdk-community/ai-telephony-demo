import logging
from typing import Optional, List, Any
from videosdk.agents import Agent

logger = logging.getLogger(__name__)

class VoiceAgent(Agent):
    """An outbound call agent specialized for medical appointment scheduling."""

    def __init__(
        self,
        instructions: str = "You are a medical appointment scheduling assistant. Your goal is to confirm upcoming appointments (5th June 2025 at 11:00 AM) and reschedule if needed.",
        tools: Optional[List[Any]] = None,
        context: Optional[dict] = None,
    ) -> None:
        """Initialize the AppointmentSchedulingAgent."""
        super().__init__(
            instructions=instructions,
            tools=tools or []
        )
        self.context = context or {}
        self.logger = logging.getLogger(__name__)
        
    async def on_enter(self) -> None:
        """Handle agent entry into the session."""
        self.logger.info("Agent entered the session.")
        initial_greeting = self.context.get("initial_greeting", "Hello, this is Neha, calling from City Medical Center regarding your upcoming appointment. Is this a good time to speak?")
        await self.session.say(initial_greeting)

    async def on_exit(self) -> None:
        """Handle call termination."""
        self.logger.info("Call ended")