from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    plan = db.Column(db.String(20), nullable=False, default="free")

    # This function hashes and stores a plain-text password for the user.
    # Input: plain-text password string
    # Output: none
    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    # This function checks whether a plain-text password matches the stored hash.
    # Input: plain-text password string
    # Output: boolean indicating whether the password is valid
    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)


# This function loads a user by ID for Flask-Login session management.
# Input: user ID string from the session
# Output: User object or None
@login_manager.user_loader
def load_user(user_id):
    if not user_id:
        return None

    return User.query.get(int(user_id))
