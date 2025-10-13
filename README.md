# Learning Progress Tracker

A collaborative Python project for tracking learning progress, courses, and analytics.

## 🎯 Project Overview

The Learning Progress Tracker is designed to help learners monitor their educational journey through:
- Course tracking and management
- Study session logging
- Progress analytics and visualizations
- Study reminders and goal setting
- Web-based dashboard and CLI interface

## 🏗️ Project Structure

```
learning_tracker/
├── src/
│   ├── models/           # Data models (Beginner friendly)
│   ├── storage/          # Data persistence (Beginner friendly)
│   ├── analytics/        # Progress analysis (Intermediate)
│   ├── reminders/        # Notification system (Intermediate)
│   ├── web_app/          # Flask web interface (Advanced)
│   └── cli/              # Command line interface (Beginner friendly)
├── tests/                # Test suite
├── docs/                 # Documentation
├── data/                 # Sample data and database
└── requirements.txt      # Python dependencies
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip package manager

### Installation
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Unix)
4. Install dependencies: `pip install -r requirements.txt`

### Running the Application
- Web interface: `python -m src.web_app.app`
- CLI interface: `python -m src.cli.main`

## 👥 Team Collaboration

### Task Difficulty Levels
- **Beginner**: Data models, basic CRUD operations, CLI interface
- **Intermediate**: Analytics, reminders, data visualization
- **Advanced**: Web framework, database design, deployment

### Git Workflow
1. Create feature branch: `git checkout -b feature/your-feature-name`
2. Make changes and commit
3. Push branch and create pull request
4. Code review and merge

## 🛠️ Technologies Used
- **Backend**: Python, Flask
- **Database**: SQLite
- **Data Visualization**: Matplotlib, Plotly
- **Task Scheduling**: Schedule library
- **Testing**: pytest
- **CLI**: Click library

## 📖 Documentation
See the `docs/` folder for detailed documentation including:
- API documentation
- Database schema
- Contribution guidelines
- Development setup

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.