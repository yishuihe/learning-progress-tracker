"""
Main entry point for the web application

This file allows running the web app directly with:
python -m src.web_app

Perfect starting point for understanding Flask applications.
"""

from . import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)