import reflex as rx
from core_app.state.auth_state import AuthState

@rx.page(route="/login", title="Login - ElveAI")
def login() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("ElveAI", size="8", margin_bottom="1em"),
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger("Login", value="login"),
                    rx.tabs.trigger("Register", value="register"),
                    width="100%",
                ),
                rx.tabs.content(
                    rx.form(
                        rx.vstack(
                            rx.input(name="username", placeholder="Username", required=True),
                            rx.input(name="password", type="password", placeholder="Password", required=True),
                            rx.button("Login", type="submit", width="100%"),
                        ),
                        on_submit=AuthState.login,
                    ),
                    value="login",
                ),
                rx.tabs.content(
                    rx.form(
                        rx.vstack(
                            rx.input(name="username", placeholder="Username", required=True),
                            rx.input(name="email", placeholder="Email", required=True),
                            rx.input(name="password", type="password", placeholder="Password", required=True),
                            rx.button("Register", type="submit", width="100%"),
                        ),
                        on_submit=AuthState.register,
                    ),
                    value="register",
                ),
                default_value="login",
                width="400px",
            ),
            rx.cond(
                AuthState.auth_error != "",
                rx.text(AuthState.auth_error, color="red.500", margin_top="1em"),
            ),
            align_items="center",
            justify_content="center",
            min_height="100vh",
        ),
        center_content=True,
    )
