from sqlalchemy.future import select
from sqlalchemy.orm import Session
from . import models, schemas
from .enums import UserRole
from app.core.security import get_password_hash

# --- User CRUD ---
async def get_user_by_email(db: Session, email: str):
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalars().first()

async def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_users(db: Session, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.User).offset(skip).limit(limit))
    return result.scalars().all()

async def update_user_role(db: Session, user_id: int, role: UserRole):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    db_user = result.scalars().first()
    if db_user:
        db_user.role = role
        await db.commit()
        await db.refresh(db_user)
    return db_user

# --- Event CRUD ---
async def get_events(db: Session, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Event).offset(skip).limit(limit))
    return result.scalars().all()

async def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return db_event

async def update_event(db: Session, event_id: int, event: schemas.EventCreate):
    result = await db.execute(select(models.Event).filter(models.Event.id == event_id))
    db_event = result.scalars().first()
    if db_event:
        update_data = event.dict(exclude_none=True)
        for key, value in update_data.items():
            setattr(db_event, key, value)
        await db.commit()
        await db.refresh(db_event)
    return db_event

async def delete_event(db: Session, event_id: int):
    result = await db.execute(select(models.Event).filter(models.Event.id == event_id))
    db_event = result.scalars().first()
    if db_event:
        await db.delete(db_event)
        await db.commit()
    return db_event