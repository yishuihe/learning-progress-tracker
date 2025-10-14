# Database Schema Documentation

## Overview

The Learning Progress Tracker uses SQLite as its primary database for storing user learning data. The database is designed to be simple, efficient, and suitable for both single-user and small team deployments.

## Database File Location
- **Development**: `data/learning_tracker.db`
- **Testing**: `data/test_learning_tracker.db`
- **Production**: Configurable via environment variables

## Schema Diagram

```
┌─────────────────┐       ┌─────────────────┐
│     users       │       │    courses      │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │
│ username        │       │ name            │
│ email           │       │ description     │
│ created_date    │       │ duration_hours  │
│ total_study_hrs │       │ difficulty_lvl  │
└─────────────────┘       │ category        │
                          │ created_date    │
                          └─────────────────┘
                                   │
                                   │ 1:N
                                   ▼
                          ┌─────────────────┐
                          │ study_sessions  │
                          ├─────────────────┤
                          │ id (PK)         │
                          │ course_id (FK)  │
                          │ start_time      │
                          │ end_time        │
                          │ notes           │
                          │ rating          │
                          └─────────────────┘

┌─────────────────┐
│ learning_goals  │
├─────────────────┤
│ id (PK)         │
│ title           │
│ description     │
│ target_date     │
│ is_completed    │
│ course_id (FK)  │ ──────┐
└─────────────────┘       │
                          │ N:1
                          ▼
                  ┌─────────────────┐
                  │    courses      │
                  │      (ref)      │
                  └─────────────────┘
```

## Tables

### users
Stores user information and profile data.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique user identifier |
| username | TEXT | UNIQUE, NOT NULL | User's unique username |
| email | TEXT | UNIQUE, NOT NULL | User's email address |
| created_date | TEXT | NOT NULL | Account creation timestamp (ISO format) |
| total_study_hours | REAL | DEFAULT 0.0 | Total accumulated study hours |

**Indexes:**
```sql
CREATE UNIQUE INDEX idx_users_username ON users(username);
CREATE UNIQUE INDEX idx_users_email ON users(email);
```

**Example Data:**
```sql
INSERT INTO users (username, email, created_date, total_study_hours) 
VALUES ('john_doe', 'john@example.com', '2024-01-15T10:30:00Z', 45.5);
```

### courses
Stores course information and metadata.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique course identifier |
| name | TEXT | NOT NULL | Course name/title |
| description | TEXT | NULL | Detailed course description |
| duration_hours | INTEGER | DEFAULT 0 | Expected course duration in hours |
| difficulty_level | INTEGER | DEFAULT 1, CHECK(1 <= difficulty_level <= 5) | Course difficulty (1-5 scale) |
| category | TEXT | NULL | Course category/subject |
| created_date | TEXT | NOT NULL | Course creation timestamp (ISO format) |

**Indexes:**
```sql
CREATE INDEX idx_courses_category ON courses(category);
CREATE INDEX idx_courses_difficulty ON courses(difficulty_level);
CREATE INDEX idx_courses_created_date ON courses(created_date);
```

**Example Data:**
```sql
INSERT INTO courses (name, description, duration_hours, difficulty_level, category, created_date)
VALUES ('Python Fundamentals', 'Learn Python basics', 40, 2, 'Programming', '2024-01-15T10:30:00Z');
```

### study_sessions
Tracks individual study sessions for courses.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique session identifier |
| course_id | INTEGER | NOT NULL, FOREIGN KEY → courses(id) | Reference to associated course |
| start_time | TEXT | NOT NULL | Session start timestamp (ISO format) |
| end_time | TEXT | NULL | Session end timestamp (ISO format) |
| notes | TEXT | NULL | User notes about the session |
| rating | INTEGER | CHECK(1 <= rating <= 5) | Session quality rating (1-5) |

**Foreign Keys:**
```sql
FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
```

**Indexes:**
```sql
CREATE INDEX idx_sessions_course_id ON study_sessions(course_id);
CREATE INDEX idx_sessions_start_time ON study_sessions(start_time);
CREATE INDEX idx_sessions_rating ON study_sessions(rating);
```

