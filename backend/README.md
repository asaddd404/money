# Coins + Groups + Leaderboards + Shop + Orders

## Run Postgres + API
```bash
cd backend
docker compose up --build -d
```

## Migrations
```bash
cd backend
alembic upgrade head
```

## Run app locally
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## cURL examples
```bash
curl -X POST http://localhost:8000/api/v1/auth/register-student -H 'Content-Type: application/json' -d '{"email":"s@test.com","password":"12345678","full_name":"Stu","center_id":1}'
curl -X POST http://localhost:8000/api/v1/auth/login -H 'Content-Type: application/json' -d '{"email":"s@test.com","password":"12345678"}'
curl http://localhost:8000/health
```

## Tests
```bash
cd backend
pytest -q
```

## Assumptions
- Leaderboard timezone defaults to UTC in routes.
- Idempotency key is required for awards, enroll, and create order.
