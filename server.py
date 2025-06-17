import logging
from typing import Optional
from fastapi import FastAPI, Request, Form, BackgroundTasks, HTTPException
from fastapi.responses import PlainTextResponse

# Import our modular components
from config import Config
from models import OutboundCallRequest, CallResponse, SessionInfo
from providers import get_provider
from services import VideoSDKService, SessionManager

# Configure logging
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="VideoSDK AI Agent Call Server (Modular)",
    description="Modular FastAPI server for inbound/outbound calls with VideoSDK AI Agent using different providers.",
    version="2.0.0"
)

# --- Initialize Services ---
videosdk_service = VideoSDKService()
session_manager = SessionManager()
sip_provider = get_provider("twilio")  # Default to Twilio

# --- FastAPI Endpoints ---

@app.get("/health", response_class=PlainTextResponse)
async def health_check():
    """Health check endpoint."""
    active_sessions = session_manager.get_active_sessions_count()
    return f"Server is healthy. Active sessions: {active_sessions}"

@app.get("/sessions", response_class=PlainTextResponse)
async def get_active_sessions():
    """Get information about active sessions."""
    session_info = session_manager.get_session_info()
    
    if not session_info:
        return "No active sessions"
    
    session_details = []
    for session in session_info:
        session_details.append(
            f"Room: {session['room_id']}, "
            f"Agent: {session['agent_type']}, "
            f"Status: {session['status']}"
        )
    
    return "\n".join(session_details)

@app.post("/inbound-call", response_class=PlainTextResponse)
async def inbound_call(
    request: Request,
    background_tasks: BackgroundTasks,
    CallSid: str = Form(...),
    From: str = Form(...),
    To: str = Form(...),
):
    """
    Handles incoming calls from SIP provider.
    1. Creates a VideoSDK room.
    2. Creates an AI Agent session for the room.
    3. Starts the session in a background task.
    4. Generates TwiML to connect the call to the VideoSDK SIP endpoint.
    """
    logger.info(f"Inbound call received from {From} to {To}. CallSid: {CallSid}")

    try:
        # Create VideoSDK room
        room_id = await videosdk_service.create_room()

        # Create the AI agent session
        session = await session_manager.create_session(room_id, "inbound")
        
        # Start the session in a background task
        background_tasks.add_task(session_manager.run_session, session, room_id)

        # Generate TwiML to connect the call to VideoSDK's SIP gateway
        sip_endpoint = videosdk_service.get_sip_endpoint(room_id)
        twiml = sip_provider.generate_twiml(sip_endpoint)

        logger.info(f"Responding to {sip_provider.get_provider_name()} inbound call {CallSid} with TwiML to dial SIP: {sip_endpoint}")
        return twiml

    except HTTPException as e:
        logger.error(f"Failed to handle inbound call {CallSid}: {e.detail}")
        return PlainTextResponse(f"<Response><Say>An error occurred: {e.detail}</Say></Response>", status_code=500)
    except Exception as e:
        logger.error(f"Unhandled error in inbound call {CallSid}: {e}", exc_info=True)
        return PlainTextResponse("<Response><Say>An unexpected error occurred. Please try again later.</Say></Response>", status_code=500)

@app.post("/outbound-call")
async def outbound_call(request_body: OutboundCallRequest, background_tasks: BackgroundTasks):
    """
    Initiates an outbound call using SIP provider, connecting to an AI Agent in a VideoSDK room.
    """
    to_number = request_body.to_number
    initial_greeting = request_body.initial_greeting
    logger.info(f"Request to initiate outbound call to: {to_number}")

    if not to_number:
        raise HTTPException(status_code=400, detail="'to_number' is required.")

    try:
        # Create VideoSDK room
        room_id = await videosdk_service.create_room()

        # Create the AI agent session
        session = await session_manager.create_session(
            room_id, 
            "outbound", 
            initial_greeting
        )
        
        # Start the session in a background task
        background_tasks.add_task(session_manager.run_session, session, room_id)

        # Generate TwiML for connecting to SIP endpoint
        sip_endpoint = videosdk_service.get_sip_endpoint(room_id)
        twiml = sip_provider.generate_twiml(sip_endpoint)

        logger.info(f"Outbound call SIP endpoint: {sip_endpoint}")

        # Create the outbound call via SIP provider
        call_result = sip_provider.initiate_outbound_call(to_number, twiml)

        logger.info(f"Outbound call initiated via {sip_provider.get_provider_name()} to {to_number}. "
                   f"Call SID: {call_result['call_sid']}. VideoSDK Room: {room_id}")
        
        return CallResponse(
            message="Outbound call initiated successfully",
            twilio_call_sid=call_result['call_sid'],
            videosdk_room_id=room_id
        )

    except HTTPException as e:
        logger.error(f"Failed to initiate outbound call to {to_number}: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unhandled error initiating outbound call to {to_number}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to initiate outbound call: {e}")

# --- Configuration Endpoints ---

@app.post("/configure-provider")
async def configure_provider(provider_name: str):
    """Configure the SIP provider to use."""
    global sip_provider
    try:
        sip_provider = get_provider(provider_name)
        logger.info(f"SIP provider changed to: {provider_name}")
        return {"message": f"Provider changed to {provider_name}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 