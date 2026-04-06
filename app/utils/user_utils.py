from dataclasses import dataclass
import re

from flask import current_app
from flask_login import current_user


@dataclass
class GuestUser:
    id: str = "guest"
    email: str = "guest@example.com"
    plan: str = "free"
    is_authenticated: bool = False


# This function returns the currently active user or a guest user fallback.
# Input: no direct inputs
# Output: authenticated User object or GuestUser instance
def get_current_user():
    if current_user.is_authenticated:
        return current_user

    return GuestUser()


# This function returns the maximum allowed file size for the given user plan.
# Input: user object with a plan attribute
# Output: integer file size limit in bytes
def get_plan_file_size_limit(user):
    if getattr(user, "plan", "free") == "premium":
        return current_app.config["PREMIUM_PLAN_SIZE_LIMIT"]

    return current_app.config["FREE_PLAN_SIZE_LIMIT"]


# This function checks whether an email address uses a simple valid format.
# Input: email string
# Output: boolean indicating whether the email format is valid
def is_valid_email(email):
    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(email_pattern, email))


# This function checks whether a password meets the minimum starter app rules.
# Input: password string
# Output: boolean indicating whether the password is valid
def is_valid_password(password):
    return len(password) >= 6
