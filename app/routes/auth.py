from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.extensions import db
from app.models.user import User
from app.utils.user_utils import is_valid_email, is_valid_password


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# This function displays the login page and logs in a user when valid credentials are submitted.
# Input: HTTP GET or POST request with email and password form fields
# Output: rendered login page or redirect response
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form_email = ""

    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        form_email = email

        if not email or not password:
            flash("Email and password are required.", "danger")
            return render_template("login.html", form_email=form_email)

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("main.index"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html", form_email=form_email)


# This function displays the registration page and creates a new free-plan user account.
# Input: HTTP GET or POST request with email and password form fields
# Output: rendered register page or redirect response
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form_email = ""

    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        form_email = email

        if not email or not password:
            flash("Email and password are required.", "danger")
            return render_template("register.html", form_email=form_email)

        if not is_valid_email(email):
            flash("Please enter a valid email address.", "danger")
            return render_template("register.html", form_email=form_email)

        if not is_valid_password(password):
            flash("Password must be at least 6 characters long.", "danger")
            return render_template("register.html", form_email=form_email)

        if password != confirm_password:
            flash("Password and confirm password must match.", "danger")
            return render_template("register.html", form_email=form_email)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("An account with that email already exists.", "danger")
            return render_template("register.html", form_email=form_email)

        user = User(email=email, plan="free")
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form_email=form_email)


# This function logs out the currently authenticated user.
# Input: authenticated user session
# Output: redirect response
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("main.index"))
