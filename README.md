# Money Monorepo

## Backend
- Location: `backend/`
- FastAPI + PostgreSQL + Alembic

## Frontend (React)
- Location: `frontend/`
- Vite + React + TypeScript

### Run frontend
```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

By default frontend expects backend API at `http://localhost:8000/api/v1`.
