import reflex as rx
from core_app.components.layout import base_layout
from core_app.state.main_state import MainState

@rx.page(route="/", title="Dashboard", on_load=MainState.load_sessions)
def index() -> rx.Component:
    return base_layout(
        rx.heading("Dashboard Overview"),
        rx.text("Welcome to ElveAI. Click 'New Chat' in the sidebar to generate database entries.", margin_bottom="2em"),
        rx.card(
            rx.vstack(
                rx.text("Total Sessions", size="2", color="gray.500"),
                rx.heading(MainState.user_sessions.length(), size="6"),
            ),
            width="250px",
        )
    )
