from flask import Blueprint, render_template

from app.utils.user_utils import get_current_user


main_bp = Blueprint("main", __name__)


# This function renders the homepage and exposes the current effective user.
# Input: no direct inputs
# Output: rendered HTML response
@main_bp.route("/")
def index():
    current_app_user = get_current_user()
    return render_template("index.html", current_app_user=current_app_user)
