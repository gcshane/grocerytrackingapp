# 🛒 Grocery Tracker (API)

A RESTful API for tracking groceries, managing shopping lists, and monitoring item expiry dates — built with **FastAPI** and **PostgreSQL**.

## ✨ Features

- **User Authentication** — Secure login with OAuth2 password flow, JWT access tokens, and Argon2 password hashing
- **Shopping Lists** — Create and manage personalised grocery lists
- **Item Tracking** — Track items with quantities and configurable stock alerts
- **Expiry Monitoring** — Log item batches with expiry dates and set alert thresholds to reduce food waste

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) |
| **ORM** | [SQLModel](https://sqlmodel.tiangolo.com/) |
| **Database** | PostgreSQL (via [Supabase](https://supabase.com/)) |
| **Auth** | [PyJWT](https://pyjwt.readthedocs.io/) + [pwdlib](https://github.com/frankie567/pwdlib) (Argon2) |
| **Deployment** | [Railway](https://railway.com/) |

## 📁 Project Structure

```
grocerytrackingapp/
├── app/
│   ├── api/v1/          # Route handlers
│   │   ├── auth.py      # Authentication endpoints
│   │   └── lists.py     # List endpoints
│   ├── core/
│   │   └── config.py    # Environment configuration
│   ├── db/
│   │   ├── database.py  # Engine & session management
│   │   └── schema.py    # SQLModel table definitions
│   ├── models/          # Pydantic request/response models
│   ├── services/        # Business logic layer
│   │   ├── auth_services.py
│   │   └── user_services.py
│   ├── dependencies.py  # FastAPI dependency injection
│   └── main.py          # App entrypoint
├── design/              # Database design diagrams
├── tests/               # Unit tests
├── pyproject.toml       # uv dependency management
└── railway.json         # Legacy Railway deployment config
```

## 📊 Database Schema

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│    User      │       │    List      │       │    Item      │       │  ItemBatch   │
├──────────────┤       ├──────────────┤       ├──────────────┤       ├──────────────┤
│ user_id (PK) │──┐    │ list_id (PK) │──┐    │ item_id (PK) │──┐    │ expiry_date  │
│ name         │  └───>│ list_name    │  └───>│ item_name    │  └───>│   (PK)       │
│ username     │       │ user_id (FK) │       │ list_id (FK) │       │ item_id      │
│ email        │       └──────────────┘       │ total_qty    │       │   (PK, FK)   │
│ password     │                              │ qty_limit    │       │ quantity     │
│ alert        │                              │ alert_days   │       └──────────────┘
└──────────────┘                              └──────────────┘
```

## 🚀 Getting Started

### Prerequisites

- Python 3.13.3+
- [uv](https://docs.astral.sh/uv/) package manager
- PostgreSQL database (or a [Supabase](https://supabase.com/) project)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/gcshane/grocerytrackingapp.git
   cd grocerytrackingapp
   ```

2. **Install dependencies**

   This automatically creates a virtual environment and installs everything:

   ```bash
   uv sync
   ```

4. **Configure environment variables**

   Create a `.env` file in the project directory:

   ```env
   DATABASE_URL=postgresql://user:password@host:port/dbname
   JWT_SECRET_KEY=your-secret-key
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Run the development server**

   ```bash
   uv run uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`.

### Development & Testing

- **Run unit tests**: `uv run pytest`
- **Lint the code**: `uvx ruff check .`

### API Documentation

FastAPI auto-generates interactive docs:

- **Swagger UI** — [http://localhost:8000/docs](http://localhost:8000/docs)

## 🔑 API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/` | Health check | ✗ |
| `POST` | `/auth/login` | Login & receive JWT | ✗ |
| `GET` | `/lists` | Get user's lists | ✓ |

> **Authentication:** Include the JWT in the `Authorization` header:
> ```
> Authorization: Bearer <access_token>
> ```

## 🌐 Deployment

The API is configured for seamless continuous deployment to **FastAPI Cloud** via GitHub Actions.

When code is pushed to the `main` branch, the `.github/workflows/deploy.yaml` pipeline automatically provisions the `uv` environment and ships the latest code using `uv run fastapi deploy`.

*(Note: There is also legacy support for Railway deployment via `railway.json`)*

## 📄 License

This project is for personal use.