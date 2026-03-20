import reflex as rx
from core_app.components.layout import base_layout
from core_app.state.main_state import MainState

@rx.page(route="/", title="Dashboard", on_load=MainState.load_sessions)
def index() -> rx.Component:
    return base_layout(
        rx.heading("Dashboard Overview"),
        rx.text("Welcome to ElveAI. Click 'New Chat' in the sidebar to generate database entries."),
        rx.stat_group(
            rx.stat(
                rx.stat_label("Total Sessions"),
                rx.stat_number(MainState.user_sessions.length()),
            )
        )
    )
