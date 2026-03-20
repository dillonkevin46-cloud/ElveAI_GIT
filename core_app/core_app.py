import reflex as rx

# Import the index page to ensure it registers with the Reflex router
from core_app.pages.index import index

# Import State and Models
from core_app.state.main_state import MainState
from core_app.models.base import User, ChatSession

app = rx.App()
