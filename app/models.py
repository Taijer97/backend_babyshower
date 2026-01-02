from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from .db import Base

class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    content: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Guest(Base):
    __tablename__ = "guests"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    rsvp: Mapped[str] = mapped_column(String(20), default="pending")
    vote: Mapped[str | None] = mapped_column(String(10), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class EventConfig(Base):
    __tablename__ = "event_config"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    hosts: Mapped[str] = mapped_column(String(200))
    date: Mapped[str] = mapped_column(String(100))
    time: Mapped[str] = mapped_column(String(100))
    locationName: Mapped[str] = mapped_column(String(200))
    address: Mapped[str] = mapped_column(String(255))
    registry: Mapped[str] = mapped_column(String(1000))
