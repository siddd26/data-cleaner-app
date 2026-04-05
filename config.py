import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
    TEMP_UPLOAD_FOLDER = os.path.join(INSTANCE_DIR, "temp_uploads")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(INSTANCE_DIR, 'data_cleaner.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    FREE_PLAN_SIZE_LIMIT = 5 * 1024 * 1024
    PREMIUM_PLAN_SIZE_LIMIT = 50 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"csv", "xlsx"}
