"""add passenger and cancellation details

Revision ID: 0003_booking_details
Revises: 0002_booking_hold
"""

from alembic import op
import sqlalchemy as sa

revision = "0003_booking_details"
down_revision = "0002_booking_hold"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "bookings",
        sa.Column("passenger_name", sa.String(120), nullable=True),
    )
    op.add_column(
        "bookings",
        sa.Column("passenger_age", sa.Integer(), nullable=True),
    )
    op.add_column(
        "bookings",
        sa.Column("passenger_gender", sa.String(20), nullable=True),
    )
    op.add_column(
        "bookings",
        sa.Column("passenger_phone", sa.String(20), nullable=True),
    )
    op.add_column(
        "bookings",
        sa.Column("passenger_email", sa.String(255), nullable=True),
    )
    op.add_column(
        "bookings",
        sa.Column("cancelled_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "bookings",
        sa.Column("cancellation_reason", sa.String(255), nullable=True),
    )


def downgrade():
    op.drop_column("bookings", "cancellation_reason")
    op.drop_column("bookings", "cancelled_at")
    op.drop_column("bookings", "passenger_email")
    op.drop_column("bookings", "passenger_phone")
    op.drop_column("bookings", "passenger_gender")
    op.drop_column("bookings", "passenger_age")
    op.drop_column("bookings", "passenger_name")
