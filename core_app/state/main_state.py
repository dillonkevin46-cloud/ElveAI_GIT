import reflex as rx
from sqlmodel import select
from core_app.models.base import User, ChatSession

class MainState(rx.State):
    current_user_id: int = 1
    user_sessions: list[ChatSession] = []

    def load_sessions(self):
        with rx.session() as session:
            user = session.get(User, self.current_user_id)
            if not user:
                user = User(id=self.current_user_id, username="Admin", email="admin@local.dev")
                session.add(user)
                session.commit()
                session.refresh(user)

            self.user_sessions = session.exec(
                select(ChatSession).where(ChatSession.user_id == self.current_user_id)
            ).all()

    def create_new_chat(self):
        with rx.session() as session:
            new_chat = ChatSession(
                session_name=f"New Chat {len(self.user_sessions) + 1}",
                user_id=self.current_user_id
            )
            session.add(new_chat)
            session.commit()
        self.load_sessions()
