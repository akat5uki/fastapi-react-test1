from typing import Any
from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
)
from ..utilities.tools import WebSocketConnectionManager

router = APIRouter(prefix="/chat", tags=["Chat"])

manager = WebSocketConnectionManager()

@router.websocket("/", "ChatApp")
async def chat_ws(websocket: WebSocket):
    await manager.connect(websocket)
    while True:
        try:
            data: dict[str, Any] = await websocket.receive_json()
            receiver_id: int = int(data["receiver"])
            await manager.setWSConnection(data["access_token"], websocket)
            await manager.send_personal_message(f"You: {data['text']}", websocket)
            await manager.send_to_specific_user(f"#User_{manager.uid}: {data['text']}", receiver_id)
        except WebSocketDisconnect as err:
            manager.disconnect()
            # await websocket.close(1012, "WebSocket Disconnected")
            print("Error Disconnect: ", err)
            await manager.connect(websocket)
        except WebSocketException as err:
            if err.code == 1008:
                print("Websocket failed to Authenticate")
                # await websocket.close(1012, "WebSocket Disconnected")
                # await manager.connect(websocket)
            print("Error: ", err)

# @router.websocket("/", "ChatApp")
# async def broadcast_ws(websocket: WebSocket):
#     await manager.broadcast("This msg is sent to all")


# @router.websocket("/", "ChatApp")
# async def chat_ws(
#     websocket: WebSocket,
#     # db: Annotated[Session, Depends(get_db)]
# ):
#     # await websocket.accept("wamp")
#     # while True:
#     #     data = await websocket.receive_text()
#     #     print(data)
#     #     await websocket.send_text(f"Text msg : {data}")
#     # f = get_current_user("sssssss", db)
#     # print(f)
#     receiver_id: int = 0
#     await manager.connect(websocket)
#     await manager.update_connections(websocket)
#     try:
#         while True:
#             data = await websocket.receive_json()
#             print("d", data)
#             receiver_id = int(data["receiver"])
#             # print(websocket.user)
#             await manager.send_personal_message(f"You wrote: {data['text']}", websocket)
#             # await manager.broadcast(f"Client #1 says: {data}")
#             print(type(receiver_id), receiver_id)
#             await manager.send_to_specific_user(
#                 f"Message to specific user #{receiver_id}: {data['text']}", receiver_id
#             )
#     except WebSocketDisconnect:
#         manager.disconnect()
#         await manager.send_to_specific_user(
#             f"Client #{manager.uid} is offline", receiver_id
#         )
#     except WebSocketException as err:
#         print("WebSocket Error: ", err)
#     # except KeyError:
#     #     await manager.send_personal_message(
#     #         f"You: Client #{receiver_id} is offline", websocket
#     #     )
