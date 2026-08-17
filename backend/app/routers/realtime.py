import json
from typing import Dict, Set

from fastapi import APIRouter, WebSocket, WebSocketDisconnect


router = APIRouter(
    prefix="/realtime",
    tags=["Realtime"],
)


class ConnectionManager:
    def __init__(self):
        self.connections: Dict[
            int,
            Set[WebSocket],
        ] = {}

    async def connect(
        self,
        page_id: int,
        websocket: WebSocket,
    ):
        await websocket.accept()

        if page_id not in self.connections:
            self.connections[page_id] = set()

        self.connections[page_id].add(
            websocket
        )

        await self.broadcast_user_count(
            page_id
        )

    async def disconnect(
        self,
        page_id: int,
        websocket: WebSocket,
    ):
        if page_id not in self.connections:
            return

        self.connections[page_id].discard(
            websocket
        )

        if not self.connections[page_id]:
            del self.connections[page_id]
            return

        await self.broadcast_user_count(
            page_id
        )

    async def broadcast(
        self,
        page_id: int,
        message: dict,
        sender: WebSocket | None = None,
    ):
        connections = list(
            self.connections.get(
                page_id,
                set(),
            )
        )

        disconnected = []

        for connection in connections:
            if connection is sender:
                continue

            try:
                await connection.send_json(
                    message
                )
            except Exception:
                disconnected.append(
                    connection
                )

        for connection in disconnected:
            self.connections.get(
                page_id,
                set(),
            ).discard(
                connection
            )

    async def broadcast_user_count(
        self,
        page_id: int,
    ):
        count = len(
            self.connections.get(
                page_id,
                set(),
            )
        )

        await self.broadcast(
            page_id,
            {
                "type": "presence",
                "online_users": count,
            },
        )


manager = ConnectionManager()


@router.websocket(
    "/pages/{page_id}"
)
async def page_realtime_socket(
    websocket: WebSocket,
    page_id: int,
):
    await manager.connect(
        page_id,
        websocket,
    )

    try:
        while True:
            raw_message = (
                await websocket.receive_text()
            )

            try:
                data = json.loads(
                    raw_message
                )
            except json.JSONDecodeError:
                continue

            message_type = data.get(
                "type"
            )

            if message_type == "page_update":
                await manager.broadcast(
                    page_id,
                    {
                        "type": "page_update",
                        "title": data.get(
                            "title"
                        ),
                        "content": data.get(
                            "content"
                        ),
                    },
                    sender=websocket,
                )

            elif message_type == "typing":
                await manager.broadcast(
                    page_id,
                    {
                        "type": "typing",
                    },
                    sender=websocket,
                )

            elif message_type == "ping":
                await websocket.send_json(
                    {
                        "type": "pong",
                    }
                )

    except WebSocketDisconnect:
        await manager.disconnect(
            page_id,
            websocket,
        )

    except Exception:
        await manager.disconnect(
            page_id,
            websocket,
        )