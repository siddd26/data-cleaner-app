import os


class Config:
    ENVIRONMENT = os.environ.get("FLASK_ENV", "development")
    SECRET_KEY = os.environ.get("SECRET_KEY") or (
        "dev-secret-key" if ENVIRONMENT == "development" else None
    )
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
    TEMP_UPLOAD_FOLDER = os.path.join(INSTANCE_DIR, "temp_uploads")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(INSTANCE_DIR, 'data_cleaner.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = os.environ.get("SESSION_COOKIE_SAMESITE", "Lax")
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "false").lower() == "true"
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    FREE_PLAN_SIZE_LIMIT = 5 * 1024 * 1024
    PREMIUM_PLAN_SIZE_LIMIT = 50 * 1024 * 1024
    TEMP_FILE_MAX_AGE_SECONDS = 60 * 60
    ALLOWED_EXTENSIONS = {"csv", "xlsx"}
