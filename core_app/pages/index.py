import reflex as rx
from core_app.components.layout import base_layout
from core_app.state.main_state import MainState

def dashboard_view() -> rx.Component:
    return rx.vstack(
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

def chat_view() -> rx.Component:
    return rx.vstack(
        rx.scroll_area(
            rx.vstack(
                rx.foreach(
                    MainState.current_messages,
                    lambda message: rx.box(
                        rx.markdown(
                            message.content,
                            component_map={
                                "code": lambda text: rx.code_block(text, wrap_long_lines=True, margin_y="1em"),
                            },
                            margin="0"
                        ),
                        bg=rx.cond(message.role == "user", "blue.100", "gray.100"),
                        align_self=rx.cond(message.role == "user", "flex-end", "flex-start"),
                        padding="1em",
                        border_radius="15px",
                        margin_bottom="1em",
                        max_width="80%",
                    )
                ),
                width="100%",
                padding_bottom="2em",
            ),
            flex="1",
            width="100%",
            padding_right="1em",
        ),
        rx.hstack(
            rx.upload(
                rx.button("Attach Document (PDF/TXT)", variant="soft", size="1"),
                id="doc_upload",
                accept={
                    ".pdf": ["application/pdf"],
                    ".txt": ["text/plain"]
                }
            ),
            rx.button(
                "Upload",
                on_click=MainState.handle_upload(rx.upload_files(upload_id="doc_upload")),
                size="1"
            ),
            width="100%",
            padding_y="0.5em"
        ),
        rx.form(
            rx.hstack(
                rx.input(name="chat_input", placeholder="Message ElveAI...", flex="1"),
                rx.button("Send", type="submit"),
                width="100%",
            ),
            on_submit=MainState.handle_submit,
            reset_on_submit=True,
            width="100%",
        ),
        width="100%",
        height="100%",
        justify_content="space-between",
    )

@rx.page(route="/", title="Dashboard", on_load=MainState.load_sessions)
def index() -> rx.Component:
    return base_layout(
        rx.cond(
            MainState.active_session_id == -1,
            dashboard_view(),
            chat_view(),
        )
    )
