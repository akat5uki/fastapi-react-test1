from typing import Dict
from fastapi import WebSocket, WebSocketException, status
from passlib.context import CryptContext

from ..schemas.auth import TokenData
from ..utilities.oauth2 import verify_websocket_access

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str) -> str:
    return pwd_context.hash(password)


def verify(plain_password: str, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


class WebSocketConnectionManager:
    def __init__(self):
        # self.active_connections: list[UserWebSocket] = []
        self.active_connections: Dict[int, WebSocket] = {}
        self.uid: int | None = None
        self.credentials_exception = WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="WebSocket Authentication failed",
        )

    async def connect(self, websocket: WebSocket):
        await websocket.accept("wamp")

    async def setWSConnection(self, token: str, websocket: WebSocket):
        token_data: TokenData = verify_websocket_access(
            token, self.credentials_exception
        )
        self.uid = token_data.id
        if token_data.id is not None and websocket is not self.active_connections.get(token_data.id):
            self.active_connections[token_data.id] = websocket

    # async def update_connections(self, websocket: WebSocket):
    #     token_data: TokenData | None = None
    #     while True:
    #         data: dict = await websocket.receive_json()
    #         print("m", data)
    #         token_data = await self.authenticate_websocket(data)
    #         if token_data is not None:
    #             break
    #         await websocket.send_json({"success": False})
    #     await websocket.send_json({"success": True})
    #     self.uid = token_data.id
    #     if self.uid is not None:
    #         self.active_connections[self.uid] = websocket

    def disconnect(self):
        if self.uid is not None:
            del self.active_connections[self.uid]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

    async def send_to_specific_user(self, message: str, idd: int):
        conn = self.active_connections.get(idd)
        if conn is not None:
            await conn.send_text(message)
