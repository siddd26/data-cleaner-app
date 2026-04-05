from dataclasses import dataclass

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
