import reflex as rx
import ollama
from sqlmodel import select
from core_app.models.base import User, ChatSession, ChatMessage
from core_app.state.auth_state import AuthState

class MainState(rx.State):
    user_sessions: list[ChatSession] = []
    active_session_id: int = -1
    current_messages: list[ChatMessage] = []

    def set_active_session_id(self, session_id: int):
        self.active_session_id = session_id

    async def load_sessions(self):
        auth = await self.get_state(AuthState)
        if not auth.auth_token:
            return rx.redirect("/login")

        with rx.session() as session:
            user = session.exec(select(User).where(User.username == auth.auth_token)).first()
            if not user:
                return rx.redirect("/login")

            db_user_id = user.id
            self.user_sessions = session.exec(
                select(ChatSession).where(ChatSession.user_id == db_user_id)
            ).all()

    async def create_new_chat(self):
        auth = await self.get_state(AuthState)
        if not auth.auth_token:
            return rx.redirect("/login")

        with rx.session() as session:
            user = session.exec(select(User).where(User.username == auth.auth_token)).first()
            if not user:
                return rx.redirect("/login")

            db_user_id = user.id
            new_chat = ChatSession(
                session_name=f"New Chat {len(self.user_sessions) + 1}",
                user_id=db_user_id
            )
            session.add(new_chat)
            session.commit()

        return await self.load_sessions()

    def select_session(self, session_id: int):
        self.active_session_id = session_id
        if self.active_session_id != -1:
            with rx.session() as session:
                self.current_messages = session.exec(
                    select(ChatMessage)
                    .where(ChatMessage.session_id == self.active_session_id)
                    .order_by(ChatMessage.created_at)
                ).all()

    async def handle_submit(self, form_data: dict):
        chat_input = form_data.get("chat_input", "")
        if not chat_input or self.active_session_id == -1:
            return

        auth = await self.get_state(AuthState)
        if not auth.auth_token:
            yield rx.redirect("/login")
            return

        with rx.session() as session:
            user = session.exec(select(User).where(User.username == auth.auth_token)).first()
            if not user:
                yield rx.redirect("/login")
                return

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

        # Add empty AI message locally
        ai_message = ChatMessage(
            session_id=self.active_session_id,
            role="assistant",
            content=""
        )
        self.current_messages.append(ai_message)
        yield

        # Build conversation history (excluding the empty bubble)
        messages = [{"role": msg.role, "content": msg.content} for msg in self.current_messages[:-1]]

        # Call local LLM with streaming
        stream = ollama.chat(model='llama3.2', messages=messages, stream=True)

        for chunk in stream:
            self.current_messages[-1].content += chunk['message']['content']
            yield

        with rx.session() as session:
            # Persist the completed AI message
            session.add(self.current_messages[-1])
            session.commit()

    async def delete_chat(self, session_id: int):
        with rx.session() as session:
            chat_session = session.exec(select(ChatSession).where(ChatSession.id == session_id)).first()
            if chat_session:
                # Delete associated messages
                messages = session.exec(select(ChatMessage).where(ChatMessage.session_id == session_id)).all()
                for msg in messages:
                    session.delete(msg)

                # Delete session
                session.delete(chat_session)
                session.commit()

        if self.active_session_id == session_id:
            self.active_session_id = -1
            self.current_messages = []

        return await self.load_sessions()

    async def delete_all_chat_history(self):
        auth = await self.get_state(AuthState)
        if not auth.auth_token:
            return rx.redirect("/login")

        with rx.session() as session:
            user = session.exec(select(User).where(User.username == auth.auth_token)).first()
            if user:
                sessions = session.exec(select(ChatSession).where(ChatSession.user_id == user.id)).all()
                for s in sessions:
                    messages = session.exec(select(ChatMessage).where(ChatMessage.session_id == s.id)).all()
                    for msg in messages:
                        session.delete(msg)
                    session.delete(s)
                session.commit()

        self.active_session_id = -1
        self.current_messages = []
        return await self.load_sessions()
