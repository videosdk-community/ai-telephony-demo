import asyncio
import traceback
from videosdk.agents import Agent, AgentSession, RealTimePipeline, JobContext, RoomOptions, WorkerJob, MCPServerStdio, Options, Worker
from videosdk.plugins.google import GeminiRealtime, GeminiLiveConfig
from dotenv import load_dotenv
import requests
import os
import logging
logging.basicConfig(level=logging.DEBUG)

load_dotenv(override=True)

# Agent Component
class MyVoiceAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are a helpful AI assistant that answers phone calls. Keep your responses concise and friendly.",
        )

    async def on_enter(self) -> None:
        await self.session.say("Hello! I'm your real-time AI assistant. How can I help you today?")
    
    async def on_exit(self) -> None:
        await self.session.say("Goodbye! It was great talking with you!")

# Create a ROOM ID
def get_room_id() -> str:
    url = "https://api.videosdk.live/v2/rooms"
    headers = {
        "Authorization": os.getenv("VIDEOSDK_AUTH_TOKEN")
    }
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    return response.json()["roomId"]


async def start_session(context: JobContext):

    # Initialize Gemini Realtime model
    model = GeminiRealtime(
        model="gemini-2.0-flash-live-001",
        # When GOOGLE_API_KEY is set in .env - DON'T pass api_key parameter
        api_key=os.getenv("GOOGLE_API_KEY"), 
        config=GeminiLiveConfig(
            voice="Leda",  # Puck, Charon etc
            response_modalities=["AUDIO"]
        )
    )

    # Create pipeline with avatar
    pipeline = RealTimePipeline(
        model=model,
    )
    
    session = AgentSession(
        
        agent=MyVoiceAgent(),
        pipeline=pipeline
    )

    try:
        await context.connect()
        await session.start()
        await asyncio.Event().wait()
    finally:
        await session.close()
        await context.shutdown()

def make_context() -> JobContext:
    room_id = get_room_id()
    print(f"Room ID: {room_id}")
    room_options = RoomOptions(
        auth_token=os.getenv("VIDEOSDK_AUTH_TOKEN"),
        room_id=room_id,
        name="AI Agent",
        playground=True,
        recording=False, 
        
    )
    return JobContext(room_options=room_options)

if __name__ == "__main__":
    try:
        options = Options(
            agent_id="agent1",
            max_processes=1,
            register=True,
            log_level="DEBUG",
            host="localhost",   
            port=8081
        )
        job = WorkerJob(entrypoint=start_session, jobctx=lambda: make_context(), options=options)
        print(f"Job: {job}")
        job.start() 
        print(f"Job started")
    except Exception as e:
        traceback.print_exc()
        print(f"Error: {e}")