import reflex as rx
import ollama
import PyPDF2
import io
from sqlmodel import select
from core_app.models.base import User, ChatSession, ChatMessage, Document
from core_app.state.auth_state import AuthState

class MainState(rx.State):
    user_sessions: list[ChatSession] = []
    active_session_id: int = -1
    current_messages: list[ChatMessage] = []

    selected_persona: str = "Default Assistant"
    personas: list[str] = ["Default Assistant", "Expert Coder", "Creative Writer", "Harsh Critic"]

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

            # Map selected persona to system prompt
            prompt_map = {
                "Default Assistant": "You are a helpful AI assistant.",
                "Expert Coder": "You are an elite software architect. Provide robust, scalable, and optimized code.",
                "Creative Writer": "You are a creative writing assistant. Be imaginative and eloquent.",
                "Harsh Critic": "You are a harsh critic. Be direct and point out flaws mercilessly."
            }
            system_prompt = prompt_map.get(self.selected_persona, "You are a helpful AI assistant.")

            new_chat = ChatSession(
                session_name=f"New Chat {len(self.user_sessions) + 1}",
                user_id=db_user_id,
                system_prompt=system_prompt
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

    async def handle_upload(self, files: list[rx.UploadFile]):
        if self.active_session_id == -1:
            return

        for file in files:
            file_data = await file.read()
            extracted_text = ""

            if file.filename.lower().endswith(".pdf"):
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_data))
                for page in pdf_reader.pages:
                    extracted_text += page.extract_text() + "\n"
            elif file.filename.lower().endswith(".txt"):
                extracted_text = file_data.decode("utf-8")
            else:
                continue # Unsupported file type

            with rx.session() as session:
                new_doc = Document(
                    session_id=self.active_session_id,
                    filename=file.filename,
                    content=extracted_text
                )
                session.add(new_doc)
                session.commit()

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

        # Build context
        with rx.session() as session:
            chat_session = session.exec(select(ChatSession).where(ChatSession.id == self.active_session_id)).first()
            documents = session.exec(select(Document).where(Document.session_id == self.active_session_id)).all()

            system_prompt = chat_session.system_prompt if chat_session else "You are a helpful AI assistant."
            if documents:
                doc_context = "\n\n".join([doc.content for doc in documents])
                system_prompt += f"\n\nCONTEXT FROM DOCUMENTS:\n{doc_context}"

        # Construct messages array
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend([{"role": msg.role, "content": msg.content} for msg in self.current_messages[:-1]])

        # Dynamic Renaming
        if len(self.current_messages) == 2:
            rename_res = ollama.chat(model='llama3.2', messages=[{"role": "user", "content": f"Summarize this in 3 short words for a title: {chat_input}"}])
            new_name = rename_res['message']['content'].strip()

            with rx.session() as session:
                cs = session.exec(select(ChatSession).where(ChatSession.id == self.active_session_id)).first()
                if cs:
                    cs.session_name = new_name
                    session.add(cs)
                    session.commit()

            yield await self.load_sessions()

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
                # Delete associated documents
                documents = session.exec(select(Document).where(Document.session_id == session_id)).all()
                for doc in documents:
                    session.delete(doc)

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
                    documents = session.exec(select(Document).where(Document.session_id == s.id)).all()
                    for doc in documents:
                        session.delete(doc)
                    messages = session.exec(select(ChatMessage).where(ChatMessage.session_id == s.id)).all()
                    for msg in messages:
                        session.delete(msg)
                    session.delete(s)
                session.commit()

        self.active_session_id = -1
        self.current_messages = []
        return await self.load_sessions()
