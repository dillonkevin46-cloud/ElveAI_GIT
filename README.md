Markdown

# ElveAI

> **An Open-Source, Locally Hosted, Sovereign AI Chat Application.**

ElveAI is a full-stack, real-time AI chat interface built on a strict, domain-driven architecture. It leverages 100% free and open-source technologies, ensuring complete data privacy and zero API costs by running the Large Language Model (LLM) entirely on your local hardware.

## 🚀 Key Features

* **Sovereign AI Engine:** Powered by [Ollama](https://ollama.com/) running the `llama3.2` model locally. No data leaves your machine.
* **Real-Time Streaming:** LLM tokens are streamed asynchronously to the UI, providing a fast, non-blocking user experience.
* **Stateless Authentication:** Secure, cookie-based session management using modern `bcrypt` password hashing.
* **Modern Reactive UI:** Built strictly with [Reflex](https://reflex.dev/) and Radix UI primitives. No HTML/CSS or Javascript was written; the entire stack is pure Python.
* **Relational Persistence:** Chat sessions, messages, and user identities are stored securely in a local PostgreSQL database using SQLModel and Alembic migrations.
* **Code Native:** Features full Markdown rendering with dedicated syntax highlighting for generated code blocks.

---

## 🛠️ Technology Stack

* **Frontend & Backend Framework:** Python 3.x / Reflex (v0.8+)
* **Database:** PostgreSQL
* **ORM & Migrations:** SQLModel / Alembic
* **Authentication:** `bcrypt`
* **Local LLM Runner:** Ollama

---

## 📂 Architecture Blueprint

The application enforces a strictly modular, domain-driven package structure:

```text
ElveAI/
├── .env                     # Local credentials & DB connection string
├── rxconfig.py              # Core Reflex & DB Configuration
├── requirements.txt         # Project Dependencies
├── alembic/                 # Auto-generated database migration scripts
└── core_app/                # Main application package
    ├── __init__.py
    ├── core_app.py          # App entry point & page routing registration
    ├── models/              # Relational Database Schemas (User, ChatSession, ChatMessage)
    ├── state/               # Async State Management (Auth, LLM Streaming, DB queries)
    ├── components/          # Reusable UI elements (Sidebar, Layout wrapper)
    └── pages/               # Individual View Definitions (Dashboard, Chat, Login)
⚙️ Local Environment Setup
Prerequisites
Python 3.10+ installed on your machine.

PostgreSQL installed and running locally.

Ollama installed (Download Here).

1. Initialize the LLM
Before starting the application, you must pull the Llama model to your local machine. Open a terminal and run:

Bash

ollama run llama3.2
(Once it finishes downloading and starts a prompt, you can type /bye to exit. The model is now cached).

2. Database Configuration
Create a PostgreSQL database named core_app_db.
Then, create a .env file in the root of this project and add your connection string. Note: URL-encode special characters in your password (e.g., @ becomes %40).

Code snippet

DATABASE_URL=postgresql://postgres:YOUR_PASSWORD_HERE@localhost:5432/core_app_db
3. Install Dependencies
Open your terminal at the project root and set up your Python virtual environment:

Windows (PowerShell):

PowerShell

python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Linux/macOS:

Bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
(If you do not have a requirements.txt, manually install: pip install reflex psycopg2-binary python-dotenv sqlmodel bcrypt ollama)

4. Run Database Migrations
Initialize the tables in your PostgreSQL database based on the Python models:

Bash

reflex db migrate
🏃‍♂️ Running the Application
With Ollama running in the background and your virtual environment activated, boot the Reflex server:

Bash

reflex run
Frontend UI: http://localhost:3000

Backend API: http://0.0.0.0:8000

Upon first visit, you will be securely redirected to /login to register your local account.

🔒 Security Notes
This application is designed for local, sovereign deployment. The .env file containing your database credentials is intentionally included in the .gitignore to prevent accidental credential leakage. Never commit your .env file to version control.


***

As your Architect, I consider this deployment officially documented and complete. The r