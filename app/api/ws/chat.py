from fastapi import WebSocket, WebSocketDisconnect, FastAPI


def register_ws(app: FastAPI):
    @app.websocket("/ws/chat")
    async def chat(ws: WebSocket):
        await ws.accept()
        try:
            while True:
                data = await ws.receive_text()
                await ws.send_text(data)
        except WebSocketDisconnect:
            pass
