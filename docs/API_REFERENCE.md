# API Reference

Interactive OpenAPI docs are available at `/docs`.

Auth:
- POST /api/auth/register
- POST /api/auth/login
- GET /api/auth/me

Buses:
- GET /api/buses/search?source=...&destination=...
- GET /api/buses/{bus_id}/seats

Cinema:
- GET /api/cinema/search?city=...&movie=...
- GET /api/cinema/{show_id}/seats

Flights:
- GET /api/flights/search?source=...&destination=...

Bookings:
- POST /api/bookings
- GET /api/bookings
- GET /api/bookings/{booking_id}

Payments:
- POST /api/payments/create-order
- POST /api/payments/verify

Admin:
- GET /api/admin/stats
- GET /api/admin/bookings
- POST /api/admin/refund/{booking_id}

Webhooks:
- POST /api/webhooks/razorpay
