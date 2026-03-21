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
                width="100%",
                padding_bottom="2em",
            ),
            flex="1",
            width="100%",
            padding_right="1em",
        ),
        rx.box(
            rx.vstack(
                rx.text("Attached Context", weight="bold", size="2", color="gray.600"),
                rx.cond(
                    MainState.active_documents,
                    rx.hstack(
                        rx.foreach(
                            MainState.active_documents,
                            lambda doc: rx.badge(
                                rx.icon("file-text", size=14),
                                doc.filename,
                                color_scheme="green",
                                radius="full",
                                padding="0.5em"
                            )
                        ),
                        wrap="wrap",
                        spacing="2"
                    ),
                    rx.text("No documents attached.", size="1", color="gray.500")
                ),
                rx.hstack(
                    rx.upload(
                        rx.button("Attach Document (PDF/TXT)", variant="soft", size="1"),
                        id="doc_upload",
                        accept={
                            "application/pdf": [".pdf"],
                            "text/plain": [".txt"]
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
                rx.cond(
                    rx.selected_files("doc_upload"),
                    rx.text(
                        rx.selected_files("doc_upload").to_string(),
                        size="1",
                        color="orange.600"
                    )
                ),
                width="100%",
                align_items="flex-start"
            ),
            border="1px solid",
            border_color="gray.200",
            border_radius="8px",
            padding="1em",
            width="100%",
            margin_bottom="1em"
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