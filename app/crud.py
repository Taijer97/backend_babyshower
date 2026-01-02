from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import Message, Guest, EventConfig
from .schemas import MessageCreate, GuestCreate, RsvpUpdate, VoteUpdate, EventConfigUpdate

async def create_message(session: AsyncSession, data: MessageCreate) -> Message:
    obj = Message(content=data.content)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

async def list_messages(session: AsyncSession) -> list[Message]:
    res = await session.execute(select(Message).order_by(Message.created_at.desc()))
    return list(res.scalars().all())

async def add_guest(session: AsyncSession, data: GuestCreate) -> Guest:
    obj = Guest(name=data.name.strip())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

async def remove_guest(session: AsyncSession, guest_id: int) -> None:
    res = await session.execute(select(Guest).where(Guest.id == guest_id))
    obj = res.scalar_one_or_none()
    if obj:
        await session.delete(obj)
        await session.commit()

async def list_guests(session: AsyncSession) -> list[Guest]:
    res = await session.execute(select(Guest).order_by(Guest.created_at.desc()))
    return list(res.scalars().all())

async def update_rsvp(session: AsyncSession, guest_id: int, data: RsvpUpdate) -> Guest | None:
    res = await session.execute(select(Guest).where(Guest.id == guest_id))
    obj = res.scalar_one_or_none()
    if not obj:
        return None
    obj.rsvp = data.rsvp
    await session.commit()
    await session.refresh(obj)
    return obj

async def update_vote(session: AsyncSession, guest_id: int, data: VoteUpdate) -> Guest | None:
    res = await session.execute(select(Guest).where(Guest.id == guest_id))
    obj = res.scalar_one_or_none()
    if not obj:
        return None
    obj.vote = data.vote
    await session.commit()
    await session.refresh(obj)
    return obj

async def get_config(session: AsyncSession) -> EventConfig:
    res = await session.execute(select(EventConfig).where(EventConfig.id == 1))
    obj = res.scalar_one_or_none()
    if obj:
        return obj
    # bootstrap default config
    obj = EventConfig(
        id=1,
        title='Baby Shower & Revelación de Género',
        hosts='Kevin & Quelyn',
        date='Sábado, 24 de Octubre',
        time='4:00 PM - 9:00 PM',
        locationName='Jardín Las Rosas - Huancayo',
        address='Av. Principal #123, Huancayo, Huancayo',
        registry='Biberon\nRopa Neutral (0-6m)\nPañales Etapa 1'
    )
    session.add(obj)
    await session.commit()
    return obj

async def update_config(session: AsyncSession, data: EventConfigUpdate) -> EventConfig:
    res = await session.execute(select(EventConfig).where(EventConfig.id == 1))
    obj = res.scalar_one_or_none()
    if not obj:
        obj = EventConfig(id=1, **data.model_dump())
        session.add(obj)
    else:
        for k, v in data.model_dump().items():
            setattr(obj, k, v)
    await session.commit()
    await session.refresh(obj)
    return obj
