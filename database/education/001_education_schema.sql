-- Ramdev Travels / Education Platform
-- PostgreSQL schema: modular, UUID based, soft-delete friendly.
-- The education module is isolated in the `education` schema so travel tables can remain untouched.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS education;

CREATE TYPE education.user_status AS ENUM ('active','inactive','blocked','pending');
CREATE TYPE education.course_status AS ENUM ('draft','published','archived');
CREATE TYPE education.enrollment_status AS ENUM ('active','completed','paused','cancelled');
CREATE TYPE education.test_status AS ENUM ('draft','published','archived');
CREATE TYPE education.question_type AS ENUM ('single_choice','multiple_choice','true_false','short_answer');
CREATE TYPE education.attempt_status AS ENUM ('in_progress','submitted','evaluated','expired');
CREATE TYPE education.omr_status AS ENUM ('uploaded','processing','evaluated','failed');
CREATE TYPE education.content_status AS ENUM ('draft','published','archived');

CREATE TABLE education.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(320) NOT NULL UNIQUE,
    phone VARCHAR(20) UNIQUE,
    password_hash TEXT NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    avatar_url TEXT,
    status education.user_status NOT NULL DEFAULT 'active',
    last_login_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

CREATE TABLE education.roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(40) NOT NULL UNIQUE,
    name VARCHAR(80) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE education.permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE education.user_roles (
    user_id UUID NOT NULL REFERENCES education.users(id) ON DELETE CASCADE,
    role_id UUID NOT NULL REFERENCES education.roles(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
);

CREATE TABLE education.role_permissions (
    role_id UUID NOT NULL REFERENCES education.roles(id) ON DELETE CASCADE,
    permission_id UUID NOT NULL REFERENCES education.permissions(id) ON DELETE CASCADE,
    PRIMARY KEY (role_id, permission_id)
);

CREATE TABLE education.student_profiles (
    user_id UUID PRIMARY KEY REFERENCES education.users(id) ON DELETE CASCADE,
    roll_no VARCHAR(50) UNIQUE,
    date_of_birth DATE,
    school_name VARCHAR(200),
    class_name VARCHAR(80),
    district VARCHAR(100),
    state VARCHAR(100) DEFAULT 'Rajasthan',
    target_exam VARCHAR(100),
    bio TEXT
);

CREATE TABLE education.teacher_profiles (
    user_id UUID PRIMARY KEY REFERENCES education.users(id) ON DELETE CASCADE,
    employee_code VARCHAR(50) UNIQUE,
    qualification TEXT,
    experience_years NUMERIC(4,1),
    specialization TEXT,
    bio TEXT
);

CREATE TABLE education.subjects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(40) UNIQUE,
    name VARCHAR(120) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE education.courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(50) NOT NULL UNIQUE,
    title VARCHAR(180) NOT NULL,
    slug VARCHAR(220) NOT NULL UNIQUE,
    description TEXT,
    thumbnail_url TEXT,
    status education.course_status NOT NULL DEFAULT 'draft',
    teacher_id UUID REFERENCES education.users(id) ON DELETE SET NULL,
    duration_minutes INTEGER,
    price NUMERIC(12,2) NOT NULL DEFAULT 0,
    is_free BOOLEAN NOT NULL DEFAULT TRUE,
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

CREATE TABLE education.course_subjects (
    course_id UUID NOT NULL REFERENCES education.courses(id) ON DELETE CASCADE,
    subject_id UUID NOT NULL REFERENCES education.subjects(id) ON DELETE RESTRICT,
    sort_order INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (course_id, subject_id)
);

CREATE TABLE education.course_modules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id UUID NOT NULL REFERENCES education.courses(id) ON DELETE CASCADE,
    title VARCHAR(180) NOT NULL,
    description TEXT,
    sort_order INTEGER NOT NULL DEFAULT 0,
    status education.content_status NOT NULL DEFAULT 'draft',
    UNIQUE(course_id, sort_order)
);

CREATE TABLE education.lessons (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    module_id UUID NOT NULL REFERENCES education.course_modules(id) ON DELETE CASCADE,
    title VARCHAR(180) NOT NULL,
    description TEXT,
    video_url TEXT,
    duration_minutes INTEGER,
    sort_order INTEGER NOT NULL DEFAULT 0,
    status education.content_status NOT NULL DEFAULT 'draft',
    UNIQUE(module_id, sort_order)
);

CREATE TABLE education.materials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lesson_id UUID REFERENCES education.lessons(id) ON DELETE CASCADE,
    course_id UUID REFERENCES education.courses(id) ON DELETE CASCADE,
    title VARCHAR(180) NOT NULL,
    file_url TEXT,
    material_type VARCHAR(40) NOT NULL DEFAULT 'pdf',
    size_bytes BIGINT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CHECK (lesson_id IS NOT NULL OR course_id IS NOT NULL)
);

CREATE TABLE education.enrollments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES education.users(id) ON DELETE CASCADE,
    course_id UUID NOT NULL REFERENCES education.courses(id) ON DELETE CASCADE,
    status education.enrollment_status NOT NULL DEFAULT 'active',
    enrolled_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at TIMESTAMPTZ,
    progress_percent NUMERIC(5,2) NOT NULL DEFAULT 0 CHECK (progress_percent BETWEEN 0 AND 100),
    UNIQUE(student_id, course_id)
);

