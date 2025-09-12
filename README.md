<div align="left">

# AI Telephony Agent

<div align="left" style="margin:0px 12px;">

Build a fully functional AI telephony agent using [VideoSDK Agent](https://github.com/videosdk-live/agents). We will cover the complete workflow, from running the agent locally to configuring SIP trunks for live inbound and outbound phone calls.

</div>
<div align="center">

![Architecture : Connecting Voice Agent to Telephony Agent](https://strapi.videosdk.live/uploads/inbound_outbound_call_c70708607c.png)

<div style="display:flex; margin: auto; justify-content: center; gap: 20px;">
<a href="https://docs.videosdk.live/telephony/introduction" target="_blank"><img src="https://img.shields.io/badge/_Documentation-4285F4?style=for-the-badge" alt="Documentation"></a>
<a href="https://youtu.be/WgEvRs0zqcI?si=YP9mFrxVMacEeBZ_" target="_blank"><img src="https://img.shields.io/badge/_Tutorials-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Video Tutorials"></a>
<a href="https://discord.gg/f2WsNDN9S5" target="_blank"><img src="https://img.shields.io/badge/_Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord Community"></a>
</div>

</div>

</div>

## Project Structure

This simple structure is our final goal for the worker. By following along, you'll create this complete project from scratch.

```
worker/
├── main.py                 # The core logic for your AI voice agent
├── requirements.txt        # Python package dependencies
└── .env.example            # Environment variables
```

## Prerequisites

- Python 3.12 or newer
- [VideoSDK Account](https://app.videosdk.live/api-keys) and [generate videosdk token ](https://docs.videosdk.live/ai_agents/authentication-and-token)
- [Google API key](https://aistudio.google.com/app/apikey) (for Gemini model)

## Running the AI Agent Locally

### 1. Setup Env. Variables

Create a `.env` file with your credentials from template `.env.example`:

```bash
VIDEOSDK_TOKEN=your_videosdk_token_here
GOOGLE_API_KEY=your_google_api_key_here
```

**API Keys** - Get [GOOGLE API KEY ↗](https://aistudio.google.com/app/apikey), and sign up to [VideoSDK Dashboard ↗](https://app.videosdk.live/api-keys) to [generate videosdk token ](https://docs.videosdk.live/ai_agents/authentication-and-token)

### 2. Create the environment

- On MacOS/Linux

```bash
python3 -m venv .venv
```

- On Windows

Next, Activate it! Command differ based on your environment

```bash
source .venv/bin/activate
```

You'll know the environment is active when you see (.venv) at the beginning of your terminal prompt.

### 3. Install Dependencies

With the virtual environment active, install the necessary Python packages listed in your requirements.txt file:

```bash
pip install -r requirements.txt
```

### 4. Run the Python Script

Finally, run the agent:

```bash
python main.py
```

This will start your agent locally and register it with VideoSDK. You should see output confirming that your agent is running and registered with the agent_id "agent1".

![Running AI Agent Locally](https://strapi.videosdk.live/uploads/run_local_agent_327c1b161c.gif)

**Important**: Keep this terminal running! Your agent needs to stay active to handle incoming calls.

## Connect Your AI Phone Agent to the Phone Network

### 1. **Set up an Inbound Gateway**

- In the [VideoSDK Dashboard ↗](https://app.videosdk.live/api-keys), go to `Telephony` > `Inbound Gateways` and click **Add**.
- Name the gateway, add your phone number, and copy the generated **Inbound Gateway URL**.
- In your SIP provider's dashboard (e.g., [Twilio ↗](https://console.twilio.com)), paste this URL into the **Origination SIP URI** field.

![Inbound Gateway](https://assets.videosdk.live/static-assets/ghost/2025/08/gif-inbound-gateway.gif)

### 2. **Set up an Outbound Gateway**

- In VideoSDK, go to `Telephony` > `Outbound Gateways` and click **Add**.
- Name the gateway and paste the **Termination SIP URI** from your SIP provider into the **Address** field.

![Outbound Gateway](https://assets.videosdk.live/static-assets/ghost/2025/08/outbound-gateway.gif)

### 3. **Create a Routing Rule**

- Go to `Telephony` > `Routing Rules` and click **Add**.
- Configure the rule:
  - **Gateway:** Choose the gateway you just created.
  - **Agent Type:** Set to `Self Hosted`.
  - **Agent ID:** Enter `agent1` (this matches the agent_id in your main.py file).
  - Click **Create** to link the gateway to your agent.

![Routing Rules](https://assets.videosdk.live/images/routing-rules.gif)

## Making an Inbound Call

Once your routing rule is configured, you can test your AI agent by making an inbound call:

1. **Call your SIP provider number** (the number you configured in your Inbound Gateway)
2. **Your AI agent will automatically answer** and start the conversation
3. **The agent will greet you** with: "Hello! I'm your real-time AI avatar assistant. How can I help you today?"
4. **You can have a conversation** with the AI agent using natural speech
5. **The agent will respond** using the Gemini Live model with voice synthesis

## Making an Outbound Call

To trigger an outbound call from your agent, you can make a simple API request to the VideoSDK SIP endpoint.

Use a `POST` request with your `VIDEOSDK_TOKEN` for authorization. In the body, specify the `gatewayId` (from your Outbound Gateway) and the phone number to call in `sipCallTo`.

```bash
curl --request POST \
  --url <https://api.videosdk.live/v2/sip/call> \
  --header 'Authorization: YOUR_VIDEOSDK_TOKEN' \
  --header 'Content-Type: application/json' \
  --data '{
    "gatewayId": "gw_123456789",
    "sipCallTo": "+14155550123"
  }'
```

## Next Step

That's it! You've successfully built a Python AI agent, run it locally, and connected it to the global telephone network for both inbound and outbound calls. Simply make a call to your SIP provider number and your AI agent will handle the conversation!

- [AI telephony agent Documentation](https://docs.videosdk.live/telephony/introduction)
- [Open Source Agent SDK](https://github.com/videosdk-live/agents)
- [Join Us on Discord](https://discord.gg/f2WsNDN9S5)
