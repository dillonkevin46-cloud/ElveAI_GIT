import reflex as rx
from core_app.state.main_state import MainState
from core_app.state.auth_state import AuthState

def sidebar() -> rx.Component:
    return rx.vstack(
        rx.heading("App Logo", size="4", padding_bottom="1em"),
        rx.link(
            rx.hstack(
                rx.icon("layout-dashboard"),
                rx.text("Dashboard"),
            ),
            on_click=lambda: MainState.set_active_session_id(-1),
            href="/",
        ),
        rx.link(
            rx.hstack(
                rx.icon("settings"),
                rx.text("Settings"),
            ),
            href="/settings",
        ),
        rx.select(
            MainState.personas,
            value=MainState.selected_persona,
            on_change=MainState.set_selected_persona,
            placeholder="Select Persona...",
            width="100%"
        ),
        rx.button("New Chat", on_click=MainState.create_new_chat, width="100%", margin_y="1em"),
        rx.text("Recent Chats", size="2", weight="bold", color="gray.500"),
        rx.foreach(
            MainState.user_sessions,
            lambda session: rx.hstack(
                rx.button(
                    session.session_name,
                    on_click=lambda: MainState.select_session(session.id),
                    variant="ghost",
                    flex="1",
                    justify_content="flex-start",
                    padding_y="0.5em"
                ),
                rx.icon_button(
                    rx.icon("trash"),
                    on_click=lambda: MainState.delete_chat(session.id),
                    variant="ghost",
                    color="red",
                    size="1"
                ),
                width="100%",
                align_items="center"
            )
        ),
        rx.button(
            "Logout",
            on_click=AuthState.logout,
            width="100%",
            variant="soft",
            color_scheme="red",
            margin_top="auto"
        ),
        width="250px",
        height="100vh",
        bg="gray.50",
        padding="1em",
        position="fixed",
        top="0",
        left="0",
        align_items="flex-start",
    )

def navbar() -> rx.Component:
    return rx.hstack(
        rx.spacer(),
        rx.icon("user"),
        width="100%",
        padding="1em",
        border_bottom="1px solid #eaeaea",
    )

def base_layout(*children) -> rx.Component:
    return rx.hstack(
        sidebar(),
        rx.vstack(
            navbar(),
            rx.box(
                *children,
                padding="2em",
                width="100%",
                height="calc(100vh - 80px)",
                display="flex",
                flex_direction="column",
            ),
            margin_left="250px",
            width="100%",
            min_height="100vh",
            align_items="flex-start",
        ),
        width="100%",
        align_items="flex-start",
    )
