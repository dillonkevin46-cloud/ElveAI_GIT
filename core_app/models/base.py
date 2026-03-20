import reflex as rx
from datetime import datetime
from sqlmodel import Field

class User(rx.Model, table=True):
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True)
    password_hash: str = Field(default="")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ChatSession(rx.Model, table=True):
    session_name: str
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

class ChatMessage(rx.Model, table=True):
    session_id: int = Field(foreign_key="chatsession.id")
    role: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
