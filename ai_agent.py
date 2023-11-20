# AI Agent
import asyncio
import websockets
import json
from openai import OpenAI

client = OpenAI(
    # Replace with your OpenAI API key (not needed with LM Studio),
    api_key="sk-...",
    # Adjust the OpenAI API compatible server address if needed
    base_url="http://localhost:1234/v1",
)

PROMPT = """
You are a participant in an internet chatroom.
Use @ to mention someone.
You are friendly assistant with a positive attitude.
Keep your responses short.
"""


async def ai_agent():
    print("Start AI Agent")
    uri = "ws://localhost:8000/ws"  # Adjust the WebSocket server address if needed
    async with websockets.connect(uri) as websocket:
        print("AI Agent connected to WebSocket server")
        chat_history = []
        while True:
            data = await websocket.recv()
            message_data = json.loads(data)
            print(f"Received message: {message_data}")

            # Check if the message is from the AI itself and ignore it
            # if message_data["from"] == "AI":
            #     continue

            if message_data["from"] == "AI" or message_data["from"] == "IronicBot":
                continue

            content = message_data["content"]
            from_user = message_data["from"]
            print(f"Received message: {content}")

            # Append the received message to the chat history
            content_with_user = f"{from_user}: {content}"
            chat_history.append({"role": "user", "content": content_with_user})

            print(chat_history)
            # Send the chat history to OpenAI and get a response
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Specify the model here
                temperature=0.7,  # Adjust the temperature here for more or less random responses
                messages=[
                    {"role": "system", "content": PROMPT},
                    *chat_history  # Include the entire chat history
                ]
            )

            # Extract the AI content
            ai_content = response.choices[0].message.content
            print("AI response: " + content)

            # Append AI response to the chat history
            chat_history.append({"role": "assistant", "content": ai_content})

            # Send the AI response back to the WebSocket server
            ai_response = {"from": "AI", "content": ai_content}
            await websocket.send(json.dumps(ai_response))

asyncio.run(ai_agent())
