from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from twilio.twiml.voice_response import VoiceResponse

class SIPProvider(ABC):
    """Base interface for SIP providers."""
    
    @abstractmethod
    def create_client(self) -> Any:
        """Create and return the provider's client instance."""
        pass
    
    @abstractmethod
    def generate_twiml(self, sip_endpoint: str, **kwargs) -> str:
        """Generate TwiML for connecting to SIP endpoint."""
        pass
    
    @abstractmethod
    def initiate_outbound_call(self, to_number: str, twiml: str) -> Dict[str, Any]:
        """Initiate an outbound call using the provider."""
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Return the provider name."""
        pass 