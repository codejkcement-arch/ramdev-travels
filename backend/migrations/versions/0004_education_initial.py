"""Education platform initial schema

Revision ID: 0002_education_initial
Revises: 0001_initial
"""

from alembic import op
import sqlalchemy as sa


revision = "0004_education_initial"
down_revision = "0003_booking_details"
branch_labels = None
depends_on = None


def upgrade() -> None:

    # -------------------------
    # Student Profiles
    # -------------------------
    op.create_table(
        "education_students",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("roll_number", sa.String(50), unique=True),
        sa.Column("class_name", sa.String(50)),
        sa.Column("section", sa.String(20)),
        sa.Column("school_name", sa.String(200)),
        sa.Column("father_name", sa.String(120)),
        sa.Column("mother_name", sa.String(120)),
        sa.Column("date_of_birth", sa.Date()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # -------------------------
    # Teacher Profiles
    # -------------------------
    op.create_table(
        "education_teachers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("employee_id", sa.String(50), unique=True),
        sa.Column("qualification", sa.String(255)),
        sa.Column("specialization", sa.String(255)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # -------------------------
    # Courses
    # -------------------------
    op.create_table(
        "education_courses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("class_name", sa.String(50)),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # -------------------------
    # Subjects
    # -------------------------
    op.create_table(
        "education_subjects",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "course_id",
            sa.Integer(),
            sa.ForeignKey("education_courses.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("code", sa.String(50), unique=True),
        sa.Column("description", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # -------------------------
    # Tests
    # -------------------------
    op.create_table(
        "education_tests",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "subject_id",
            sa.Integer(),
            sa.ForeignKey("education_subjects.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "created_by",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("duration_minutes", sa.Integer(), nullable=False, server_default="60"),
        sa.Column("total_marks", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("negative_marking", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("negative_marks", sa.Numeric(5, 2), nullable=False, server_default="0"),
        sa.Column("is_published", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # -------------------------
    # Questions
    # -------------------------
    op.create_table(
        "education_questions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("question_text", sa.Text(), nullable=False),
        sa.Column("question_type", sa.String(30), nullable=False, server_default="MCQ"),
        sa.Column("option_a", sa.Text()),
        sa.Column("option_b", sa.Text()),
        sa.Column("option_c", sa.Text()),
        sa.Column("option_d", sa.Text()),
        sa.Column("correct_answer", sa.String(1)),
        sa.Column("marks", sa.Numeric(5, 2), nullable=False, server_default="1"),
        sa.Column("explanation", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # -------------------------
    # Test Questions
    # -------------------------
    op.create_table(
        "education_test_questions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "test_id",
            sa.Integer(),
            sa.ForeignKey("education_tests.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "question_id",
            sa.Integer(),
            sa.ForeignKey("education_questions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("question_number", sa.Integer(), nullable=False),
        sa.UniqueConstraint("test_id", "question_id"),
        sa.UniqueConstraint("test_id", "question_number"),
    )

    # -------------------------
    # Test Attempts
    # -------------------------
    op.create_table(
        "education_attempts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "test_id",
            sa.Integer(),
            sa.ForeignKey("education_tests.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "student_id",
            sa.Integer(),
            sa.ForeignKey("education_students.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("submitted_at", sa.DateTime(timezone=True)),
        sa.Column("status", sa.String(30), nullable=False, server_default="started"),
        sa.Column("score", sa.Numeric(8, 2), nullable=False, server_default="0"),
        sa.Column("correct_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("wrong_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("unanswered_count", sa.Integer(), nullable=False, server_default="0"),
    )

    # -------------------------
    # Student Answers
    # -------------------------
    op.create_table(
        "education_answers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "attempt_id",
            sa.Integer(),
            sa.ForeignKey("education_attempts.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "question_id",
            sa.Integer(),
            sa.ForeignKey("education_questions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("selected_answer", sa.String(1)),
        sa.Column("is_correct", sa.Boolean()),
        sa.Column("marks_obtained", sa.Numeric(8, 2), nullable=False, server_default="0"),
        sa.UniqueConstraint("attempt_id", "question_id"),
    )

    # -------------------------
    # Results / Ranking
    # -------------------------
    op.create_table(
        "education_results",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "attempt_id",
            sa.Integer(),
            sa.ForeignKey("education_attempts.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("total_marks", sa.Numeric(8, 2), nullable=False),
        sa.Column("percentage", sa.Numeric(6, 2), nullable=False),
        sa.Column("rank", sa.Integer()),
        sa.Column("result_status", sa.String(30), nullable=False, server_default="completed"),
        sa.Column("published_at", sa.DateTime(timezone=True)),
    )

    # -------------------------
    # OMR Sheets
    # -------------------------
    op.create_table(
        "education_omr_sheets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "test_id",
            sa.Integer(),
            sa.ForeignKey("education_tests.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "student_id",
            sa.Integer(),
            sa.ForeignKey("education_students.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("sheet_number", sa.String(100), unique=True, nullable=False),
        sa.Column("image_path", sa.String(500)),
        sa.Column("status", sa.String(30), nullable=False, server_default="uploaded"),
        sa.Column("score", sa.Numeric(8, 2), nullable=False, server_default="0"),
        sa.Column("processed_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # -------------------------
    # OMR Answers
    # -------------------------
    op.create_table(
        "education_omr_answers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "omr_sheet_id",
            sa.Integer(),
            sa.ForeignKey("education_omr_sheets.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "question_id",
            sa.Integer(),
            sa.ForeignKey("education_questions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("question_number", sa.Integer(), nullable=False),
        sa.Column("detected_answer", sa.String(1)),
        sa.Column("is_correct", sa.Boolean()),
        sa.Column("marks_obtained", sa.Numeric(8, 2), nullable=False, server_default="0"),
        sa.UniqueConstraint("omr_sheet_id", "question_id"),
    )


def downgrade() -> None:

    op.drop_table("education_omr_answers")
    op.drop_table("education_omr_sheets")
    op.drop_table("education_results")
    op.drop_table("education_answers")
    op.drop_table("education_attempts")
    op.drop_table("education_test_questions")
    op.drop_table("education_questions")
    op.drop_table("education_tests")
    op.drop_table("education_subjects")
    op.drop_table("education_courses")
    op.drop_table("education_teachers")
    op.drop_table("education_students")
