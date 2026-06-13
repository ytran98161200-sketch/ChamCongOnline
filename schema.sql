CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password_hash TEXT,
    role VARCHAR(20),

    employee_code VARCHAR(20),

    department VARCHAR(100),

    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS employees(
    id SERIAL PRIMARY KEY,
    employee_code VARCHAR(50) UNIQUE,
    fullname VARCHAR(255),
    department VARCHAR(255),
    position VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS attendance(
    id SERIAL PRIMARY KEY,
    employee_code VARCHAR(50),
    work_date DATE,
    checkin TIMESTAMP,
    checkout TIMESTAMP
);
CREATE TABLE IF NOT EXISTS attendance (

    id SERIAL PRIMARY KEY,

    employee_code VARCHAR(20),

    work_date DATE,

    check_in TIMESTAMP,

    check_out TIMESTAMP,

    late_minutes INTEGER DEFAULT 0,

    early_leave_minutes INTEGER DEFAULT 0,

    overtime_minutes INTEGER DEFAULT 0,

    workday NUMERIC(4,2) DEFAULT 0

);

CREATE TABLE IF NOT EXISTS attendance_logs (

    id SERIAL PRIMARY KEY,

    employee_code VARCHAR(20),

    scan_time TIMESTAMP DEFAULT NOW()

);