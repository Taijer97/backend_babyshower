import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

# Asegura imports válidos sin depender de paquete relativo
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
try:
    from backend.app.db import Base
    from backend.app.models import Message, Guest, EventConfig
except ImportError:
    from backend_bs.app.db import Base
    from backend_bs.app.models import Message, Guest, EventConfig

def normalize_url(url: str) -> str:
    if not url:
        return url
    url = url.replace("+aiomysql", "+pymysql")
    url = url.replace("+aiosqlite", "")
    return url

def pick_env_path(arg_path: str | None) -> str | None:
    if arg_path and os.path.exists(arg_path):
        return arg_path
    candidates = [
        os.path.join("backend", ".env"),
        os.path.join("backend_bs", ".env"),
        ".env",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

def main():
    env_path = pick_env_path(sys.argv[1] if len(sys.argv) > 1 else None)
    if env_path:
        load_dotenv(env_path)
    else:
        load_dotenv()
    source_url = os.getenv("SOURCE_DATABASE_URL") or "sqlite:///backend/backend.db"
    target_url = os.getenv("DATABASE_URL")
    if not target_url:
        raise RuntimeError("DATABASE_URL no está definido en .env")
    se = create_engine(normalize_url(source_url))
    te = create_engine(normalize_url(target_url))
    Base.metadata.create_all(te)
    with Session(se) as ssrc, Session(te) as sdst:
        cfgs = ssrc.execute(select(EventConfig)).scalars().all()
        for c in cfgs:
            if not sdst.get(EventConfig, c.id):
                sdst.add(EventConfig(
                    id=c.id,
                    title=c.title,
                    hosts=c.hosts,
                    date=c.date,
                    time=c.time,
                    locationName=c.locationName,
                    address=c.address,
                    registry=c.registry,
                ))
        sdst.commit()
        msgs = ssrc.execute(select(Message)).scalars().all()
        for m in msgs:
            if not sdst.get(Message, m.id):
                sdst.add(Message(id=m.id, content=m.content, created_at=m.created_at))
        sdst.commit()
        guests = ssrc.execute(select(Guest)).scalars().all()
        for g in guests:
            if not sdst.get(Guest, g.id):
                sdst.add(Guest(id=g.id, name=g.name, rsvp=g.rsvp, vote=g.vote, created_at=g.created_at))
        sdst.commit()

if __name__ == "__main__":
    main()
