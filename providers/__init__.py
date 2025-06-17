from .base import SIPProvider
from .twilio_provider import TwilioProvider

def get_provider(provider_name: str = "twilio") -> SIPProvider:
    """Factory function to get the appropriate SIP provider."""
    providers = {
        "twilio": TwilioProvider,
    }
    
    if provider_name not in providers:
        raise ValueError(f"Unsupported provider: {provider_name}. Available providers: {list(providers.keys())}")
    
    return providers[provider_name]()

__all__ = ["SIPProvider", "TwilioProvider", "get_provider"] 