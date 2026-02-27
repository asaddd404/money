# Money Frontend (React + Vite + TypeScript)

Полноценный mobile-first фронтенд для FastAPI backend (`/api/v1`) с ролевым UX:
- `student`
- `teacher`
- `manager`
- `admin`

## Stack
- React 18 + Vite + TypeScript (strict)
- React Router v6
- TailwindCSS + Radix UI + shadcn-style components
- TanStack Query
- Zustand (in-memory auth/session)
- react-hook-form + Zod
- Framer Motion
- recharts
- sonner toast
- ESLint + Prettier
- Vitest + RTL

## ENV
Скопируйте `.env.example` в `.env`:

```bash
cp .env.example .env
```

Поля:
- `VITE_API_URL` — базовый URL backend (например `http://localhost:8000`)
- `VITE_ENABLE_REFRESH_SESSION_STORAGE` — `true|false`, хранить ли refresh token в `sessionStorage`.

### Почему refresh в sessionStorage опционален
По умолчанию refresh token хранится только в памяти (без `localStorage`), это безопаснее при XSS.
Опциональный `sessionStorage` добавлен для UX после reload, но это менее безопасно, поэтому выключен по умолчанию.

## Пошаговый запуск: БД → backend → создание admin → регистрация

### 1) Поднять Postgres и API
```bash
cd backend
docker compose up --build -d
```

### 2) Применить миграции
```bash
cd backend
alembic upgrade head
```

### 3) Создать `center` (если в БД еще пусто)
```bash
docker exec -it backend-db-1 psql -U postgres -d coins -c "INSERT INTO centers (name, timezone) VALUES ('Main Center','UTC');"
```

### 4) Создать главного admin в БД
```bash
cd backend
python scripts/create_admin.py --email admin@example.com --password 'StrongPass123!' --full-name 'Main Admin' --center-id 1
```

### 5) Запустить frontend
```bash
npm install
npm run dev
```

### 6) Как зайти
- Откройте `http://localhost:5173/auth/login`.
- Для главного пользователя введите admin email/password из шага 4.
- После логина произойдет редирект в `/app/admin/home`.

### 7) Как проходит регистрация
- Откройте `http://localhost:5173/auth/register`.
- Заполните `full_name`, `email`, `password`, `center_id`.
- Форма отправляет `POST /api/v1/auth/register-student`.
- После успешной регистрации фронт возвращает на `/auth/login`.
- Вход выполняется через `POST /api/v1/auth/login`.

## Проверки
```bash
npm run lint
npm run test
npm run build
```

## Auth flow
1. `POST /api/v1/auth/login`
2. `GET /api/v1/users/me`
3. Role redirect:
   - student -> `/app/student/home`
   - teacher -> `/app/teacher/home`
   - manager -> `/app/manager/home`
   - admin -> `/app/admin/home`
4. При `401` клиент делает **один** `refresh` (`POST /api/v1/auth/refresh`) и ретрай запроса.
5. Если refresh неуспешен -> logout + redirect `/auth/login`.

## Idempotency-Key
Для:
- `POST /api/v1/awards`
- `POST /api/v1/orders`
- `POST /api/v1/groups/{group_id}/enroll`

клиент отправляет `Idempotency-Key: <uuid-v4>` + кнопки блокируются в pending.

## Demo users
Заполните соответствующими аккаунтами backend:
- `student@example.com`
- `teacher@example.com`
- `manager@example.com`
- `admin@example.com`

## Примечание по интеграции
UI ожидает backend contract из задания: единый формат ошибок
```json
{
  "error": {
    "code": "SOME_CODE",
    "message": "Human readable",
    "details": {}
  }
}
```
`message` показывается в toast/inline, `code` логируется в dev-консоль, `details` выводятся в expandable блоке.
