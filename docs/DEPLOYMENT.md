# Free deployment (Render + Supabase)

Ramdev Travels can run without an always-on Redis/Celery service. Booking holds are stored in PostgreSQL and expired holds are released transactionally when API traffic reaches the booking/search endpoints. This keeps the core booking flow compatible with a free web-service deployment.

## 1. Supabase PostgreSQL

Create a Supabase project and copy the PostgreSQL connection string from **Connect**. For a hosted API, the shared pooler is suitable; use the exact host/user/password shown by Supabase. Set it as `DATABASE_URL` in Render.

The application uses SQLAlchemy's `NullPool` and disables asyncpg statement caching, which is compatible with Supabase transaction-pooler connections.

## 2. Render

The repository includes `render.yaml` with two services:

- `ramdev-travels-api`: FastAPI/Gunicorn web service on the free plan.
- `ramdev-travels-web`: React/Vite static site.

The API runs `alembic upgrade head` before deployment. The static site has a React Router rewrite to `/index.html`.

After creating the Blueprint, verify the generated `onrender.com` URLs. If Render assigns a suffix because the names already exist, update `VITE_API_URL` on the frontend service to the actual API URL and redeploy the frontend.

## 3. Required API secrets

Set these in the Render dashboard; never commit them:

- `DATABASE_URL`
- `RAZORPAY_KEY_ID`
- `RAZORPAY_KEY_SECRET`
- `RAZORPAY_WEBHOOK_SECRET`
- `ADMIN_EMAIL`
- `ADMIN_PASSWORD`
- SMTP variables if email delivery is enabled

Render generates `SECRET_KEY` automatically from the Blueprint.

## 4. Razorpay

Configure the production webhook URL as:

`https://<actual-api-host>/api/webhooks/razorpay`

Do not enable real-money bookings until the Razorpay account is verified, HTTPS is active, and payment/webhook tests have passed.

## 5. Local Docker

Docker Compose now runs only PostgreSQL, FastAPI and the frontend; Redis/Celery are no longer required for the booking-hold mechanism.
