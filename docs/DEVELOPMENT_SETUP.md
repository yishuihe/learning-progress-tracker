# Development Setup Guide

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** (3.9+ recommended)
- **Git** for version control
- **Code editor** (VS Code recommended)
- **Terminal/Command Prompt**

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yishuihe/learning-progress-tracker.git
   cd learning-progress-tracker
   ```

2. **Create Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Installation**
   ```bash
   # Test CLI
   python -m src.cli.main --help
   
   # Test Web App
   python -m src.web_app.main
   ```

## 🔧 Development Environment Setup

### VS Code Configuration

1. **Install Recommended Extensions**
   - Python (ms-python.python)
   - Python Debugger (ms-python.debugpy)
   - GitLens (eamodio.gitlens)
   - Thunder Client (rangav.vscode-thunder-client) - for API testing

2. **VS Code Settings**
   Create `.vscode/settings.json`:
   ```json
   {
     "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
     "python.linting.enabled": true,
     "python.linting.pylintEnabled": true,
     "python.formatting.provider": "black",
     "python.testing.pytestEnabled": true,
     "python.testing.pytestArgs": ["tests"],
     "files.exclude": {
       "**/__pycache__": true,
       "**/venv": true,
       "**/*.pyc": true
     }
   }
   ```

3. **Launch Configuration**
   Create `.vscode/launch.json`:
   ```json
   {
     "version": "0.2.0",
     "configurations": [
       {
         "name": "Flask Web App",
         "type": "python",
         "request": "launch",
         "program": "${workspaceFolder}/src/web_app/main.py",
         "console": "integratedTerminal",
         "env": {
           "FLASK_ENV": "development",
           "FLASK_DEBUG": "1"
         }
       },
       {
         "name": "CLI Application",
         "type": "python",
         "request": "launch",
         "module": "src.cli.main",
         "args": ["--help"],
         "console": "integratedTerminal"
       },
       {
         "name": "Run Tests",
         "type": "python",
         "request": "launch",
         "module": "pytest",
         "args": ["tests/"],
         "console": "integratedTerminal"
       }
     ]
   }
   ```

### Database Setup

1. **Initialize Database**
   ```bash
   python -c "from src.storage import DatabaseManager; dm = DatabaseManager(); print('Database initialized!')"
   ```

2. **Load Sample Data (Optional)**
   ```bash
   python -c "
   from src.storage import DatabaseManager
   from src.models import Course
   from datetime import datetime
   
   db = DatabaseManager()
   sample_course = Course(
       name='Sample Course',
       description='A sample course for testing', 
       duration_hours=10,
       difficulty_level=2,
       category='Sample'
   )
   course_id = db.add_course(sample_course)
   print(f'Sample course added with ID: {course_id}')
   "
   ```

### Environment Variables

Create a `.env` file in the project root:
```bash
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-development-secret-key

# Database Configuration
DATABASE_URL=sqlite:///data/learning_tracker.db
TEST_DATABASE_URL=sqlite:///data/test_learning_tracker.db

# Logging
LOG_LEVEL=DEBUG
LOG_FILE=logs/app.log

