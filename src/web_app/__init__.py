"""
Flask web application for Learning Progress Tracker

This module provides a web interface for the application.
Advanced level - introduces web development concepts with Flask.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import os
from ..models import Course, StudySession, LearningGoal
from ..storage import DatabaseManager
from ..analytics import ProgressAnalyzer
from ..reminders import ReminderSystem

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Initialize database
db = DatabaseManager()
analyzer = ProgressAnalyzer(db)
reminder_system = ReminderSystem(db)


@app.route('/')
def index():
    """Home page - Dashboard"""
    courses = db.get_all_courses()
    course_stats = analyzer.get_course_completion_stats()
    weekly_data = analyzer.get_weekly_study_hours()
    
    return render_template('dashboard.html', 
                         courses=courses,
                         stats=course_stats,
                         weekly_data=weekly_data)


@app.route('/courses')
def courses():
    """Courses page - List all courses"""
    all_courses = db.get_all_courses()
    return render_template('courses.html', courses=all_courses)


@app.route('/courses/add', methods=['GET', 'POST'])
def add_course():
    """Add new course page"""
    if request.method == 'POST':
        course = Course(
            name=request.form['name'],
            description=request.form['description'],
            duration_hours=int(request.form['duration_hours']),
            difficulty_level=int(request.form['difficulty_level']),
            category=request.form['category']
        )
        
        course_id = db.add_course(course)
        flash(f'Course "{course.name}" added successfully!', 'success')
        return redirect(url_for('courses'))
    
    return render_template('add_course.html')


@app.route('/courses/<int:course_id>')
def course_detail(course_id):
    """Course detail page"""
    course = db.get_course_by_id(course_id)
    if not course:
        flash('Course not found!', 'error')
        return redirect(url_for('courses'))
    
    sessions = db.get_sessions_for_course(course_id)
    return render_template('course_detail.html', course=course, sessions=sessions)


@app.route('/sessions/start/<int:course_id>', methods=['POST'])
def start_session(course_id):
    """Start a new study session"""
    course = db.get_course_by_id(course_id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    session = StudySession(
        course_id=course_id,
        notes=request.form.get('notes', ''),
        start_time=datetime.now()
    )
    
    session_id = db.add_study_session(session)
    flash(f'Study session started for "{course.name}"!', 'success')
    return redirect(url_for('course_detail', course_id=course_id))


@app.route('/analytics')
def analytics():
    """Analytics page"""
    weekly_data = analyzer.get_weekly_study_hours()
    course_stats = analyzer.get_course_completion_stats()
    difficulty_dist = analyzer.generate_course_difficulty_distribution()
    monthly_report = analyzer.generate_monthly_report()
    
    return render_template('analytics.html',
                         weekly_data=weekly_data,
                         course_stats=course_stats,
                         difficulty_dist=difficulty_dist,
                         monthly_report=monthly_report)


@app.route('/goals')
def goals():
    """Learning goals page"""
    # TODO: Implement goals retrieval from database
    goals = []  # Placeholder
    return render_template('goals.html', goals=goals)


@app.route('/goals/add', methods=['GET', 'POST'])
def add_goal():
    """Add new learning goal"""
    if request.method == 'POST':
        goal = LearningGoal(
            title=request.form['title'],
            description=request.form['description'],
            target_date=datetime.strptime(request.form['target_date'], '%Y-%m-%d')
        )
        
        # TODO: Implement goal saving to database
        flash(f'Goal "{goal.title}" added successfully!', 'success')
        return redirect(url_for('goals'))
    
    return render_template('add_goal.html')


@app.route('/reminders')
def reminders():
    """Reminders management page"""
    active_reminders = reminder_system.get_active_reminders()
    return render_template('reminders.html', reminders=active_reminders)


@app.route('/api/chart-data')
def chart_data():
    """API endpoint for chart data"""
    weekly_data = analyzer.get_weekly_study_hours()
    return jsonify(weekly_data)


@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics"""
    stats = {
        'course_stats': analyzer.get_course_completion_stats(),
        'study_streak': analyzer.get_study_streak(),
        'weekly_hours': list(analyzer.get_weekly_study_hours().values())
    }
    return jsonify(stats)


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


# Template folder setup
def setup_templates():
    """Create templates directory and basic HTML files"""
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    # This would create basic HTML templates
    # For now, just ensuring the directory exists


if __name__ == '__main__':
    setup_templates()
    app.run(debug=True, host='0.0.0.0', port=5000)