import reflex as rx

def sidebar() -> rx.Component:
    return rx.vstack(
        rx.heading("App Logo", size="4", padding_bottom="1em"),
        rx.link(
            rx.hstack(
                rx.icon("layout-dashboard"),
                rx.text("Dashboard"),
            ),
            href="/",
        ),
        rx.link(
            rx.hstack(
                rx.icon("settings"),
                rx.text("Settings"),
            ),
            href="/settings",
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
            ),
            margin_left="250px",
            width="100%",
            min_height="100vh",
            align_items="flex-start",
        ),
        width="100%",
        align_items="flex-start",
    )
