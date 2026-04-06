from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)

from app.utils.cleaning import clean_dataframe, create_preview_rows
from app.utils.cleaning import calculate_cleaning_summary
from app.utils.file_handlers import (
    allowed_file,
    cleanup_expired_temp_files,
    cleanup_temp_file,
    format_size_limit,
    get_uploaded_file_size,
    load_dataframe_from_file,
    save_cleaned_dataframe,
    save_uploaded_file,
)
from app.utils.user_utils import get_current_user, get_plan_file_size_limit


main_bp = Blueprint("main", __name__)


# This function renders the homepage and exposes the current effective user.
# Input: no direct inputs
# Output: rendered HTML response
@main_bp.route("/")
def index():
    cleanup_expired_temp_files_from_storage()
    current_app_user = get_current_user()
    preview_data = session.get("preview_data")
    cleaning_summary = session.get("cleaning_summary")
    download_ready = bool(session.get("cleaned_file_path"))
    original_filename = session.get("original_filename")

    return render_template(
        "index.html",
        cleaning_summary=cleaning_summary,
        current_app_user=current_app_user,
        preview_data=preview_data,
        download_ready=download_ready,
        original_filename=original_filename,
    )


# This function removes expired temporary files based on the app cleanup settings.
# Input: no direct inputs
# Output: none
def cleanup_expired_temp_files_from_storage():
    cleanup_expired_temp_files(
        temp_folder=current_app.config["TEMP_UPLOAD_FOLDER"],
        max_age_seconds=current_app.config["TEMP_FILE_MAX_AGE_SECONDS"],
    )


# This function validates, uploads, cleans, and previews a user dataset.
# Input: HTTP POST request with uploaded file data
# Output: redirect response back to the homepage
@main_bp.route("/upload", methods=["POST"])
def upload_file():
    cleanup_expired_temp_files_from_storage()
    current_app_user = get_current_user()
    uploaded_file = request.files.get("data_file")

    previous_cleaned_file = session.pop("cleaned_file_path", None)
    previous_uploaded_file = session.pop("uploaded_file_path", None)
    session.pop("preview_data", None)
    session.pop("cleaning_summary", None)
    session.pop("original_filename", None)
    cleanup_temp_file(previous_cleaned_file)
    cleanup_temp_file(previous_uploaded_file)

    if uploaded_file is None:
        flash("Please choose a file to upload.", "danger")
        return redirect(url_for("main.index"))

    if not uploaded_file.filename:
        flash("Empty file upload is not allowed.", "danger")
        return redirect(url_for("main.index"))

    if not allowed_file(uploaded_file.filename):
        flash("Invalid file format. Only CSV and XLSX files are allowed.", "danger")
        return redirect(url_for("main.index"))

    file_size = get_uploaded_file_size(uploaded_file)
    file_size_limit = get_plan_file_size_limit(current_app_user)

    if file_size == 0:
        flash("The uploaded file is empty.", "danger")
        return redirect(url_for("main.index"))

    if file_size > file_size_limit:
        flash(
            f"File too large. Your {current_app_user.plan} plan allows up to {format_size_limit(file_size_limit)}.",
            "danger",
        )
        return redirect(url_for("main.index"))

    saved_upload_path = None

    try:
        saved_upload_path, original_filename = save_uploaded_file(uploaded_file)
        dataframe = load_dataframe_from_file(saved_upload_path, original_filename)

        if len(dataframe.columns) == 0:
            raise ValueError("The uploaded file has missing columns or an invalid structure.")

        cleaned_dataframe = clean_dataframe(dataframe, current_app_user)
        preview_data = create_preview_rows(cleaned_dataframe)
        cleaning_summary = calculate_cleaning_summary(dataframe, cleaned_dataframe)
        cleaned_file_path, download_name = save_cleaned_dataframe(cleaned_dataframe, original_filename)

        session["uploaded_file_path"] = saved_upload_path
        session["cleaned_file_path"] = cleaned_file_path
        session["cleaned_download_name"] = download_name
        session["preview_data"] = preview_data
        session["cleaning_summary"] = cleaning_summary
        session["original_filename"] = original_filename

        flash("File uploaded and cleaned successfully.", "success")
    except ValueError as error:
        cleanup_temp_file(saved_upload_path)
        flash(str(error), "danger")
    except Exception:
        cleanup_temp_file(saved_upload_path)
        flash("Processing failed. Please try again with a valid file.", "danger")

    return redirect(url_for("main.index"))


# This function sends the most recently cleaned file to the user for download.
# Input: current session data
# Output: file download response or redirect response
@main_bp.route("/download")
def download_file():
    cleanup_expired_temp_files_from_storage()
    cleaned_file_path = session.get("cleaned_file_path")
    download_name = session.get("cleaned_download_name", "cleaned_file.csv")

    if not cleaned_file_path:
        flash("No cleaned file is available for download.", "warning")
        return redirect(url_for("main.index"))

    try:
        return send_file(cleaned_file_path, as_attachment=True, download_name=download_name)
    except FileNotFoundError:
        session.pop("cleaned_file_path", None)
        session.pop("cleaned_download_name", None)
        flash("The cleaned file is no longer available. Please upload the file again.", "danger")
        return redirect(url_for("main.index"))
