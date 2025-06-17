from typing import Dict, Any
from twilio.rest import Client as TwilioClient
from twilio.twiml.voice_response import VoiceResponse, Dial
from .base import SIPProvider
from config import Config

class TwilioProvider(SIPProvider):
    """Twilio SIP provider implementation."""
    
    def __init__(self):
        self.client = self.create_client()
    
    def create_client(self) -> TwilioClient:
        """Create and return Twilio client instance."""
        return TwilioClient(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
    
    def generate_twiml(self, sip_endpoint: str, **kwargs) -> str:
        """Generate TwiML for connecting to SIP endpoint."""
        response = VoiceResponse()
        dial = Dial()
        dial.sip(
            sip_endpoint,
            username=Config.VIDEOSDK_SIP_USERNAME,
            password=Config.VIDEOSDK_SIP_PASSWORD,
        )
        response.append(dial)
        return str(response)
    
    def initiate_outbound_call(self, to_number: str, twiml: str) -> Dict[str, Any]:
        """Initiate an outbound call using Twilio."""
        call = self.client.calls.create(
            to=to_number,
            from_=Config.TWILIO_NUMBER,
            twiml=twiml
        )
        return {
            "call_sid": call.sid,
            "status": call.status,
            "provider": "twilio"
        }
    
    def get_provider_name(self) -> str:
        """Return the provider name."""
        return "twilio" 