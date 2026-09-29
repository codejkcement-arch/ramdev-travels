# Database schema

users: users and admin roles
buses: bus inventory
bus_seats: individual bus seats
flights: flight inventory
cinemas: cinema venues
cinema_shows: movie showtimes
cinema_seats: show inventory
bookings: booking and payment state
payments: Razorpay references
refunds: refund records

Production should add indexes based on actual query traffic and enforce additional uniqueness constraints for provider references.
