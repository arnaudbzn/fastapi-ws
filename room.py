# Room Web Socket server
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="username" autocomplete="off" placeholder="username" value="John"/>
            <input type="text" id="messageText" autocomplete="off" placeholder="Type your message..."/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messageData = JSON.parse(event.data)
                console.log("Message received", messageData)
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(messageData.from + ': ' + messageData.content)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var messageInput = document.getElementById("messageText")
                var usernameInput  = document.getElementById("username")
                ws.send(JSON.stringify({ from: usernameInput.value, content: messageInput.value}))
                messageInput.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)

# Store connected websockets
connected_websockets = set()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_websockets.add(websocket)  # Add the new client to the set

    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message: {data}")
            # Broadcast message to all connected clients
            for ws in connected_websockets:
                await ws.send_text(data)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        connected_websockets.remove(websocket)
