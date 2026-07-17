# TaskFlow API

TaskFlow API is a backend service for task and organization management built with FastAPI, SQLAlchemy 2.0, PostgreSQL, and Alembic.

> Status: In Development 🚧

## Goals

- Learn FastAPI professionally.
- Master SQLAlchemy 2.0.
- Build a production-ready backend.
- Apply Clean Architecture and best practices.

---

## Tech Stack

- Python 3.14
- FastAPI
- SQLAlchemy 2.0
- PostgreSQL
- Alembic
- Pydantic v2
- Docker (planned)
- Redis (planned)
- Pytest (planned)

---

## Current Features

- Project configuration with Pydantic Settings
- SQLAlchemy Engine
- Session Factory
- Declarative Base
- BaseModel
- User model
- Alembic integration
- Database migrations

---

## Project Structure

```text
app/
├── alembic/
├── api/
├── core/
├── db/
├── dependencies/
├── middleware/
├── models/
├── permissions/
├── repositories/
├── schemas/
├── services/
└── tests/
```

---

## Database

Current tables:

- users

---

## Getting Started

### Clone repository

```bash
git clone <repository_url>
cd TaskFlow-API
```

### Create virtual environment

```bash
python -m venv venv
```

### Activate

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment

Create a `.env` file.

```env
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql+psycopg://user:password@localhost/taskflow
DEBUG=True
```

### Run migrations

```bash
alembic upgrade head
```

### Start server

```bash
uvicorn main:app --reload
```

---

## Roadmap

- [x] Project Configuration
- [x] SQLAlchemy Engine
- [x] Session
- [x] Declarative Base
- [x] User Model
- [x] Alembic Integration
- [ ] Authentication
- [ ] Organizations
- [ ] RBAC
- [ ] Tasks
- [ ] Comments
- [ ] Notifications
- [ ] Docker
- [ ] Testing
- [ ] CI/CD

---

## License

MIT License