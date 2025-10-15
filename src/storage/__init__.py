"""
Data storage and persistence layer

This module handles all database operations for the Learning Progress Tracker.
Great for beginners to learn about database interactions and SQL basics.
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Optional
from ..models import Course, StudySession, LearningGoal, User


class DatabaseManager:
    """Handles all database operations"""
    
    def __init__(self, db_path: str = "data/learning_tracker.db"):
        self.db_path = db_path
        self.ensure_database_exists()
        self.create_tables()
    
    def ensure_database_exists(self):
        """Create database directory if it doesn't exist"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def create_tables(self):
        """Create all necessary tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table creation
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    created_date TEXT NOT NULL,
                    total_study_hours REAL DEFAULT 0.0
                )
            ''')
            
            # Courses table creation
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    duration_hours INTEGER DEFAULT 0,
                    difficulty_level INTEGER DEFAULT 1,
                    category TEXT,
                    created_date TEXT NOT NULL
                )
            ''')
            
            # Study sessions table creation
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS study_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_id INTEGER NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    notes TEXT,
                    rating INTEGER,
                    FOREIGN KEY (course_id) REFERENCES courses (id)
                )
            ''')
            
            # Learning goals table creation
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS learning_goals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    target_date TEXT,
                    is_completed BOOLEAN DEFAULT FALSE,
                    course_id INTEGER,
                    FOREIGN KEY (course_id) REFERENCES courses (id)
                )
            ''')
            
            conn.commit()
    
    # Course operations
    def add_course(self, course: Course) -> int:
        """Add a new course to the database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO courses (name, description, duration_hours, 
                                   difficulty_level, category, created_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (course.name, course.description, course.duration_hours,
                  course.difficulty_level, course.category, 
                  course.created_date.isoformat()))
            return cursor.lastrowid
    
    def get_all_courses(self) -> List[Course]:
        """Get all courses from the database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM courses')
            rows = cursor.fetchall()
            
            courses = []
            for row in rows:
                course = Course(
                    id=row[0],
                    name=row[1],
                    description=row[2],
                    duration_hours=row[3],
                    difficulty_level=row[4],
                    category=row[5],
                    created_date=datetime.fromisoformat(row[6])
                )
                courses.append(course)
            return courses
    
    def get_course_by_id(self, course_id: int) -> Optional[Course]:
        """Get a specific course by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM courses WHERE id = ?', (course_id,))
            row = cursor.fetchone()
            
            if row:
                return Course(
                    id=row[0],
                    name=row[1],
                    description=row[2],
                    duration_hours=row[3],
                    difficulty_level=row[4],
                    category=row[5],
                    created_date=datetime.fromisoformat(row[6])
                )
            return None
    
    # Study session operations  
    def add_study_session(self, session: StudySession) -> int:
        """Add a new study session"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            end_time_str = session.end_time.isoformat() if session.end_time else None
            cursor.execute('''
                INSERT INTO study_sessions (course_id, start_time, end_time, notes, rating)
                VALUES (?, ?, ?, ?, ?)
            ''', (session.course_id, session.start_time.isoformat(), 
                  end_time_str, session.notes, session.rating))
            return cursor.lastrowid
    
    def get_sessions_for_course(self, course_id: int) -> List[StudySession]:
        """Get all study sessions for a specific course"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM study_sessions WHERE course_id = ?', (course_id,))
            rows = cursor.fetchall()
            
            sessions = []
            for row in rows:
                session = StudySession(
                    id=row[0],
                    course_id=row[1],
                    start_time=datetime.fromisoformat(row[2]),
                    end_time=datetime.fromisoformat(row[3]) if row[3] else None,
                    notes=row[4],
                    rating=row[5]
                )
                sessions.append(session)
            return sessions