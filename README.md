# Ramdev Travels

A full-stack travel booking MVP for buses, flights and cinema tickets.

## Stack

- Backend: FastAPI, SQLAlchemy async, PostgreSQL, JWT
- Payments: Razorpay integration with signature verification and webhook endpoint
- Frontend: React, Vite, Redux Toolkit, Tailwind CSS
- Free deployment: Render static site + Render free web service + Supabase PostgreSQL
- Tests: Pytest

## Free deployment architecture

The production configuration does **not** require an always-on Redis/Celery worker. Booking holds live in PostgreSQL for 15 minutes and expired holds are released transactionally when booking/search traffic reaches the API. This keeps the booking inventory correct without a paid background worker.

See [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) and [`render.yaml`](render.yaml).

## Local development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
AUTO_CREATE_TABLES=true python seed.py
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open http://localhost:5173.

### Docker

Create `backend/.env`, then:

```bash
docker compose up --build
```

## Razorpay

Set these in `backend/.env`:

- `RAZORPAY_KEY_ID`
- `RAZORPAY_KEY_SECRET`
- `RAZORPAY_WEBHOOK_SECRET`

Never expose the secret key in the frontend. The frontend receives only the public key ID from the backend.

## Database

For local development you may use `AUTO_CREATE_TABLES=true`. Production deployments use Alembic migrations automatically.

## Production readiness gate

Do not accept real bookings until PostgreSQL migrations have been applied, strong secrets are configured, Razorpay production keys/webhook are configured, HTTPS is enabled, and concurrency/payment webhook tests have passed in staging.
