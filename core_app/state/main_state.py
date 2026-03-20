import reflex as rx
from sqlmodel import select
from core_app.models.base import User, ChatSession

class MainState(rx.State):
    current_user_id: int = 1
    user_sessions: list[ChatSession] = []

    def load_sessions(self):
        with rx.session() as session:
            self.user_sessions = session.exec(
                select(ChatSession).where(ChatSession.user_id == self.current_user_id)
            ).all()
