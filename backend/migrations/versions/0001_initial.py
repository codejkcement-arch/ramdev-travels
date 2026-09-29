"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-09-27
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("users",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(120), nullable=False),
        sa.Column("email", sa.String(255), nullable=False), sa.Column("phone", sa.String(20)),
        sa.Column("password_hash", sa.String(255), nullable=False), sa.Column("is_admin", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table("buses",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("operator", sa.String(120), nullable=False),
        sa.Column("bus_number", sa.String(50), nullable=False), sa.Column("source", sa.String(100), nullable=False),
        sa.Column("destination", sa.String(100), nullable=False), sa.Column("departure_time", sa.String(10), nullable=False),
        sa.Column("arrival_time", sa.String(10), nullable=False), sa.Column("fare", sa.Float(), nullable=False),
        sa.Column("total_seats", sa.Integer(), nullable=False, server_default="40"))
    op.create_index("ix_buses_bus_number", "buses", ["bus_number"], unique=True)
    op.create_index("ix_buses_source", "buses", ["source"])
    op.create_index("ix_buses_destination", "buses", ["destination"])

    op.create_table("bus_seats", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("bus_id", sa.Integer(), sa.ForeignKey("buses.id", ondelete="CASCADE"), nullable=False), sa.Column("seat_number", sa.String(10), nullable=False), sa.Column("is_booked", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.create_index("ix_bus_seats_bus_seat", "bus_seats", ["bus_id", "seat_number"], unique=True)

    op.create_table("flights", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("airline", sa.String(120), nullable=False), sa.Column("flight_number", sa.String(30), nullable=False), sa.Column("source", sa.String(100), nullable=False), sa.Column("destination", sa.String(100), nullable=False), sa.Column("departure_time", sa.DateTime(), nullable=False), sa.Column("arrival_time", sa.DateTime(), nullable=False), sa.Column("fare", sa.Float(), nullable=False), sa.Column("available_seats", sa.Integer(), nullable=False, server_default="180"))
    op.create_index("ix_flights_flight_number", "flights", ["flight_number"], unique=True)
    op.create_index("ix_flights_source", "flights", ["source"])
    op.create_index("ix_flights_destination", "flights", ["destination"])

    op.create_table("cinemas", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(150), nullable=False), sa.Column("city", sa.String(100), nullable=False), sa.Column("address", sa.String(255), nullable=False))
    op.create_index("ix_cinemas_city", "cinemas", ["city"])
    op.create_table("cinema_shows", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("cinema_id", sa.Integer(), sa.ForeignKey("cinemas.id"), nullable=False), sa.Column("movie_name", sa.String(150), nullable=False), sa.Column("show_time", sa.DateTime(), nullable=False), sa.Column("price", sa.Float(), nullable=False), sa.Column("total_seats", sa.Integer(), nullable=False, server_default="100"))
    op.create_table("cinema_seats", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("show_id", sa.Integer(), sa.ForeignKey("cinema_shows.id", ondelete="CASCADE"), nullable=False), sa.Column("seat_number", sa.String(10), nullable=False), sa.Column("is_booked", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.create_index("ix_cinema_seats_show_seat", "cinema_seats", ["show_id", "seat_number"], unique=True)

    op.create_table("bookings", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("pnr", sa.String(20), nullable=False), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False), sa.Column("booking_type", sa.String(20), nullable=False), sa.Column("item_id", sa.Integer(), nullable=False), sa.Column("seats", sa.Text(), nullable=False), sa.Column("amount", sa.Float(), nullable=False), sa.Column("status", sa.String(30), nullable=False, server_default="PENDING"), sa.Column("payment_status", sa.String(30), nullable=False, server_default="PENDING"), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_bookings_pnr", "bookings", ["pnr"], unique=True)

    op.create_table("payments", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("booking_id", sa.Integer(), sa.ForeignKey("bookings.id"), nullable=False), sa.Column("provider", sa.String(30), nullable=False, server_default="razorpay"), sa.Column("order_id", sa.String(100), unique=True), sa.Column("payment_id", sa.String(100)), sa.Column("signature", sa.String(255)), sa.Column("amount", sa.Float(), nullable=False), sa.Column("currency", sa.String(5), nullable=False, server_default="INR"), sa.Column("status", sa.String(30), nullable=False, server_default="CREATED"), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_table("refunds", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("booking_id", sa.Integer(), sa.ForeignKey("bookings.id"), nullable=False), sa.Column("amount", sa.Float(), nullable=False), sa.Column("reason", sa.String(255), nullable=False), sa.Column("status", sa.String(30), nullable=False, server_default="REQUESTED"), sa.Column("provider_ref", sa.String(100)), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()))

def downgrade():
    for table in ["refunds", "payments", "bookings", "cinema_seats", "cinema_shows", "cinemas", "flights", "bus_seats", "buses", "users"]:
        op.drop_table(table)
