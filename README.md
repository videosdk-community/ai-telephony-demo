<div align="left">

# AI Telephony Agent

<div align="left" style="margin:0px 12px;">

Make INBOUND and OUTBOUND calls with AI agents using VideoSDK. Supports multiple SIP providers and AI agents with a clean, extensible architecture for VoIP telephony solutions.

</div>
<div align="center">

![Architecture : Connecting Voice Agent to Telephony Agent](https://assets.videosdk.live/images/sip-telephony-agent.png)

<a href="https://docs.videosdk.live/ai_agents/introduction" target="_blank"><img src="https://img.shields.io/badge/_Documentation-4285F4?style=for-the-badge" alt="Documentation"></a>
<a href="https://www.youtube.com/playlist?list=PLrujdOR6BS_1fMqsHd9tynAg0foSRX5ti" target="_blank"><img src="https://img.shields.io/badge/_Tutorials-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Video Tutorials"></a>
<a href="https://dub.sh/o59dJJB" target="_blank"><img src="https://img.shields.io/badge/_Get_Started-4285F4?style=for-the-badge" alt="Get Started"></a>
<a href="https://discord.gg/f2WsNDN9S5" target="_blank"><img src="https://img.shields.io/badge/_Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord Community"></a>
<a href="https://pypi.org/project/videosdk-agents/" target="_blank"><img src="https://img.shields.io/badge/_pip_install-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="PyPI Package"></a>

</div>

</div>

## Installation

### Prerequisites

- Python 3.11+
- VideoSDK account
- Twilio account (SIP trunking provider)
- Google API key (for Gemini AI)

### Setup

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/ai-agent-telephony.git
cd ai-agent-telephony
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
   Create a `.env` file:

```env
# VideoSDK Configuration
VIDEOSDK_AUTH_TOKEN=your_videosdk_token
VIDEOSDK_SIP_USERNAME=your_sip_username
VIDEOSDK_SIP_PASSWORD=your_sip_password

# AI Configuration
GOOGLE_API_KEY=your_google_api_key

# Twilio SIP Trunking Configuration
TWILIO_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_NUMBER=your_twilio_number
```

4. **Run the server**

```bash
python server.py
```

The server will start on `http://localhost:8000`

## API Endpoints

### Handle Inbound Calls (SIP User Agent Server)

```bash
POST /inbound-call
```

Handles incoming calls from your SIP provider. Expects Twilio webhook parameters, either host this server or use `ngrok`:

```bash
POST <server-url>/inbound-call
```

- `CallSid`: Unique call identifier
- `From`: Caller's phone number (CLI - Calling Line Identification)
- `To`: Recipient's phone number (DID - Direct Inward Dialing)

### Initiate Outbound Calls (SIP User Agent Client)

```bash
POST /outbound-call
Content-Type: application/json

{
  "to_number": "+1234567890",
  "initial_greeting": "Hello from AI Agent!"
}
```

### Configure SIP Provider

```bash
POST /configure-provider?provider_name=twilio
```

Switch SIP providers at runtime (currently supports: `twilio`).

## Adding New SIP Providers

The modular architecture makes it easy to add new SIP providers and SIP trunking services. Here's how to add a new provider:

### 1. Create Provider Implementation

Create `providers/your_provider.py`:

```python
from typing import Dict, Any
from .base import SIPProvider
from config import Config

class YourProvider(SIPProvider):
    def __init__(self):
        self.client = self.create_client()

    def create_client(self) -> Any:
        return YourProviderClient(Config.YOUR_API_KEY)

    def generate_twiml(self, sip_endpoint: str, **kwargs) -> str:
        return f"<Response><Dial><Sip>{sip_endpoint}</Sip></Dial></Response>"

    def initiate_outbound_call(self, to_number: str, twiml: str) -> Dict[str, Any]:
        call = self.client.calls.create(
            to=to_number,
            from_=Config.YOUR_NUMBER,
            twiml=twiml
        )
        return {
            "call_sid": call.id,
            "status": call.status,
            "provider": "your_provider"
        }

    def get_provider_name(self) -> str:
        return "your_provider"
```

### 2. Update Provider Factory

Add to `providers/__init__.py`:

```python
from .your_provider import YourProvider

def get_provider(provider_name: str = "twilio") -> SIPProvider:
    providers = {
        "twilio": TwilioProvider,
        "your_provider": YourProvider,
    }
    # ... rest of function
```

### 3. Add Configuration

Update `config.py`:

```python
class Config:
    YOUR_API_KEY = os.getenv("YOUR_API_KEY")
    YOUR_NUMBER = os.getenv("YOUR_NUMBER")

    @classmethod
    def validate(cls) -> None:
        required_vars = {
            # ... existing vars
            "YOUR_API_KEY": cls.YOUR_API_KEY,
            "YOUR_NUMBER": cls.YOUR_NUMBER,
        }
        # ... rest of validation
```

## Adding New AI Agents

Similarly, you can add new AI agents for intelligent call handling:

### 1. Create AI Agent Implementation

Create `ai/your_ai_agent.py`:

```python
from typing import Dict, Any
from videosdk.agents import AgentSession, RealTimePipeline
from .base_agent import AIAgent
from voice_agent import VoiceAgent
from config import Config

class YourAIAgent(AIAgent):
    def create_pipeline(self) -> RealTimePipeline:
        model = YourAIModel(
            api_key=Config.YOUR_AI_API_KEY,
            model="your-model-name"
        )
        return RealTimePipeline(model=model)

    def create_session(self, room_id: str, context: Dict[str, Any]) -> AgentSession:
        pipeline = self.create_pipeline()
        agent_context = {
            "name": "Your AI Agent",
            "meetingId": room_id,
            "videosdk_auth": Config.VIDEOSDK_AUTH_TOKEN,
            **context
        }

        session = AgentSession(
            agent=VoiceAgent(context=agent_context),
            pipeline=pipeline,
            context=agent_context
        )
        return session

    def get_agent_name(self) -> str:
        return "your_ai_agent"
```

### 2. Update AI Agent Factory

Add to `ai/__init__.py`:

```python
from .your_ai_agent import YourAIAgent

def get_ai_agent(agent_name: str = "gemini") -> AIAgent:
    agents = {
        "gemini": GeminiAgent,
        "your_ai_agent": YourAIAgent,
    }
    # ... rest of function
```

## Testing

### Health Check

```bash
curl "http://localhost:8000/health"
```

### Outbound Call Test (SIP UAC)

```bash
curl -X POST "http://localhost:8000/outbound-call" \
  -H "Content-Type: application/json" \
  -d '{"to_number": "+1234567890", "initial_greeting": "Hello from AI Agent!"}'
```

### Switch SIP Provider

```bash
curl -X POST "http://localhost:8000/configure-provider?provider_name=twilio"
```

## 🔧 Configuration

### Environment Variables

| Variable                | Description                   | Required |
| ----------------------- | ----------------------------- | -------- |
| `VIDEOSDK_AUTH_TOKEN`   | VideoSDK authentication token | ✅       |
| `VIDEOSDK_SIP_USERNAME` | VideoSDK SIP username         | ✅       |
| `VIDEOSDK_SIP_PASSWORD` | VideoSDK SIP password         | ✅       |
| `GOOGLE_API_KEY`        | Google API key for Gemini     | ✅       |
| `TWILIO_SID`            | Twilio account SID            | ✅       |
| `TWILIO_AUTH_TOKEN`     | Twilio auth token             | ✅       |
| `TWILIO_NUMBER`         | Twilio phone number           | ✅       |

### Provider-Specific Variables

For additional SIP providers, add their specific environment variables to `config.py`.

## Features

- **SIP/VoIP Integration**: Pluggable SIP providers (Twilio, and more) with session initiation protocol support
- **AI-Powered Voice Agents**: Pluggable AI agents (Gemini, and more) for intelligent call handling
- **Real-time Voice Communication**: AI agents with real-time transport protocol (RTP) capabilities
- **Modular Architecture**: Clean separation of concerns for scalable telephony solutions
- **Runtime Configuration**: Switch SIP providers and AI agents without restart
- **VideoSDK Integration**: Seamless room creation and session management
- **Call Control**: Advanced call routing, forwarding, and transfer capabilities
- **Codec Support**: Multiple audio codecs for optimal voice quality

## Use Cases

### Customer Service (SIP-based)

- AI agents handle customer inquiries via VoIP
- 24/7 availability with SIP trunking
- Consistent service quality across PSTN and IP networks

### Appointment Scheduling

- Automated appointment booking via SIP calls
- Reminder calls using SIP user agent client
- Rescheduling assistance with DTMF support

### Surveys and Feedback

- Automated survey calls over SIP
- Customer feedback collection via VoIP
- Data collection with real-time transport protocol

### Emergency Notifications

- Automated emergency alerts via SIP trunking
- Mass notification systems using PSTN integration
- Status updates through IP multimedia subsystem (IMS)

## Architecture Benefits

1. **Separation of Concerns**: Each component has a single responsibility
2. **Extensibility**: Easy to add new SIP providers and AI agents
3. **Testability**: Components can be tested in isolation
4. **Maintainability**: Clear structure makes code easier to understand
5. **Reusability**: Components can be reused across different projects
6. **Configuration Management**: Centralized configuration with validation
7. **SIP Compliance**: Full session initiation protocol support
8. **VoIP Integration**: Seamless integration with voice over internet protocol

## Roadmap

- [ ] Add support for multiple AI agents per session
- [ ] Implement SIP-specific features (SBC, registrar, proxy server)
- [ ] Add monitoring and metrics for SIP sessions
- [ ] Create provider-specific webhook handlers
- [ ] Add support for different voice codecs per AI agent
- [ ] Implement call recording and transcription
- [ ] Add sentiment analysis for call quality
- [ ] Create web dashboard for call management
- [ ] Support for H.323 protocol integration
- [ ] Advanced call control features (forwarding, transfer, queue)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Guidelines

- Follow the existing code patterns
- Add proper error handling
- Include logging
- Update documentation
- Add tests if possible

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Made with ❤️ for the developer community**
