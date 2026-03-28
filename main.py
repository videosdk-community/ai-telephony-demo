import traceback
from videosdk.agents import Agent, AgentSession, Pipeline, JobContext, RoomOptions, WorkerJob, Options
from videosdk.plugins.google import GeminiRealtime, GeminiLiveConfig
from dotenv import load_dotenv
import os
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", handlers=[logging.StreamHandler()])
load_dotenv()

# Define the agent's behavior and personality
class MyVoiceAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are a helpful AI assistant that answers phone calls. Keep your responses concise and friendly.",
        )

    async def on_enter(self) -> None:
        await self.session.say("Hello! I'm your real-time assistant. How can I help you today?")

    async def on_exit(self) -> None:
        await self.session.say("Goodbye! It was great talking with you!")

async def start_session(context: JobContext):
    # Configure the Gemini model for real-time voice
    model = GeminiRealtime(
        model="gemini-3.1-flash-live-preview",
        api_key=os.getenv("GOOGLE_API_KEY"),
        config=GeminiLiveConfig(
            voice="Leda",
            response_modalities=["AUDIO"]
        )
    )
    pipeline = Pipeline(llm=model)
    session = AgentSession(agent=MyVoiceAgent(), pipeline=pipeline)

    await session.start(wait_for_participant=True, run_until_shutdown=True)

def make_context() -> JobContext:
    room_options = RoomOptions()
    return JobContext(room_options=room_options)

if __name__ == "__main__":
    try:
        # Register the agent with a unique ID
        options = Options(
            agent_id="MyTelephonyAgent",  # CRITICAL: Unique identifier for routing
            register=True,               # REQUIRED: Register with VideoSDK for telephony
            max_processes=10,            # Concurrent calls to handle
            host="localhost",
            port=8081,
            )            
        job = WorkerJob(entrypoint=start_session, jobctx=make_context, options=options)
        job.start()
    except Exception as e:
        traceback.print_exc()