from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    content: str

class MessageRead(BaseModel):
    id: int
    content: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class GuestCreate(BaseModel):
    name: str

class GuestRead(BaseModel):
    id: int
    name: str
    rsvp: str
    vote: str | None
    created_at: datetime

    model_config = {"from_attributes": True}

class RsvpUpdate(BaseModel):
    rsvp: str

class VoteUpdate(BaseModel):
    vote: str | None

class EventConfigRead(BaseModel):
    id: int
    title: str
    hosts: str
    date: str
    time: str
    locationName: str
    address: str
    registry: str

    model_config = {"from_attributes": True}

class EventConfigUpdate(BaseModel):
    title: str
    hosts: str
    date: str
    time: str
    locationName: str
    address: str
    registry: str
