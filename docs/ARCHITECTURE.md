# Architecture

Browser/Android WebView → Nginx → React/Vite frontend and FastAPI API.

FastAPI owns authentication, inventory, booking state, payments and admin APIs.
PostgreSQL is the source of truth. Redis handles short-lived seat holds and Celery broker/backend.
Razorpay is the external payment provider.

Booking lifecycle:
PENDING → payment order → PAID/CONFIRMED
or PENDING → cancellation/expiry
PAID → REFUNDED
