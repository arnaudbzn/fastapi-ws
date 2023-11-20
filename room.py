# Room WebSockets server
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

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
