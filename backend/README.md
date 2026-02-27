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

## Create first center (required before users)
```bash
docker exec -it backend-db-1 psql -U postgres -d coins -c "INSERT INTO centers (name, timezone) VALUES ('Main Center','UTC');"
```

## Create super admin user
```bash
cd backend
python scripts/create_admin.py --email admin@example.com --password 'StrongPass123!' --full-name 'Main Admin' --center-id 1
```

## Register student
```bash
curl -X POST http://localhost:8000/api/v1/auth/register-student \
  -H 'Content-Type: application/json' \
  -d '{"email":"s@test.com","password":"12345678","full_name":"Stu","center_id":1}'
```

## Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"s@test.com","password":"12345678"}'
```

## Healthcheck
```bash
curl http://localhost:8000/health
```

## Run app locally
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Tests
```bash
cd backend
pytest -q
```

## Assumptions
- Leaderboard timezone defaults to UTC in routes.
- Idempotency key is required for awards, enroll, and create order.
