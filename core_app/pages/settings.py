import reflex as rx
from core_app.components.layout import base_layout
from core_app.state.main_state import MainState
from core_app.state.auth_state import AuthState

@rx.page(route="/settings", title="Settings - ElveAI", on_load=MainState.load_sessions)
def settings() -> rx.Component:
    return base_layout(
        rx.vstack(
            rx.heading("Account Settings", size="7", margin_bottom="1em"),
            rx.card(
                rx.vstack(
                    rx.text("Profile Information", weight="bold", size="4"),
                    rx.text("Logged in as: ", rx.badge(AuthState.auth_token, color_scheme="blue")),
                    rx.divider(margin_y="1em"),
                    rx.text("Data Management", weight="bold", size="4", color="red"),
                    rx.text("Warning: This action will permanently delete all your chat sessions and messages from the local database. This cannot be undone.", size="2", color="gray"),
                    rx.button("Delete All Chat History", on_click=MainState.delete_all_chat_history, color_scheme="red", variant="solid", margin_top="1em")
                ),
                width="100%",
                max_width="600px"
            ),
            width="100%",
            align_items="flex-start"
        )
    )
