# API Documentation

## Overview

The Learning Progress Tracker provides both REST API endpoints and CLI commands for managing courses, study sessions, goals, and analytics.

## REST API Endpoints

### Base URL
```
http://localhost:5000/api
```

### Authentication
Currently using session-based authentication. Future versions will support JWT tokens.

## Courses API

### GET /api/courses
Get all courses

**Response:**
```json
{
  "courses": [
    {
      "id": 1,
      "name": "Python Fundamentals",
      "description": "Learn Python basics",
      "duration_hours": 40,
      "difficulty_level": 2,
      "category": "Programming",
      "created_date": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 1
}
```

### POST /api/courses
Create a new course

**Request Body:**
```json
{
  "name": "Advanced Python",
  "description": "Deep dive into Python",
  "duration_hours": 60,
  "difficulty_level": 4,
  "category": "Programming"
}
```

**Response:**
```json
{
  "id": 2,
  "message": "Course created successfully"
}
```

### GET /api/courses/{id}
Get a specific course

**Response:**
```json
{
  "id": 1,
  "name": "Python Fundamentals",
  "description": "Learn Python basics",
  "duration_hours": 40,
  "difficulty_level": 2,
  "category": "Programming",
  "created_date": "2024-01-15T10:30:00Z",
  "sessions": [
    {
      "id": 1,
      "start_time": "2024-01-16T14:00:00Z",
      "end_time": "2024-01-16T15:30:00Z",
      "duration_minutes": 90,
      "notes": "Good progress on variables",
      "rating": 4
    }
  ]
}
```

### PUT /api/courses/{id}
Update a course

**Request Body:**
```json
{
  "name": "Python Fundamentals Updated",
  "description": "Updated description",
  "duration_hours": 45
}
```

### DELETE /api/courses/{id}
Delete a course

**Response:**
```json
{
  "message": "Course deleted successfully"
}
```

## Study Sessions API

### GET /api/sessions
Get all study sessions

**Query Parameters:**
- `course_id` (optional): Filter by course ID
- `limit` (optional): Limit number of results (default: 50)
- `offset` (optional): Offset for pagination (default: 0)

**Response:**
```json
{
  "sessions": [
    {
      "id": 1,
      "course_id": 1,
      "start_time": "2024-01-16T14:00:00Z",
      "end_time": "2024-01-16T15:30:00Z",
      "duration_minutes": 90,
      "notes": "Good progress",
      "rating": 4
    }
  ],
  "total": 1
}
```

### POST /api/sessions
Start a new study session

**Request Body:**
```json
{
  "course_id": 1,
  "notes": "Starting new chapter"
}
```

**Response:**
```json
{
  "id": 2,
  "message": "Study session started",
  "start_time": "2024-01-16T16:00:00Z"
}
```

### PUT /api/sessions/{id}/end
End a study session

**Request Body:**
```json
{
  "rating": 4,
  "notes": "Completed successfully"
}
```

**Response:**
```json
{
  "message": "Session ended successfully",
  "duration_minutes": 75
}
```

## Analytics API

### GET /api/analytics/stats
Get overall statistics

**Response:**
```json
{
  "total_courses": 5,
  "completed_courses": 2,
  "in_progress": 3,
  "not_started": 0,
  "total_study_hours": 45.5,
  "study_streak": 7,
  "average_session_rating": 4.2
}
```

### GET /api/analytics/weekly-progress
Get weekly study progress

**Query Parameters:**
- `weeks` (optional): Number of weeks (default: 4)

**Response:**
```json
{
  "weekly_data": {
    "Week of Oct 01": 8.5,
    "Week of Oct 08": 12.0,
    "Week of Oct 15": 10.5,
    "Week of Oct 22": 14.0
  }
}
```

### GET /api/analytics/course-difficulty
Get course difficulty distribution

**Response:**
```json
{
  "difficulty_distribution": {
    "Beginner (1-2)": 3,
    "Intermediate (3)": 2,
    "Advanced (4-5)": 1
  }
}
```

### POST /api/analytics/generate-report
Generate comprehensive progress report

**Response:**
```json
{
  "report": {
    "total_study_hours": 45.5,
    "courses_completed": 2,
    "average_session_rating": 4.2,
    "study_streak": 7,
    "weekly_progress": { ... },
    "course_difficulty_distribution": { ... },
    "generated_date": "2024-01-16T10:00:00Z"
  },
  "chart_url": "/static/charts/progress_chart.png"
}
```

## Goals API

### GET /api/goals
Get all learning goals

**Response:**
```json
{
  "goals": [
    {
      "id": 1,
      "title": "Complete Python Course",
      "description": "Finish all modules",
      "target_date": "2024-12-31T23:59:59Z",
      "is_completed": false,
      "course_id": 1,
      "days_until_target": 45
    }
  ]
}
```

### POST /api/goals
Create a new learning goal

**Request Body:**
```json
{
  "title": "Master Data Analysis",
  "description": "Complete pandas course",
  "target_date": "2024-11-30T23:59:59Z",
  "course_id": 3
}
```

### PUT /api/goals/{id}/complete
Mark a goal as completed

**Response:**
```json
{
  "message": "Goal marked as completed",
  "completed_date": "2024-01-16T10:00:00Z"
}
```

## CLI Commands Reference

### Course Management
```bash
# Add a new course
python -m src.cli.main add-course

# List all courses
python -m src.cli.main list-courses

# Show course details
python -m src.cli.main show-course --id=1
```

### Study Session Management
```bash
# Start a study session
python -m src.cli.main start-session --course-id=1

# End a study session
python -m src.cli.main end-session --session-id=1 --rating=4

# List recent sessions
python -m src.cli.main list-sessions --recent=10
```

### Analytics
```bash
# Show statistics
python -m src.cli.main show-stats

# Generate progress report
python -m src.cli.main generate-report

# Export data
python -m src.cli.main export-data --format=csv
```

### Goal Management
```bash
# Add a learning goal
python -m src.cli.main add-goal

# List goals
python -m src.cli.main list-goals

# Complete a goal
python -m src.cli.main complete-goal --id=1
```

## Error Responses

### Standard Error Format
```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Course with ID 999 not found",
    "timestamp": "2024-01-16T10:00:00Z"
  }
}
```

### Common Error Codes
- `VALIDATION_ERROR` (400): Invalid input data
- `RESOURCE_NOT_FOUND` (404): Requested resource doesn't exist
- `DUPLICATE_RESOURCE` (409): Resource already exists
- `INTERNAL_ERROR` (500): Server error

## Rate Limiting

Currently no rate limiting is implemented. Future versions will include:
- 100 requests per minute per IP
- 1000 requests per hour per authenticated user

## Webhooks (Future Feature)

Planned webhook events:
- `course.created`
- `session.completed`
- `goal.achieved`
- `milestone.reached`

## SDK Examples

### Python SDK Usage
```python
from learning_tracker import Client

client = Client(base_url="http://localhost:5000/api")

# Create a course
course = client.courses.create({
    "name": "Python Basics",
    "duration_hours": 20,
    "difficulty_level": 2
})

# Start a session
session = client.sessions.start(course.id)

# Get analytics
stats = client.analytics.get_stats()
```

### JavaScript SDK Usage
```javascript
import { LearningTracker } from 'learning-tracker-js';

const client = new LearningTracker('http://localhost:5000/api');

// Create course
const course = await client.courses.create({
  name: 'JavaScript Fundamentals',
  duration_hours: 30,
  difficulty_level: 2
});

// Get weekly progress
const progress = await client.analytics.getWeeklyProgress();
```