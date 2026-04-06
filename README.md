# Data Cleaner App

Starter Flask project for uploading, cleaning, previewing, and downloading CSV and Excel files.

## Features

- Modular Flask app package with `create_app()`
- SQLite database with `Flask-SQLAlchemy`
- Email/password authentication with hashed passwords
- Guest user support through `get_current_user()`
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

## Project Structure

- `run.py`: application entry point
- `config.py`: app configuration and plan limits
- `app/__init__.py`: app factory and blueprint registration
- `app/extensions.py`: database and login manager setup
- `app/models/user.py`: user model
- `app/routes/main.py`: upload, preview, and download routes
- `app/routes/auth.py`: login, register, and logout routes
- `app/utils/cleaning.py`: pandas cleaning helpers
- `app/utils/file_handlers.py`: file validation, storage, loading, saving, and cleanup helpers
- `app/utils/user_utils.py`: guest-user and auth validation helpers

## Setup

1. Create a virtual environment:
   `python -m venv venv`
2. Activate it:
   Windows PowerShell: `.\venv\Scripts\Activate.ps1`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Run the app:
   `python run.py`
5. Open:
   `http://127.0.0.1:5000`

## Default Rules

- Free plan upload limit: 5 MB
- Premium plan upload limit: 50 MB
- Temporary files are stored in `instance/temp_uploads`
- Old temporary files are cleaned automatically

## Starter Test Checklist

- Register a new user
- Log in with the created account
- Upload a valid `.csv` file
- Upload a valid `.xlsx` file
- Verify preview shows the first 10 cleaned rows
- Download the cleaned file
- Try an invalid file type like `.txt`
- Try an empty file upload
- Try a file larger than the plan limit
