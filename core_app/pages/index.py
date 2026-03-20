import reflex as rx
from core_app.components.layout import base_layout

@rx.page(route="/", title="Dashboard")
def index() -> rx.Component:
    return base_layout(
        rx.heading("Dashboard Overview"),
        rx.text("Welcome to the new system architecture."),
    )
