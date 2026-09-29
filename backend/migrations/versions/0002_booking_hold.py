"""add booking hold expiry
Revision ID: 0002_booking_hold
Revises: 0001_initial
"""
from alembic import op
import sqlalchemy as sa
revision = "0002_booking_hold"
down_revision = "0001_initial"
branch_labels = None
depends_on = None

def upgrade():
    op.add_column("bookings", sa.Column("hold_expires_at", sa.DateTime(timezone=True), nullable=True))
    op.create_index("ix_bookings_hold_expires_at", "bookings", ["hold_expires_at"])

def downgrade():
    op.drop_index("ix_bookings_hold_expires_at", table_name="bookings")
    op.drop_column("bookings", "hold_expires_at")