**Example Data:**
```sql
INSERT INTO study_sessions (course_id, start_time, end_time, notes, rating)
VALUES (1, '2024-01-16T14:00:00Z', '2024-01-16T15:30:00Z', 'Great progress on variables', 4);
```

### learning_goals
Stores user learning goals and milestones.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique goal identifier |
| title | TEXT | NOT NULL | Goal title/name |
| description | TEXT | NULL | Detailed goal description |
| target_date | TEXT | NULL | Target completion date (ISO format) |
| is_completed | BOOLEAN | DEFAULT FALSE | Completion status |
| course_id | INTEGER | NULL, FOREIGN KEY → courses(id) | Optional associated course |

**Foreign Keys:**
```sql
FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE SET NULL
```

**Indexes:**
```sql
CREATE INDEX idx_goals_target_date ON learning_goals(target_date);
CREATE INDEX idx_goals_is_completed ON learning_goals(is_completed);
CREATE INDEX idx_goals_course_id ON learning_goals(course_id);
```

**Example Data:**
```sql
INSERT INTO learning_goals (title, description, target_date, is_completed, course_id)
VALUES ('Complete Python Course', 'Finish all modules', '2024-12-31T23:59:59Z', FALSE, 1);
```

## Views

### course_progress_view
Aggregated view showing course progress statistics.

```sql
CREATE VIEW course_progress_view AS
SELECT 
    c.id,
    c.name,
    c.category,
    c.difficulty_level,
    c.duration_hours,
    COUNT(s.id) as total_sessions,
    COALESCE(SUM(
        CASE 
            WHEN s.end_time IS NOT NULL 
            THEN (julianday(s.end_time) - julianday(s.start_time)) * 24 * 60
            ELSE 0 
        END
    ), 0) as total_minutes_studied,
    COALESCE(AVG(s.rating), 0) as average_rating,
    MAX(s.start_time) as last_studied
FROM courses c
LEFT JOIN study_sessions s ON c.id = s.course_id
GROUP BY c.id, c.name, c.category, c.difficulty_level, c.duration_hours;
```

### weekly_progress_view
Shows weekly study progress aggregation.

```sql
CREATE VIEW weekly_progress_view AS
SELECT 
    strftime('%Y-%W', s.start_time) as week_year,
    strftime('%Y-%m-%d', s.start_time, 'weekday 0', '-7 days') as week_start,
    COUNT(s.id) as sessions_count,
    SUM(
        CASE 
            WHEN s.end_time IS NOT NULL 
            THEN (julianday(s.end_time) - julianday(s.start_time)) * 24
            ELSE 0 
        END
    ) as total_hours,
    AVG(s.rating) as average_rating
FROM study_sessions s
WHERE s.end_time IS NOT NULL
GROUP BY strftime('%Y-%W', s.start_time)
ORDER BY week_year DESC;
```

## Triggers

### update_user_study_hours
Automatically updates user's total study hours when sessions are completed.

```sql
CREATE TRIGGER update_user_study_hours
    AFTER UPDATE OF end_time ON study_sessions
    WHEN NEW.end_time IS NOT NULL AND OLD.end_time IS NULL
BEGIN
    UPDATE users 
    SET total_study_hours = total_study_hours + 
        (julianday(NEW.end_time) - julianday(NEW.start_time)) * 24
    WHERE id = (
        SELECT user_id FROM courses WHERE id = NEW.course_id
    );
END;
```

### validate_session_times
Ensures end_time is after start_time for study sessions.

```sql
CREATE TRIGGER validate_session_times
    BEFORE UPDATE OF end_time ON study_sessions
    WHEN NEW.end_time IS NOT NULL
BEGIN
    SELECT CASE
        WHEN julianday(NEW.end_time) <= julianday(NEW.start_time) THEN
            RAISE(ABORT, 'End time must be after start time')
    END;
END;
```

## Common Queries

### Get user's learning statistics
```sql
SELECT 
    u.username,
    u.total_study_hours,
    COUNT(DISTINCT c.id) as total_courses,
    COUNT(DISTINCT s.id) as total_sessions,
    AVG(s.rating) as average_session_rating
FROM users u
LEFT JOIN courses c ON u.id = c.user_id
LEFT JOIN study_sessions s ON c.id = s.course_id
WHERE u.id = ?
GROUP BY u.id, u.username, u.total_study_hours;
```

