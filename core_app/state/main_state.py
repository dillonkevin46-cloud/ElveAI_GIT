import reflex as rx
import ollama
from sqlmodel import select
from core_app.models.base import User, ChatSession, ChatMessage

class MainState(rx.State):
    current_user_id: int = 1
    user_sessions: list[ChatSession] = []
    active_session_id: int = -1
    current_messages: list[ChatMessage] = []

    def set_active_session_id(self, session_id: int):
        self.active_session_id = session_id

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

    def select_session(self, session_id: int):
        self.active_session_id = session_id
        if self.active_session_id != -1:
            with rx.session() as session:
                self.current_messages = session.exec(
                    select(ChatMessage)
                    .where(ChatMessage.session_id == self.active_session_id)
                    .order_by(ChatMessage.created_at)
                ).all()

    def handle_submit(self, form_data: dict):
        chat_input = form_data.get("chat_input", "")
        if not chat_input or self.active_session_id == -1:
            return

        with rx.session() as session:
            # Insert user message
            user_msg = ChatMessage(
                session_id=self.active_session_id,
                role="user",
                content=chat_input
            )
            session.add(user_msg)
            session.commit()

        self.select_session(self.active_session_id)
        yield

        # Build conversation history
        messages = [{"role": msg.role, "content": msg.content} for msg in self.current_messages]

        # Call local LLM
        response = ollama.chat(model='llama3.2', messages=messages)
        ai_text = response['message']['content']

        with rx.session() as session:
            # Insert AI message
            ai_msg = ChatMessage(
                session_id=self.active_session_id,
                role="assistant",
                content=ai_text
            )
            session.add(ai_msg)
            session.commit()

        self.select_session(self.active_session_id)
        yield
