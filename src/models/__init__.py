"""
Data models for the Learning Progress Tracker

This module defines the core data structures used throughout the application.
Perfect for beginners to understand object-oriented programming concepts.
"""

from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class Course:
    """Represents a learning course"""
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    duration_hours: int = 0
    difficulty_level: int = 1  # 1-5 scale
    category: str = ""
    created_date: datetime = None
    
    def __post_init__(self):
        if self.created_date is None:
            self.created_date = datetime.now()
    
    def is_beginner_friendly(self) -> bool:
        """Check if course is suitable for beginners"""
        return self.difficulty_level <= 2


@dataclass 
class StudySession:
    """Represents a single study session"""
    id: Optional[int] = None
    course_id: int = 0
    start_time: datetime = None
    end_time: Optional[datetime] = None
    notes: str = ""
    rating: Optional[int] = None  # 1-5 how well the session went
    
    def __post_init__(self):
        if self.start_time is None:
            self.start_time = datetime.now()
    
    @property
    def duration_minutes(self) -> int:
        """Calculate session duration in minutes"""
        if self.end_time:
            delta = self.end_time - self.start_time
            return int(delta.total_seconds() / 60)
        return 0
    
    def is_completed(self) -> bool:
        """Check if session is completed"""
        return self.end_time is not None


@dataclass
class LearningGoal:
    """Represents a learning goal or milestone"""
    id: Optional[int] = None
    title: str = ""
    description: str = ""
    target_date: Optional[datetime] = None
    is_completed: bool = False
    course_id: Optional[int] = None
    
    def days_until_target(self) -> Optional[int]:
        """Calculate days until target date"""
        if self.target_date:
            delta = self.target_date - datetime.now()
            return delta.days
        return None


@dataclass
class User:
    """Represents a user of the system"""
    id: Optional[int] = None
    username: str = ""
    email: str = ""
    created_date: datetime = None
    total_study_hours: float = 0.0
    
    def __post_init__(self):
        if self.created_date is None:
            self.created_date = datetime.now()
    
    def add_study_time(self, minutes: int):
        """Add study time to user's total"""
        self.total_study_hours += minutes / 60.0