### Get course completion progress
```sql
SELECT 
    c.name,
    c.duration_hours as target_hours,
    COALESCE(SUM(
        (julianday(s.end_time) - julianday(s.start_time)) * 24
    ), 0) as completed_hours,
    ROUND(
        COALESCE(SUM(
            (julianday(s.end_time) - julianday(s.start_time)) * 24
        ), 0) / c.duration_hours * 100, 2
    ) as completion_percentage
FROM courses c
LEFT JOIN study_sessions s ON c.id = s.course_id AND s.end_time IS NOT NULL
WHERE c.id = ?
GROUP BY c.id, c.name, c.duration_hours;
```

### Get recent study activity
```sql
SELECT 
    c.name as course_name,
    s.start_time,
    s.end_time,
    s.rating,
    s.notes,
    (julianday(s.end_time) - julianday(s.start_time)) * 24 * 60 as duration_minutes
FROM study_sessions s
JOIN courses c ON s.course_id = c.id
WHERE s.end_time IS NOT NULL
ORDER BY s.start_time DESC
LIMIT 10;
```

## Migration Scripts

### Version 1.0 → 1.1: Add user_id to courses
```sql
-- Add user_id column to courses table
ALTER TABLE courses ADD COLUMN user_id INTEGER;

-- Create foreign key relationship
-- Note: SQLite doesn't support ADD CONSTRAINT, so we need to recreate the table
-- (This would be handled by the migration system)

-- Add index for performance
CREATE INDEX idx_courses_user_id ON courses(user_id);
```

### Version 1.1 → 1.2: Add reminders table
```sql
CREATE TABLE reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    reminder_time TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    course_id INTEGER,
    created_date TEXT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE SET NULL
);

CREATE INDEX idx_reminders_reminder_time ON reminders(reminder_time);
CREATE INDEX idx_reminders_is_active ON reminders(is_active);
```

## Performance Considerations

### Recommended Indexes
```sql
-- For frequent course lookups
CREATE INDEX idx_courses_name ON courses(name);

-- For session analytics
CREATE INDEX idx_sessions_date_range ON study_sessions(start_time, end_time);

-- For goal tracking
CREATE INDEX idx_goals_target_completion ON learning_goals(target_date, is_completed);
```

### Query Optimization Tips
1. Use `LIMIT` for paginated results
2. Index columns used in `WHERE` clauses
3. Use prepared statements for repeated queries
4. Consider using `EXPLAIN QUERY PLAN` for complex queries

## Backup Strategy

### Daily Backups
```bash
# Create daily backup
sqlite3 data/learning_tracker.db ".backup data/backups/backup_$(date +%Y%m%d).db"

# Compress backup
gzip "data/backups/backup_$(date +%Y%m%d).db"
```

### Data Export
```sql
-- Export to CSV
.mode csv
.output data/exports/courses_export.csv
SELECT * FROM courses;

.output data/exports/sessions_export.csv
SELECT * FROM study_sessions;
```

## Testing Data

### Sample Data Script
```sql
-- Insert test users
INSERT INTO users (username, email, created_date) VALUES 
    ('test_user', 'test@example.com', '2024-01-01T00:00:00Z');

-- Insert test courses
INSERT INTO courses (name, description, duration_hours, difficulty_level, category, created_date) VALUES
    ('Python Basics', 'Fundamental Python concepts', 20, 2, 'Programming', '2024-01-01T00:00:00Z'),
    ('Web Development', 'Build web applications', 40, 3, 'Web Development', '2024-01-02T00:00:00Z');

-- Insert test sessions
INSERT INTO study_sessions (course_id, start_time, end_time, rating, notes) VALUES
    (1, '2024-01-10T10:00:00Z', '2024-01-10T11:30:00Z', 4, 'Good progress'),
    (1, '2024-01-11T14:00:00Z', '2024-01-11T15:00:00Z', 5, 'Excellent session');
```