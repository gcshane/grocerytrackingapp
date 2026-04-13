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
| **Deployment** | [FastAPI Cloud](https://fastapi.tiangolo.com/deployment/) |

## 📁 Project Structure

```
grocerytracker-api/
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
   git clone https://github.com/gcshane/grocerytracker-api.git
   cd grocerytracker-api
   ```

2. **Install dependencies**

   This automatically creates a virtual environment and installs everything:

   ```bash
   uv sync
   ```

3. **Configure environment variables**

   Create a `.env` file in the project directory:

   ```env
   # Database
   DATABASE_URL=postgresql://user:password@host:port/dbname
   # Or use SQLite for local development:
   # DATABASE_URL=sqlite:///grocery.db
   
   # JWT Authentication
   JWT_SECRET_KEY=your-secret-key-here-min-32-chars
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

   > **⚠️ Security Warning**: Use a strong secret key (32+ characters) in production. Never commit this file to version control.

4. **Run the development server**

   ```bash
   uv run uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`.

### Development & Testing

- **Run all tests**: `uv run pytest -v`
- **Lint the code**: `uvx ruff check .`

### API Documentation

FastAPI auto-generates interactive docs:

- **Swagger UI** — [http://localhost:8000/docs](http://localhost:8000/docs)

## 🔑 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth | Request Body |
|--------|----------|-------------|------|--------------|
| `POST` | `/auth/signup` | Create a new account | ✗ | `{"username": "...", "password": "...", "email": "...", "name": "...", "alert": true}` |
| `POST` | `/auth/login` | Login & receive JWT | ✗ | Form data: `username`, `password` |

### Lists & Items

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/lists` | Get user's shopping lists | ✓ |
| `POST` | `/lists` | Create a new shopping list | ✓ |

### Health Check

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/` | API health check | ✗ |

> **Authentication:** Include the JWT in the `Authorization` header:
> ```
> Authorization: Bearer <access_token>
> ```

### Example: Login Flow

1. **Sign up** with credentials:
   ```bash
   curl -X POST http://localhost:8000/auth/signup \
     -H "Content-Type: application/json" \
     -d '{
       "username": "john_doe",
       "password": "secret123",
       "email": "john@example.com",
       "name": "John Doe",
       "alert": true
     }'
   ```

2. **Login** to get access token:
   ```bash
   curl -X POST http://localhost:8000/auth/login \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=john_doe&password=secret123"
   ```
   
   Response:
   ```json
   {
     "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
     "token_type": "bearer"
   }
   ```

3. **Access protected endpoints** with the token:
   ```bash
   curl -X GET http://localhost:8000/lists \
     -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
   ```

## 🌐 Deployment

The API is deployed on **FastAPI Cloud**, with automatic continuous deployment via GitHub Actions.

When code is pushed to the `main` branch, the `.github/workflows/deploy.yaml` pipeline automatically builds and deploys the application to FastAPI Cloud, ensuring the latest changes are live within minutes.

*(Note: There is also legacy support for [Railway](https://railway.com/) deployment via `railway.json`)*

## 🏛️ Architecture

This API follows a **layered architecture** pattern:

```
┌─────────────────────────────────────┐
│        API Routes (FastAPI)         │ ← HTTP endpoints, request validation
├─────────────────────────────────────┤
│     Service Layer (Business Logic)  │ ← Auth flows, user management
├─────────────────────────────────────┤
│  Data Access Layer (SQLModel/ORM)   │ ← Database queries
├─────────────────────────────────────┤
│        Database (PostgreSQL)        │ ← Persistent storage
└─────────────────────────────────────┘
```

**Benefits:**
- ✅ Business logic is testable independently of HTTP layer
- ✅ Easy to add new routes without duplicating logic
- ✅ Database queries are centralized and reusable
- ✅ 100% test coverage on service layer

## 📄 License

This project is for personal use.