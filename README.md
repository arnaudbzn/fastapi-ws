# FastAPI WebSockets with an AI Agent

## Overview
Minimalist FastAPI WebSockets Server with an AI Agent using an OpenAI compatible API.
The current implemention is using LM Studio API endpoint to use a local LLM.
You can customize the `PROMPT` in the agent code according to your needs.

## Setup

```sh
pip install -r requirements.txt
```

## Launch the WebSockets server in dev mode

```sh
uvicorn room:app --reload --port 8000
```

Open your web browser to access the chat room available at http://localhost:8000

## Launch the AI agent

In another terminal:

```sh
python ai_agent.py
```