# Development Settings
DEVELOPMENT_MODE=1
```

## 🛠️ Development Workflow

### Branch Strategy
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Work on your changes...

# Commit changes
git add .
git commit -m "Add: descriptive commit message"

# Push branch
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

### Code Style Guidelines

1. **Python Style**
   - Follow PEP 8
   - Use type hints
   - Maximum line length: 88 characters
   - Use docstrings for all functions and classes

2. **Import Organization**
   ```python
   # Standard library imports
   import os
   from datetime import datetime
   
   # Third-party imports
   import click
   from flask import Flask
   
   # Local imports
   from .models import Course
   from .storage import DatabaseManager
   ```

3. **Naming Conventions**
   ```python
   # Variables and functions: snake_case
   course_name = "Python Basics"
   def get_course_by_id(course_id: int) -> Course:
   
   # Classes: PascalCase
   class CourseManager:
   
   # Constants: UPPER_SNAKE_CASE
   MAX_COURSE_DURATION = 100
   ```

### Testing Strategy

1. **Run All Tests**
   ```bash
   python -m pytest tests/ -v
   ```

2. **Run Specific Test Categories**
   ```bash
   # Unit tests only
   python -m pytest tests/test_models.py -v
   
   # Integration tests
   python -m pytest tests/test_database.py -v
   
   # With coverage
   python -m pytest tests/ --cov=src --cov-report=html
   ```

3. **Test Structure**
   ```
   tests/
   ├── test_models.py          # Model unit tests
   ├── test_storage.py         # Database tests
   ├── test_analytics.py       # Analytics tests
   ├── test_web_app.py         # Flask app tests
   ├── test_cli.py             # CLI tests
   └── conftest.py             # Test configuration
   ```

### Debugging

1. **Flask Debug Mode**
   ```bash
   export FLASK_DEBUG=1
   python -m src.web_app.main
   ```

2. **Python Debugger**
   ```python
   import pdb; pdb.set_trace()  # Add breakpoint
   ```

3. **Logging Setup**
   ```python
   import logging
   
   logging.basicConfig(
       level=logging.DEBUG,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   )
   
   logger = logging.getLogger(__name__)
   logger.debug("Debug message")
   ```

## 🔍 Code Quality Tools

### Pre-commit Hooks

1. **Install pre-commit**
   ```bash
   pip install pre-commit
   ```

2. **Create `.pre-commit-config.yaml`**
   ```yaml
   repos:
   - repo: https://github.com/psf/black
     rev: 23.1.0
     hooks:
     - id: black
       language_version: python3
   
   - repo: https://github.com/pycqa/flake8
     rev: 6.0.0
     hooks:
     - id: flake8
   
   - repo: https://github.com/pycqa/isort
     rev: 5.12.0
     hooks:
     - id: isort
   ```

3. **Install hooks**
   ```bash
   pre-commit install
   ```

### Code Formatting

1. **Black (Code Formatter)**
   ```bash
   pip install black
   black src/ tests/
   ```

2. **isort (Import Sorting)**
   ```bash
   pip install isort
   isort src/ tests/
   ```

3. **flake8 (Linting)**
   ```bash
   pip install flake8
   flake8 src/ tests/
   ```

## 📊 Performance Monitoring

### Profiling

1. **cProfile for Performance**
   ```bash
   python -m cProfile -o profile_output.prof -m src.web_app.main
   ```

2. **Memory Profiling**
   ```bash
   pip install memory-profiler
   python -m memory_profiler src/analytics/__init__.py
   ```

### Database Performance

1. **SQLite Analysis**
   ```sql
   -- Enable query planning
   PRAGMA query_only = ON;
   EXPLAIN QUERY PLAN SELECT * FROM courses WHERE difficulty_level = 3;
   ```

2. **Database Optimization**
   ```python
   # Use connection pooling
   from src.storage import DatabaseManager
   
   db = DatabaseManager()
   with db.get_connection() as conn:
       # Batch operations
       conn.executemany("INSERT INTO courses ...", course_data)
   ```

## 🚀 Deployment Preparation

### Environment-Specific Configurations

1. **Development**
   ```python
   DEBUG = True
   DATABASE_URL = "sqlite:///data/dev_learning_tracker.db"
   LOG_LEVEL = "DEBUG"
   ```

2. **Testing**
   ```python
   TESTING = True
   DATABASE_URL = "sqlite:///data/test_learning_tracker.db"
   WTF_CSRF_ENABLED = False
   ```

3. **Production**
   ```python
   DEBUG = False
   DATABASE_URL = os.environ.get('DATABASE_URL')
   SECRET_KEY = os.environ.get('SECRET_KEY')
   LOG_LEVEL = "INFO"
   ```

### Docker Setup (Optional)

1. **Dockerfile**
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 5000
   CMD ["python", "-m", "src.web_app.main"]
   ```

2. **docker-compose.yml**
   ```yaml
   version: '3.8'
   services:
     web:
       build: .
       ports:
         - "5000:5000"
       volumes:
         - ./data:/app/data
       environment:
         - FLASK_ENV=development
   ```

## 🔧 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure you're in the project root
   cd learning-progress-tracker
   
   # Activate virtual environment
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Database Issues**
   ```bash
   # Delete and recreate database
   rm data/learning_tracker.db
   python -c "from src.storage import DatabaseManager; DatabaseManager()"
   ```

3. **Port Already in Use**
   ```bash
   # Find process using port 5000
   lsof -i :5000  # macOS/Linux
   netstat -ano | findstr :5000  # Windows
   
   # Kill process or use different port
   python -m src.web_app.main --port=5001
   ```

### Getting Help

1. **Check Documentation**
   - API Documentation: `docs/API.md`
   - Database Schema: `docs/DATABASE_SCHEMA.md`
   - Contributing Guidelines: `docs/CONTRIBUTING.md`

2. **GitHub Issues**
   - Search existing issues
   - Create new issue with:
     - Clear description
     - Steps to reproduce
     - Expected vs actual behavior
     - Environment details

3. **Community Support**
   - Join project discussions
   - Ask questions in pull requests
   - Help other contributors

## 📈 Development Metrics

### Code Coverage
```bash
# Generate coverage report
python -m pytest tests/ --cov=src --cov-report=html --cov-report=term

# View coverage report
open htmlcov/index.html
```

### Performance Benchmarks
```bash
# Basic performance test
python -m timeit -n 1000 "from src.models import Course; Course(name='test')"

# Database performance
python scripts/benchmark_database.py
```

### Code Quality Metrics
```bash
# Complexity analysis
pip install radon
radon cc src/ -a

# Maintainability index
radon mi src/
```

Remember: The goal is to create a learning environment where everyone can contribute meaningfully while growing their Python skills! 🎓