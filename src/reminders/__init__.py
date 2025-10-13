"""
Reminder and notification system

This module handles study reminders and notifications.
Intermediate level - introduces task scheduling and notification concepts.
"""

import schedule
import time
from datetime import datetime, timedelta
from typing import List, Callable, Optional
from ..models import LearningGoal
from ..storage import DatabaseManager


class ReminderSystem:
    """Manages study reminders and notifications"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.active_reminders = []
        self.notification_callback: Optional[Callable] = None
    
    def set_notification_callback(self, callback: Callable[[str], None]):
        """Set callback function for notifications"""
        self.notification_callback = callback
    
    def send_notification(self, message: str):
        """Send a notification message"""
        if self.notification_callback:
            self.notification_callback(message)
        else:
            # Default to console output
            print(f"📚 Study Reminder: {message}")
    
    def schedule_daily_reminder(self, time_str: str, message: str):
        """Schedule a daily reminder at specific time"""
        def reminder_job():
            self.send_notification(message)
        
        schedule.every().day.at(time_str).do(reminder_job)
        self.active_reminders.append(f"Daily reminder at {time_str}")
        return f"Daily reminder scheduled for {time_str}"
    
    def schedule_weekly_reminder(self, day: str, time_str: str, message: str):
        """Schedule a weekly reminder on specific day and time"""
        def reminder_job():
            self.send_notification(message)
        
        getattr(schedule.every(), day.lower()).at(time_str).do(reminder_job)
        self.active_reminders.append(f"Weekly reminder on {day} at {time_str}")
        return f"Weekly reminder scheduled for {day}s at {time_str}"
    
    def check_goal_deadlines(self):
        """Check for approaching learning goal deadlines"""
        # TODO: Implement goal deadline checking
        # This would query the database for goals with upcoming target dates
        goals_due_soon = []
        
        # Sample implementation
        upcoming_days = 7  # Check goals due in next 7 days
        cutoff_date = datetime.now() + timedelta(days=upcoming_days)
        
        # TODO: Query database for goals with target_date <= cutoff_date
        # For now, returning empty list
        
        for goal in goals_due_soon:
            days_left = goal.days_until_target()
            if days_left is not None and days_left <= 3:
                message = f"Goal '{goal.title}' is due in {days_left} days!"
                self.send_notification(message)
    
    def schedule_goal_deadline_checks(self):
        """Schedule regular checks for goal deadlines"""
        schedule.every().day.at("09:00").do(self.check_goal_deadlines)
        schedule.every().day.at("18:00").do(self.check_goal_deadlines)
    
    def create_study_streak_reminder(self):
        """Create reminder to maintain study streak"""
        def streak_reminder():
            message = "Don't break your study streak! Time for today's session."
            self.send_notification(message)
        
        # Remind in the evening if no study session today
        schedule.every().day.at("19:00").do(streak_reminder)
    
    def get_active_reminders(self) -> List[str]:
        """Get list of all active reminders"""
        return self.active_reminders.copy()
    
    def clear_all_reminders(self):
        """Clear all scheduled reminders"""
        schedule.clear()
        self.active_reminders.clear()
        return "All reminders cleared"
    
    def run_scheduler(self, run_once: bool = False):
        """Run the reminder scheduler"""
        if run_once:
            schedule.run_pending()
        else:
            # Run continuously
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute


class StudySessionReminder:
    """Specific reminders for study sessions"""
    
    def __init__(self, reminder_system: ReminderSystem):
        self.reminder_system = reminder_system
    
    def set_daily_study_time(self, time_str: str, duration_minutes: int = 30):
        """Set a daily study reminder"""
        message = f"Time for your {duration_minutes}-minute study session!"
        return self.reminder_system.schedule_daily_reminder(time_str, message)
    
    def set_course_specific_reminder(self, course_name: str, schedule_time: str):
        """Set reminder for specific course study"""
        message = f"Time to study {course_name}!"
        return self.reminder_system.schedule_daily_reminder(schedule_time, message)
    
    def set_break_reminder(self, interval_minutes: int = 25):
        """Set Pomodoro-style break reminders"""
        # This would be more complex to implement with the schedule library
        # For now, just showing the concept
        message = f"Take a {interval_minutes}-minute break!"
        # TODO: Implement interval-based reminders
        return f"Break reminder set for every {interval_minutes} minutes"


class MotivationalNotifications:
    """Sends motivational messages and achievements"""
    
    def __init__(self, reminder_system: ReminderSystem):
        self.reminder_system = reminder_system
        self.motivational_messages = [
            "You're doing great! Keep up the excellent work! 🌟",
            "Every expert was once a beginner. Keep learning! 📚",
            "Progress, not perfection. You've got this! 💪",
            "Knowledge is power. You're building yours every day! 🧠",
            "Small steps daily lead to big results yearly! 🎯"
        ]
    
    def send_random_motivation(self):
        """Send a random motivational message"""
        import random
        message = random.choice(self.motivational_messages)
        self.reminder_system.send_notification(message)
    
    def celebrate_milestone(self, milestone: str):
        """Send celebration message for achievements"""
        message = f"🎉 Congratulations! You've achieved: {milestone}"
        self.reminder_system.send_notification(message)
    
    def schedule_weekly_motivation(self):
        """Schedule weekly motivational messages"""
        self.reminder_system.schedule_weekly_reminder(
            "monday", "08:00", 
            "New week, new opportunities to learn! Let's make it count! 🚀"
        )