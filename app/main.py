import asyncio
from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from .config import settings
from .db import engine, Base, get_session
from .crud import (
    create_message, list_messages,
    add_guest, remove_guest, list_guests,
    update_rsvp, update_vote,
    get_config, update_config
)
from .schemas import (
    MessageCreate, MessageRead,
    GuestCreate, GuestRead,
    RsvpUpdate, VoteUpdate,
    EventConfigRead, EventConfigUpdate
)
from .ws import manager

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}

# Config
@app.get("/config", response_model=EventConfigRead)
async def read_config(session: AsyncSession = Depends(get_session)) -> EventConfigRead:
    cfg = await get_config(session)
    return EventConfigRead.model_validate(cfg)

@app.put("/config", response_model=EventConfigRead)
async def write_config(payload: EventConfigUpdate, session: AsyncSession = Depends(get_session)) -> EventConfigRead:
    cfg = await update_config(session, payload)
    await manager.broadcast("config_updated")
    return EventConfigRead.model_validate(cfg)

@app.post("/messages", response_model=MessageRead)
async def post_message(payload: MessageCreate, session: AsyncSession = Depends(get_session)) -> MessageRead:
    obj = await create_message(session, payload)
    await manager.broadcast(f"nuevo:{obj.id}:{obj.content}")
    return MessageRead.model_validate(obj)

@app.get("/messages", response_model=list[MessageRead])
async def get_messages(session: AsyncSession = Depends(get_session)) -> list[MessageRead]:
    objs = await list_messages(session)
    return [MessageRead.model_validate(o) for o in objs]

# Guests
@app.get("/guests", response_model=list[GuestRead])
async def get_guests(session: AsyncSession = Depends(get_session)) -> list[GuestRead]:
    objs = await list_guests(session)
    return [GuestRead.model_validate(o) for o in objs]

@app.post("/guests", response_model=GuestRead)
async def create_guest(payload: GuestCreate, session: AsyncSession = Depends(get_session)) -> GuestRead:
    obj = await add_guest(session, payload)
    await manager.broadcast(f"guest_added:{obj.id}")
    return GuestRead.model_validate(obj)

@app.delete("/guests/{guest_id}")
async def delete_guest(guest_id: int, session: AsyncSession = Depends(get_session)) -> dict:
    await remove_guest(session, guest_id)
    await manager.broadcast(f"guest_removed:{guest_id}")
    return {"ok": True}

@app.post("/guests/{guest_id}/rsvp", response_model=GuestRead)
async def set_rsvp(guest_id: int, payload: RsvpUpdate, session: AsyncSession = Depends(get_session)) -> GuestRead:
    obj = await update_rsvp(session, guest_id, payload)
    if obj:
        await manager.broadcast(f"guest_updated:{obj.id}")
        return GuestRead.model_validate(obj)
    return GuestRead.model_validate(obj)

@app.post("/guests/{guest_id}/vote", response_model=GuestRead)
async def set_vote(guest_id: int, payload: VoteUpdate, session: AsyncSession = Depends(get_session)) -> GuestRead:
    obj = await update_vote(session, guest_id, payload)
    if obj:
        await manager.broadcast(f"guest_updated:{obj.id}")
        return GuestRead.model_validate(obj)
    return GuestRead.model_validate(obj)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, client_id: str = "anon") -> None:
    await manager.connect(client_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data.startswith("ping"):
                await manager.send_to(client_id, "pong")
            elif data.startswith("simulate"):
                for i in range(1, 6):
                    await manager.send_to(client_id, f"progreso:{i}/5")
                    await asyncio.sleep(0.5)
                await manager.send_to(client_id, "finalizado")
            else:
                await manager.broadcast(f"echo:{data}")
    except WebSocketDisconnect:
        manager.disconnect(client_id)
