import logging
import httpx
from typing import Dict, Any
from fastapi import HTTPException
from config import Config

logger = logging.getLogger(__name__)

class VideoSDKService:
    """Service for managing VideoSDK rooms and operations."""
    
    def __init__(self):
        self.auth_token = Config.VIDEOSDK_AUTH_TOKEN
        self.base_url = "https://api.videosdk.live/v2"
    
    async def create_room(self, geo_fence: str = "us002") -> str:
        """Creates a new VideoSDK room and returns its ID."""
        url = f"{self.base_url}/rooms"
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.auth_token
        }
       
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=headers)
                response.raise_for_status()
                room_data = response.json()
                
                room_id = room_data.get("roomId")
                if not room_id:
                    raise ValueError("roomId not found in VideoSDK response.")
                
                logger.info(f"VideoSDK Room created: {room_id}")
                return room_id
                
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error creating VideoSDK room: {e.response.status_code} - {e.response.text}")
                raise HTTPException(
                    status_code=500, 
                    detail=f"Failed to create VideoSDK room: HTTP error {e.response.status_code}"
                )
            except Exception as e:
                logger.error(f"Error creating VideoSDK room: {e}")
                raise HTTPException(
                    status_code=500, 
                    detail=f"Failed to create VideoSDK room: {e}"
                )
    
    def get_sip_endpoint(self, room_id: str) -> str:
        """Generate SIP endpoint for a room."""
        return f"sip:{room_id}@sip.videosdk.live" 