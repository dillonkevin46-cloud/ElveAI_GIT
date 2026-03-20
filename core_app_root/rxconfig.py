import reflex as rx
import os
from dotenv import load_dotenv

# Load environment variables from the .env file securely
load_dotenv()

# Fetch the database URL; fail safely to a default if missing during initial setup
DB_URL = os.getenv("DATABASE_URL", "sqlite:///reflex.db")

config = rx.Config(
    app_name="core_app",
    db_url=DB_URL,
    env=rx.Env.DEV,
    # We strictly define the telemetry as false for privacy
    telemetry_enabled=False, 
)