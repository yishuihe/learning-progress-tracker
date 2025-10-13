"""
Analytics and visualization module

This module provides data analysis and visualization capabilities.
Intermediate level - great for learning matplotlib and data analysis concepts.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import List, Dict, Tuple
from datetime import datetime, timedelta
from ..models import Course, StudySession
from ..storage import DatabaseManager


class ProgressAnalyzer:
    """Analyzes learning progress and generates insights"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def get_weekly_study_hours(self, weeks: int = 4) -> Dict[str, float]:
        """Get study hours for the past N weeks"""
        end_date = datetime.now()
        start_date = end_date - timedelta(weeks=weeks)
        
        # This would need to be implemented with proper database queries
        # For now, returning sample data for demonstration
        weekly_data = {}
        for i in range(weeks):
            week_start = start_date + timedelta(weeks=i)
            week_label = week_start.strftime("Week of %b %d")
            # TODO: Calculate actual study hours from database
            weekly_data[week_label] = 5.5 + (i * 0.5)  # Sample data
        
        return weekly_data
    
    def get_course_completion_stats(self) -> Dict[str, int]:
        """Get statistics about course completion"""
        courses = self.db.get_all_courses()
        
        stats = {
            "total_courses": len(courses),
            "completed_courses": 0,  # TODO: Implement completion logic
            "in_progress": 0,
            "not_started": 0
        }
        
        # TODO: Implement actual completion checking logic
        stats["in_progress"] = len(courses)
        
        return stats
    
    def generate_progress_chart(self, save_path: str = "data/progress_chart.png"):
        """Generate a progress visualization chart"""
        weekly_data = self.get_weekly_study_hours()
        
        # Create the plot
        plt.figure(figsize=(10, 6))
        weeks = list(weekly_data.keys())
        hours = list(weekly_data.values())
        
        plt.plot(weeks, hours, marker='o', linewidth=2, markersize=8)
        plt.title("Weekly Study Progress", fontsize=16, fontweight='bold')
        plt.xlabel("Week", fontsize=12)
        plt.ylabel("Study Hours", fontsize=12)
        plt.grid(True, alpha=0.3)
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save the chart
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    def generate_course_difficulty_distribution(self) -> Dict[str, int]:
        """Analyze distribution of course difficulties"""
        courses = self.db.get_all_courses()
        
        difficulty_dist = {
            "Beginner (1-2)": 0,
            "Intermediate (3)": 0, 
            "Advanced (4-5)": 0
        }
        
        for course in courses:
            if course.difficulty_level <= 2:
                difficulty_dist["Beginner (1-2)"] += 1
            elif course.difficulty_level == 3:
                difficulty_dist["Intermediate (3)"] += 1
            else:
                difficulty_dist["Advanced (4-5)"] += 1
        
        return difficulty_dist
    
    def get_study_streak(self) -> int:
        """Calculate current study streak in days"""
        # TODO: Implement streak calculation based on study sessions
        # This would require querying study sessions and checking consecutive days
        return 5  # Sample data
    
    def generate_monthly_report(self) -> Dict:
        """Generate a comprehensive monthly progress report"""
        report = {
            "total_study_hours": 45.5,  # TODO: Calculate from database
            "courses_completed": 2,      # TODO: Calculate from database
            "average_session_rating": 4.2,  # TODO: Calculate from database
            "study_streak": self.get_study_streak(),
            "weekly_progress": self.get_weekly_study_hours(),
            "course_difficulty_distribution": self.generate_course_difficulty_distribution(),
            "generated_date": datetime.now().isoformat()
        }
        
        return report


class VisualizationHelper:
    """Helper class for creating various types of visualizations"""
    
    @staticmethod
    def create_pie_chart(data: Dict[str, int], title: str, save_path: str):
        """Create a pie chart from data dictionary"""
        plt.figure(figsize=(8, 8))
        labels = list(data.keys())
        values = list(data.values())
        
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title(title, fontsize=16, fontweight='bold')
        plt.axis('equal')
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    @staticmethod
    def create_bar_chart(data: Dict[str, float], title: str, xlabel: str, ylabel: str, save_path: str):
        """Create a bar chart from data dictionary"""
        plt.figure(figsize=(10, 6))
        categories = list(data.keys())
        values = list(data.values())
        
        plt.bar(categories, values)
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path