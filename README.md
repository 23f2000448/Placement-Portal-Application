# Placement Portal Application

A web application for managing campus recruitment — connecting institutes, companies, and students through a role-based placement management system.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Flask (Python) |
| Frontend | Vue.js (Vite + CLI) |
| Database | SQLite (via SQLAlchemy) |
| Auth | JWT (Flask-JWT-Extended) |
| Caching | Redis |
| Background Jobs | Celery + Redis |
| Styling | Bootstrap 5 |

## Roles

- **Admin** — pre-seeded superuser; approves companies and drives, manages the platform
- **Company** — registers, creates placement drives after approval, manages applications
- **Student** — registers, applies to drives, tracks application status

## Project Structure

```
placement-portal-application/
├── backend/        # Flask API
└── frontend/       # Vue.js SPA
```

## Setup

> Detailed setup instructions will be added as the project progresses.

**Prerequisites:** Python 3.10+, Node.js, Redis

```bash
# Backend
cd backend
pip install -r requirements.txt
python run.py

# Frontend
cd frontend
npm install
npm run dev

# Celery worker
celery -A celery_worker.celery worker --loglevel=info
```

## Author

Tanuj Nain