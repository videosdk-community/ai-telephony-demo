import os
import logging
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Config:
    """Centralized configuration management."""
    
    # VideoSDK Configuration
    VIDEOSDK_AUTH_TOKEN = os.getenv("VIDEOSDK_AUTH_TOKEN")
    VIDEOSDK_SIP_USERNAME = os.getenv("VIDEOSDK_SIP_USERNAME")
    VIDEOSDK_SIP_PASSWORD = os.getenv("VIDEOSDK_SIP_PASSWORD")
    
    # AI Configuration
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Twilio Configuration
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
    
    @classmethod
    def validate(cls) -> None:
        """Validate that all required environment variables are set."""
        required_vars = {
            "VIDEOSDK_AUTH_TOKEN": cls.VIDEOSDK_AUTH_TOKEN,
            "VIDEOSDK_SIP_USERNAME": cls.VIDEOSDK_SIP_USERNAME,
            "VIDEOSDK_SIP_PASSWORD": cls.VIDEOSDK_SIP_PASSWORD,
            "GOOGLE_API_KEY": cls.GOOGLE_API_KEY,
            "TWILIO_SID": cls.TWILIO_ACCOUNT_SID,
            "TWILIO_AUTH_TOKEN": cls.TWILIO_AUTH_TOKEN,
            "TWILIO_NUMBER": cls.TWILIO_NUMBER,
        }
        
        missing_vars = [var_name for var_name, var_value in required_vars.items() if not var_value]
        
        if missing_vars:
            for var_name in missing_vars:
                logger.error(f"Error: Missing environment variable: {var_name}")
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        logger.info("All required environment variables are set.")

# Validate configuration on import
Config.validate() 