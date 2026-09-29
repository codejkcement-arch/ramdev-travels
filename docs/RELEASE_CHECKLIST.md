# Release checklist

- [ ] Create production PostgreSQL database and Redis.
- [ ] Set a long random SECRET_KEY.
- [ ] Set production CORS_ORIGINS to the public web origin.
- [ ] Set Razorpay production keys and webhook secret.
- [ ] Apply `alembic upgrade head`.
- [ ] Create a non-default admin account and remove demo credentials.
- [ ] Confirm `/health` and `/docs` from the API network.
- [ ] Test registration/login.
- [ ] Test search → seat selection → booking → Razorpay test payment.
- [ ] Test duplicate payment verification and duplicate webhook delivery.
- [ ] Test concurrent booking attempts for the same seat.
- [ ] Test cancellation/refund rules against the actual provider.
- [ ] Enable HTTPS and secure cookies/headers at the edge.
- [ ] Configure backups, monitoring and error alerts.
- [ ] Review logs for secrets and personal/payment data.
- [ ] Build the frontend and verify `/api/*` is proxied by Nginx.