CREATE TABLE education.lesson_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES education.users(id) ON DELETE CASCADE,
    lesson_id UUID NOT NULL REFERENCES education.lessons(id) ON DELETE CASCADE,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    watched_seconds INTEGER NOT NULL DEFAULT 0,
    last_viewed_at TIMESTAMPTZ,
    UNIQUE(student_id, lesson_id)
);

CREATE TABLE education.tests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id UUID REFERENCES education.courses(id) ON DELETE SET NULL,
    subject_id UUID REFERENCES education.subjects(id) ON DELETE SET NULL,
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(220) NOT NULL UNIQUE,
    description TEXT,
    status education.test_status NOT NULL DEFAULT 'draft',
    duration_minutes INTEGER NOT NULL DEFAULT 60,
    total_marks NUMERIC(8,2) NOT NULL DEFAULT 0,
    negative_mark_per_question NUMERIC(8,2) NOT NULL DEFAULT 0,
    total_questions INTEGER NOT NULL DEFAULT 0,
    starts_at TIMESTAMPTZ,
    ends_at TIMESTAMPTZ,
    created_by UUID REFERENCES education.users(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE education.questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    test_id UUID NOT NULL REFERENCES education.tests(id) ON DELETE CASCADE,
    question_no INTEGER NOT NULL,
    body TEXT NOT NULL,
    question_type education.question_type NOT NULL DEFAULT 'single_choice',
    marks NUMERIC(8,2) NOT NULL DEFAULT 1,
    explanation TEXT,
    UNIQUE(test_id, question_no)
);

CREATE TABLE education.question_options (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question_id UUID NOT NULL REFERENCES education.questions(id) ON DELETE CASCADE,
    option_key CHAR(1) NOT NULL,
    option_text TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE(question_id, option_key)
);

CREATE TABLE education.test_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    test_id UUID NOT NULL REFERENCES education.tests(id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES education.users(id) ON DELETE CASCADE,
    status education.attempt_status NOT NULL DEFAULT 'in_progress',
    started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    submitted_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    score NUMERIC(10,2),
    correct_count INTEGER NOT NULL DEFAULT 0,
    wrong_count INTEGER NOT NULL DEFAULT 0,
    unanswered_count INTEGER NOT NULL DEFAULT 0,
    percentile NUMERIC(6,2),
    rank INTEGER,
    UNIQUE(test_id, student_id, started_at)
);

CREATE TABLE education.attempt_answers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    attempt_id UUID NOT NULL REFERENCES education.test_attempts(id) ON DELETE CASCADE,
    question_id UUID NOT NULL REFERENCES education.questions(id) ON DELETE CASCADE,
    selected_option_ids UUID[] NOT NULL DEFAULT '{}',
    answer_text TEXT,
    is_correct BOOLEAN,
    marks_awarded NUMERIC(8,2) NOT NULL DEFAULT 0,
    answered_at TIMESTAMPTZ,
    UNIQUE(attempt_id, question_id)
);

CREATE TABLE education.results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    attempt_id UUID NOT NULL UNIQUE REFERENCES education.test_attempts(id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES education.users(id) ON DELETE CASCADE,
    test_id UUID NOT NULL REFERENCES education.tests(id) ON DELETE CASCADE,
    score NUMERIC(10,2) NOT NULL,
    max_score NUMERIC(10,2) NOT NULL,
    percentage NUMERIC(6,2) NOT NULL,
    correct_count INTEGER NOT NULL DEFAULT 0,
    wrong_count INTEGER NOT NULL DEFAULT 0,
    unanswered_count INTEGER NOT NULL DEFAULT 0,
    rank INTEGER,
    percentile NUMERIC(6,2),
    generated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE education.omr_submissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    test_id UUID REFERENCES education.tests(id) ON DELETE SET NULL,
    student_id UUID REFERENCES education.users(id) ON DELETE SET NULL,
    roll_no VARCHAR(50),
    file_url TEXT NOT NULL,
    status education.omr_status NOT NULL DEFAULT 'uploaded',
    detected_answers JSONB,
    evaluated_result JSONB,
    error_message TEXT,
    uploaded_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    processed_at TIMESTAMPTZ
);

CREATE TABLE education.notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES education.users(id) ON DELETE CASCADE,
    title VARCHAR(180) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(40) NOT NULL DEFAULT 'system',
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE education.audit_logs (
    id BIGSERIAL PRIMARY KEY,
    actor_user_id UUID REFERENCES education.users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100),
    entity_id UUID,
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_enrollments_student ON education.enrollments(student_id);
CREATE INDEX idx_enrollments_course ON education.enrollments(course_id);
CREATE INDEX idx_questions_test ON education.questions(test_id);
CREATE INDEX idx_attempts_student ON education.test_attempts(student_id);
CREATE INDEX idx_results_test_score ON education.results(test_id, score DESC);
CREATE INDEX idx_notifications_user ON education.notifications(user_id, is_read);
CREATE INDEX idx_audit_actor_created ON education.audit_logs(actor_user_id, created_at DESC);

INSERT INTO education.roles(code,name) VALUES
('student','Student'),('teacher','Teacher'),('admin','Admin')
ON CONFLICT (code) DO NOTHING;

INSERT INTO education.subjects(code,name) VALUES
('RJ-GK','Rajasthan GK'),('MATH','Mathematics'),('REASONING','Reasoning'),
('SCIENCE','General Science'),('HINDI','Hindi'),('ENGLISH','English')
ON CONFLICT (code) DO NOTHING;
