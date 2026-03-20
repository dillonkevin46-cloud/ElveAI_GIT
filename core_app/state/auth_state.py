import reflex as rx
import bcrypt
from sqlmodel import select
from core_app.models.base import User

class AuthState(rx.State):
    auth_token: str = rx.Cookie("")
    auth_error: str = ""

    def login(self, form_data: dict):
        username = form_data.get("username", "")
        password = form_data.get("password", "")

        with rx.session() as session:
            user = session.exec(select(User).where(User.username == username)).first()
            if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                self.auth_token = user.username
                self.auth_error = ""
                return rx.redirect("/")
            else:
                self.auth_error = "Invalid credentials."

    def register(self, form_data: dict):
        username = form_data.get("username", "")
        email = form_data.get("email", "")
        password = form_data.get("password", "")

        if not username or not email or not password:
            self.auth_error = "All fields are required."
            return

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        with rx.session() as session:
            # Check if user exists
            existing_user = session.exec(select(User).where(User.username == username)).first()
            if existing_user:
                self.auth_error = "User already exists."
                return

            new_user = User(username=username, email=email, password_hash=hashed)
            session.add(new_user)
            session.commit()

        self.auth_token = username
        self.auth_error = ""
        return rx.redirect("/")

    def logout(self):
        self.auth_token = ""
        return rx.redirect("/login")
