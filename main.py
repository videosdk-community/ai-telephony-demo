import asyncio
from videosdk.agents import Agent, AgentSession, RealTimePipeline, JobContext, RoomOptions, WorkerJob, MCPServerStdio
from videosdk.plugins.google import GeminiRealtime, GeminiLiveConfig
from dotenv import load_dotenv
import requests
import os

load_dotenv(override=True)

# Agent Component
class MyVoiceAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are VideoSDK's AI Avatar Voice Agent with real-time capabilities. You are a helpful virtual assistant with a visual avatar that can answer questions about weather help with other tasks in real-time.",
        )

    async def on_enter(self) -> None:
        await self.session.say("Hello! I'm your real-time AI avatar assistant. How can I help you today?")
    
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
    room_options = RoomOptions(
        auth_token=os.getenv("VIDEOSDK_AUTH_TOKEN"),
        room_id=room_id,
        name="AI Agent",
        playground=True,
        recording=False
    )
    return JobContext(room_options=room_options)


if __name__ == "__main__":
    job = WorkerJob(entrypoint=start_session, jobctx=make_context)
    job.start() 