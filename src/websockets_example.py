"""
Example of websockets usage with FastAPI.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.websockets import WebSocket

app = FastAPI()


@app.get("/")
async def indexPge():
    """
    Index (start) page that shows how websockets are working.
    """

    with open("resources/templates/websockets-index.html") as template:
        page = template.read()
        template.close()

    return HTMLResponse(page)


@app.websocket("/ws")
async def websocketsEndpoint(websocket: WebSocket) -> None:
    """
    Endpoint for websockets messenger.
    """

    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


if __name__ == "__main__":
    uvicorn.run(app, port=8010, debug=True)
