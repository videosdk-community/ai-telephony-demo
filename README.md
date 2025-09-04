<div align="left">

# AI Telephony Agent

<div align="left" style="margin:0px 12px;">

Build a fully functional AI telephony agent using [VideoSDK Agent](https://github.com/videosdk-live/agents). We will cover the complete workflow, from running the agent locally to configuring SIP trunks for live inbound and outbound phone calls.

</div>
<div align="center">

![Architecture : Connecting Voice Agent to Telephony Agent](https://strapi.videosdk.live/uploads/whatsapp_ai_agent_adf0519bcc.png)

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
├── Dockerfile              # Instructions to build the Docker container
├── main.py                 # The core logic for your AI voice agent
├── requirements.txt        # Python package dependencies
├── .env.example            # Environment variables
└── videosdk.yaml           # VideoSDK configuration for deploying the agent
```

## Prerequisites

- Python 3.12 or newer
- [VideoSDK Account](https://app.videosdk.live/api-keys) and [generate videosdk token ](https://docs.videosdk.live/ai_agents/authentication-and-token)
- [Google API key](https://aistudio.google.com/app/apikey) (for Gemini model)
- Docker (for containerization)

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

This will start your agent and connect it to a playground session, as defined by `playground=True` in the `make_context()` function in your code. You can now interact with it for initial testing before moving on to a full deployment.

## Build and Test AI Phone Agent

Before deploying our agent to the cloud, it's crucial to ensure it runs correctly on our local machine.
In your terminal, in your root directory run following command:

- Create a `deployment id` first and add to your `.yaml` file : Follow our [API Reference](https://docs.videosdk.live/api-reference/agent-cloud/create-deployment)

```bash
curl --request POST \
  --url <https://api.videosdk.live/ai/v1/ai-deployments> \
  --header 'Authorization: YOUR_VIDEOSDK_TOKEN' \
  --header 'Content-Type: application/json' \
  --data '{
		"name" : "ai-deployment-name",
		"description" : "This is a sample Deployment description."
  }'
```

- NOTE: If you get a response `{"message":"Please Enable AI Worker Services"}` then make sure to choose [PAY AS YOU GO](https://app.videosdk.live/profile/billing?page=1&perPage=20&default_action=save-card) plan

- Run AI Agent

```bash
videosdk run
```

This command reads your videosdk.yaml and Dockerfile, builds a local container, and starts your agent. You should see an output confirming that your worker is running.

![docker container build preview](https://assets.videosdk.live/static-assets/ghost/2025/08/videosdk-run.png)

## Deploy Your AI Phone Agent to the Cloud

Once you've confirmed the agent works locally, it's time to deploy it to VideoSDK's global infrastructure.

### 1. Configure the Deployment Manifest

```yaml
version: "1.0"
deployment:
  id: # your_deployment_id
  entry:
    path: main.py

deploy:
  cloud: true

env:
  path: "./.env"

secrets:
  VIDEOSDK_AUTH_TOKEN: # your_videosdk_token
```

### 2. Deploy with a Single Command

Now for the magic. Run the `deploy` command:

```python
videosdk deploy
```

The CLI will now package your worker, build the container, and upload it to the VideoSDK cloud. You'll see a live log of the progress.
Upon completion, you will get a Success! message along with your unique Worker ID.

![Deployed videosdk agent](https://assets.videosdk.live/static-assets/ghost/2025/08/videosdk-deploy-.png)

Crucial Step: Copy this Worker ID! You will need this unique identifier in the next step to connect your deployed agent to a phone number using a Routing Rule in the VideoSDK dashboard.

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
  - **Agent Type:** Set to `Cloud`.
  - **Deployment ID:** Paste the **Worker ID** from your `videosdk.yaml` file.
  - Click **Create** to link the gateway to your agent.

![Routing Rules](https://assets.videosdk.live/static-assets/ghost/2025/08/sippart05-clip-1.gif)

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

That's it! You've successfully built a Python AI agent, deployed it to the cloud, and connected it to the global telephone network for both inbound and outbound calls.

- [AI telephony agent Documentation](https://docs.videosdk.live/telephony/introduction)
- [Open Source Agent SDK](https://github.com/videosdk-live/agents)
- [Join Us on Discord](https://discord.gg/f2WsNDN9S5)
