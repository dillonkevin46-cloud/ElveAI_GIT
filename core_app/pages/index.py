import reflex as rx
from core_app.components.layout import base_layout
from core_app.state.main_state import MainState

@rx.page(route="/", title="Dashboard", on_load=MainState.load_sessions)
def index():
    return base_layout(
        rx.cond(
            MainState.active_session_id == -1,
            # -----------------------------------------
            # DASHBOARD VIEW
            # -----------------------------------------
            rx.vstack(
                rx.heading("Dashboard Overview"),
                rx.text("Welcome to ElveAI. Select or create a chat in the sidebar to begin.", margin_bottom="2em"),
                rx.card(
                    rx.vstack(
                        rx.text("Total Sessions", size="2", color="gray.500"),
                        rx.heading(MainState.user_sessions.length(), size="6")
                    ),
                    width="250px"
                )
            ),
            # -----------------------------------------
            # ACTIVE CHAT VIEW
            # -----------------------------------------
            rx.vstack(
                # Chat Messages Area
                rx.scroll_area(
                    rx.foreach(
                        MainState.current_messages,
                        lambda message: rx.box(
                            rx.markdown(
                                message.content,
                                component_map={
                                    "code": lambda text: rx.code_block(text, wrap_long_lines=True, margin_y="1em"),
                                }
                            ),
                            background_color=rx.cond(message.role == "user", "blue.100", "gray.100"),
                            color="black",
                            padding="1em",
                            border_radius="15px",
                            margin_y="0.5em",
                            align_self=rx.cond(message.role == "user", "flex-end", "flex-start"),
                            max_width="85%"
                        )
                    ),
                    height="70vh",
                    width="100%",
                    padding_right="1em",
                ),
                
                # RAG Document Upload Zone
                rx.vstack(
                    rx.hstack(
                        rx.upload(
                            rx.button("Select Document (PDF/TXT)", variant="soft", size="1"), 
                            id="doc_upload", 
                            accept={
                                "application/pdf": [".pdf"], 
                                "text/plain": [".txt"]
                            }
                        ),
                        rx.button(
                            "Upload to Context", 
                            on_click=MainState.handle_upload(rx.upload_files(upload_id="doc_upload")), 
                            size="1"
                        ),
                        align_items="center"
                    ),
                    # Dynamic Visual Feedback for Selected Files
                    rx.cond(
                        rx.selected_files("doc_upload"),
                        rx.text(
                            "Pending Upload: ", 
                            rx.foreach(rx.selected_files("doc_upload"), lambda f: rx.text(f, as_="span", weight="bold")), 
                            size="2", 
                            color="blue.600"
                        ),
                        rx.text("No file selected.", size="2", color="gray.400")
                    ),
                    width="100%",
                    padding_y="0.5em",
                    align_items="flex-start"
                ),

                # Chat Input Form
                rx.form(
                    rx.hstack(
                        rx.input(name="chat_input", placeholder="Message ElveAI...", width="100%"),
                        rx.button("Send", type="submit")
                    ),
                    on_submit=MainState.handle_submit,
                    reset_on_submit=True,
                    width="100%"
                ),
                width="100%",
                height="100%",
                justify_content="space-between"
            )
        )
    )