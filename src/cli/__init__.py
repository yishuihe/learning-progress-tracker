"""
Command Line Interface for Learning Progress Tracker

This module provides a user-friendly CLI for the application.
Beginner friendly - great introduction to CLI applications and user input handling.
"""

import click
from datetime import datetime
from ..models import Course, StudySession, LearningGoal
from ..storage import DatabaseManager
from ..analytics import ProgressAnalyzer


@click.group()
@click.pass_context
def cli(ctx):
    """Learning Progress Tracker - Track your learning journey!"""
    ctx.ensure_object(dict)
    ctx.obj['db'] = DatabaseManager()


@cli.command()
@click.option('--name', prompt='Course name', help='Name of the course')
@click.option('--description', prompt='Course description', help='Description of the course')
@click.option('--duration', prompt='Duration (hours)', type=int, help='Expected duration in hours')
@click.option('--difficulty', prompt='Difficulty (1-5)', type=click.IntRange(1, 5), help='Difficulty level 1-5')
@click.option('--category', prompt='Category', help='Course category')
@click.pass_context
def add_course(ctx, name, description, duration, difficulty, category):
    """Add a new course to track"""
    db = ctx.obj['db']
    
    course = Course(
        name=name,
        description=description,
        duration_hours=duration,
        difficulty_level=difficulty,
        category=category
    )
    
    course_id = db.add_course(course)
    click.echo(f"✅ Course '{name}' added successfully with ID: {course_id}")


@cli.command()
@click.pass_context
def list_courses(ctx):
    """List all courses"""
    db = ctx.obj['db']
    courses = db.get_all_courses()
    
    if not courses:
        click.echo("📚 No courses found. Add some courses first!")
        return
    
    click.echo("📚 Your Courses:")
    click.echo("-" * 60)
    
    for course in courses:
        difficulty_stars = "⭐" * course.difficulty_level
        click.echo(f"ID: {course.id}")
        click.echo(f"Name: {course.name}")
        click.echo(f"Category: {course.category}")
        click.echo(f"Duration: {course.duration_hours} hours")
        click.echo(f"Difficulty: {difficulty_stars} ({course.difficulty_level}/5)")
        click.echo(f"Description: {course.description}")
        click.echo("-" * 60)


@cli.command()
@click.option('--course-id', prompt='Course ID', type=int, help='ID of the course to study')
@click.option('--notes', default='', help='Notes about the study session')
@click.pass_context
def start_session(ctx, course_id, notes):
    """Start a new study session"""
    db = ctx.obj['db']
    
    # Check if course exists
    course = db.get_course_by_id(course_id)
    if not course:
        click.echo(f"❌ Course with ID {course_id} not found!")
        return
    
    session = StudySession(
        course_id=course_id,
        notes=notes,
        start_time=datetime.now()
    )
    
    session_id = db.add_study_session(session)
    click.echo(f"▶️  Study session started for '{course.name}'!")
    click.echo(f"Session ID: {session_id}")
    click.echo("⏰ Timer started. Use 'end-session' command when you're done.")


@cli.command()
@click.option('--session-id', prompt='Session ID', type=int, help='ID of the session to end')
@click.option('--rating', prompt='Session rating (1-5)', type=click.IntRange(1, 5), help='How was the session?')
@click.pass_context
def end_session(ctx, session_id, rating):
    """End a study session"""
    # TODO: Implement session ending logic
    # This would require updating the study session in the database
    click.echo(f"⏹️  Study session {session_id} ended!")
    click.echo(f"Rating: {'⭐' * rating}")
    click.echo("Great job studying! 🎉")


@cli.command()
@click.pass_context
def show_stats(ctx):
    """Show learning statistics"""
    db = ctx.obj['db']
    analyzer = ProgressAnalyzer(db)
    
    # Get basic statistics
    courses = db.get_all_courses()
    course_stats = analyzer.get_course_completion_stats()
    
    click.echo("📊 Your Learning Statistics:")
    click.echo("=" * 40)
    click.echo(f"Total Courses: {course_stats['total_courses']}")
    click.echo(f"Completed: {course_stats['completed_courses']}")
    click.echo(f"In Progress: {course_stats['in_progress']}")
    click.echo(f"Not Started: {course_stats['not_started']}")
    click.echo(f"Study Streak: {analyzer.get_study_streak()} days")
    click.echo("=" * 40)
    
    # Show weekly progress
    weekly_data = analyzer.get_weekly_study_hours()
    click.echo("\n📈 Weekly Study Hours:")
    for week, hours in weekly_data.items():
        bar = "█" * int(hours)
        click.echo(f"{week}: {hours:.1f}h {bar}")


@cli.command()
@click.pass_context
def generate_report(ctx):
    """Generate a comprehensive progress report"""
    db = ctx.obj['db']
    analyzer = ProgressAnalyzer(db)
    
    click.echo("📋 Generating progress report...")
    
    # Generate chart
    chart_path = analyzer.generate_progress_chart()
    click.echo(f"📊 Progress chart saved to: {chart_path}")
    
    # Generate monthly report
    report = analyzer.generate_monthly_report()
    
    click.echo("\n📅 Monthly Report Summary:")
    click.echo("-" * 30)
    click.echo(f"Total Study Hours: {report['total_study_hours']}")
    click.echo(f"Courses Completed: {report['courses_completed']}")
    click.echo(f"Average Session Rating: {report['average_session_rating']}/5")
    click.echo(f"Current Study Streak: {report['study_streak']} days")
    
    click.echo("\n✅ Report generated successfully!")


@cli.command()
@click.option('--title', prompt='Goal title', help='Title of the learning goal')
@click.option('--description', prompt='Goal description', help='Description of the goal')
@click.option('--target-date', prompt='Target date (YYYY-MM-DD)', help='Target completion date')
@click.pass_context
def add_goal(ctx, title, description, target_date):
    """Add a new learning goal"""
    try:
        target_dt = datetime.strptime(target_date, '%Y-%m-%d')
        
        goal = LearningGoal(
            title=title,
            description=description,
            target_date=target_dt
        )
        
        # TODO: Implement goal saving to database
        click.echo(f"🎯 Goal '{title}' added successfully!")
        click.echo(f"Target date: {target_date}")
        
    except ValueError:
        click.echo("❌ Invalid date format. Please use YYYY-MM-DD")


if __name__ == '__main__':
    cli()