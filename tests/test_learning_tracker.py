"""
Test suite for the Learning Progress Tracker

This module contains unit tests for all components.
Great for beginners to learn about testing concepts.
"""

import unittest
import os
import tempfile
from datetime import datetime
from src.models import Course, StudySession, LearningGoal, User
from src.storage import DatabaseManager


class TestModels(unittest.TestCase):
    """Test the data models"""
    
    def test_course_creation(self):
        """Test Course model creation"""
        course = Course(
            name="Python Basics",
            description="Learn Python fundamentals",
            duration_hours=40,
            difficulty_level=2,
            category="Programming"
        )
        
        self.assertEqual(course.name, "Python Basics")
        self.assertEqual(course.difficulty_level, 2)
        self.assertTrue(course.is_beginner_friendly())
        self.assertIsInstance(course.created_date, datetime)
    
    def test_study_session_duration(self):
        """Test StudySession duration calculation"""
        start_time = datetime(2024, 1, 1, 10, 0, 0)
        end_time = datetime(2024, 1, 1, 12, 30, 0)
        
        session = StudySession(
            course_id=1,
            start_time=start_time,
            end_time=end_time,
            notes="Good session"
        )
        
        self.assertEqual(session.duration_minutes, 90)
        self.assertTrue(session.is_completed())
    
    def test_learning_goal_target_date(self):
        """Test LearningGoal target date calculation"""
        future_date = datetime(2024, 12, 31)
        goal = LearningGoal(
            title="Complete Python Course",
            description="Finish all modules",
            target_date=future_date
        )
        
        days_until = goal.days_until_target()
        self.assertIsInstance(days_until, int)


class TestDatabaseManager(unittest.TestCase):
    """Test the database operations"""
    
    def setUp(self):
        """Set up test database"""
        # Create temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db = DatabaseManager(self.temp_db.name)
    
    def tearDown(self):
        """Clean up test database"""
        self.temp_db.close()
        os.unlink(self.temp_db.name)
    
    def test_add_and_get_course(self):
        """Test adding and retrieving courses"""
        course = Course(
            name="Test Course",
            description="A test course",
            duration_hours=10,
            difficulty_level=3,
            category="Test"
        )
        
        # Add course
        course_id = self.db.add_course(course)
        self.assertIsInstance(course_id, int)
        self.assertGreater(course_id, 0)
        
        # Retrieve course
        retrieved_course = self.db.get_course_by_id(course_id)
        self.assertIsNotNone(retrieved_course)
        self.assertEqual(retrieved_course.name, "Test Course")
        self.assertEqual(retrieved_course.difficulty_level, 3)
    
    def test_get_all_courses(self):
        """Test retrieving all courses"""
        # Add multiple courses
        course1 = Course(name="Course 1", description="First course")
        course2 = Course(name="Course 2", description="Second course")
        
        self.db.add_course(course1)
        self.db.add_course(course2)
        
        # Get all courses
        all_courses = self.db.get_all_courses()
        self.assertEqual(len(all_courses), 2)
        
        course_names = [course.name for course in all_courses]
        self.assertIn("Course 1", course_names)
        self.assertIn("Course 2", course_names)
    
    def test_add_study_session(self):
        """Test adding study sessions"""
        # First add a course
        course = Course(name="Test Course", description="Test")
        course_id = self.db.add_course(course)
        
        # Add study session
        session = StudySession(
            course_id=course_id,
            start_time=datetime.now(),
            notes="Test session"
        )
        
        session_id = self.db.add_study_session(session)
        self.assertIsInstance(session_id, int)
        self.assertGreater(session_id, 0)
    
    def test_get_sessions_for_course(self):
        """Test retrieving sessions for a course"""
        # Add course
        course = Course(name="Test Course", description="Test")
        course_id = self.db.add_course(course)
        
        # Add sessions
        session1 = StudySession(course_id=course_id, notes="Session 1")
        session2 = StudySession(course_id=course_id, notes="Session 2")
        
        self.db.add_study_session(session1)
        self.db.add_study_session(session2)
        
        # Get sessions
        sessions = self.db.get_sessions_for_course(course_id)
        self.assertEqual(len(sessions), 2)


class TestAnalytics(unittest.TestCase):
    """Test the analytics functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db = DatabaseManager(self.temp_db.name)
        
        # Add some test data
        course = Course(name="Test Course", description="Test", difficulty_level=2)
        self.course_id = self.db.add_course(course)
    
    def tearDown(self):
        """Clean up"""
        self.temp_db.close()
        os.unlink(self.temp_db.name)
    
    def test_course_completion_stats(self):
        """Test course completion statistics"""
        from src.analytics import ProgressAnalyzer
        analyzer = ProgressAnalyzer(self.db)
        
        stats = analyzer.get_course_completion_stats()
        
        self.assertIn('total_courses', stats)
        self.assertIn('completed_courses', stats)
        self.assertIn('in_progress', stats)
        self.assertIn('not_started', stats)
        
        self.assertEqual(stats['total_courses'], 1)
    
    def test_weekly_study_hours(self):
        """Test weekly study hours calculation"""
        from src.analytics import ProgressAnalyzer
        analyzer = ProgressAnalyzer(self.db)
        
        weekly_data = analyzer.get_weekly_study_hours(4)
        
        self.assertIsInstance(weekly_data, dict)
        self.assertEqual(len(weekly_data), 4)


if __name__ == '__main__':
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestModels))
    test_suite.addTest(unittest.makeSuite(TestDatabaseManager))
    test_suite.addTest(unittest.makeSuite(TestAnalytics))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    if result.wasSuccessful():
        print("\n🎉 All tests passed!")
    else:
        print(f"\n❌ {len(result.failures)} test(s) failed")
        print(f"❌ {len(result.errors)} error(s) occurred")