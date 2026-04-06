from pathlib import Path

import pytest

from app import create_app
from app.extensions import db
from config import Config


# This function builds a test-specific Flask configuration class.
# Input: temporary pytest path object
# Output: Config subclass for tests
def build_test_config(tmp_path):
    class TestConfig(Config):
        TESTING = True
        SECRET_KEY = "test-secret-key"
        INSTANCE_DIR = str(tmp_path / "instance")
        TEMP_UPLOAD_FOLDER = str(Path(INSTANCE_DIR) / "temp_uploads")
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{tmp_path / 'test_app.db'}"

    return TestConfig


# This function creates a Flask app fixture backed by temporary test storage.
# Input: pytest temporary path fixture
# Output: configured Flask application for tests
@pytest.fixture
def app(tmp_path):
    test_config = build_test_config(tmp_path)
    application = create_app(test_config)

    with application.app_context():
        db.drop_all()
        db.create_all()

    yield application

    with application.app_context():
        db.session.remove()
        db.drop_all()


# This function creates a Flask test client fixture.
# Input: Flask app fixture
# Output: Flask test client
@pytest.fixture
def client(app):
    return app.test_client()
