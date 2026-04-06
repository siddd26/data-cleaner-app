# Data Cleaner App

Production-ready Flask application for uploading, cleaning, previewing, and downloading CSV and Excel files.

## Overview

Data Cleaner provides a clean SaaS-style interface for uploading spreadsheets, applying basic cleaning steps, previewing results, and downloading the cleaned file in its original format.

## Features

- Modular Flask app package with `create_app()`
- SQLite database with `Flask-SQLAlchemy`
- Email/password authentication with hashed passwords
- Guest user support for free plan access
- Free and premium plans with file-size gating
- CSV and XLSX upload support
- Basic pandas cleaning:
  - remove duplicates
  - drop fully empty rows
  - fill text values with empty strings
  - fill numeric values with `0`
- First 10 cleaned rows preview
- Cleaned file download in the original file format
- Friendly error messages for invalid uploads and processing failures

## Tech Stack

- Python 3.9+
- Flask 3.x
- Flask-Login
- Flask-SQLAlchemy
- pandas + openpyxl
- SQLite

## Project Structure

- `run.py`: application entry point
- `config.py`: configuration and plan limits
- `app/__init__.py`: app factory and blueprint registration
- `app/extensions.py`: database and login manager setup
- `app/models/user.py`: user model
- `app/routes/main.py`: upload, preview, and download routes
- `app/routes/auth.py`: login, register, and logout routes
- `app/utils/cleaning.py`: pandas cleaning helpers
- `app/utils/file_handlers.py`: file validation, storage, loading, saving, and cleanup helpers
- `app/utils/user_utils.py`: guest-user and auth validation helpers

## Environment Variables

- `SECRET_KEY` (required in production): session and cookie signing key
- `FLASK_ENV`: `development` or `production` (defaults to `development`)
- `FLASK_DEBUG`: `true` or `false` (defaults to `false`)
- `SESSION_COOKIE_SECURE`: `true` to force secure cookies (defaults to `false`)
- `SESSION_COOKIE_SAMESITE`: `Lax` or `Strict` (defaults to `Lax`)

## Setup (Local)

1. Create a virtual environment:
   `python -m venv venv`
2. Activate it:
   Windows PowerShell: `.\venv\Scripts\Activate.ps1`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Run the app:
   `python run.py`
5. Open:
   `http://127.0.0.1:5050`

## Tests

1. Install dev dependencies:
   `pip install -r requirements-dev.txt`
2. Run tests:
   `pytest -q`

## Deployment Notes

- Use a production WSGI server such as Gunicorn (Linux/macOS) or Waitress (Windows).
- Set `SECRET_KEY` and `SESSION_COOKIE_SECURE=true` for production.
- Point the app at a production database if scaling beyond SQLite.

## Assumptions and Limitations

- SQLite is used by default for simplicity.
- Cleaning is intentionally minimal and designed for beginners.
- Temporary uploads are stored in `instance/temp_uploads` and cleaned automatically.
- File size limits are plan-based: free (5 MB), premium (50 MB).
