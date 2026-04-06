import os
import time
import uuid

import pandas as pd
from flask import current_app
from werkzeug.utils import secure_filename


# This function checks whether the uploaded filename has an allowed extension.
# Input: filename string
# Output: boolean indicating whether the extension is allowed
def allowed_file(filename):
    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()
    return extension in current_app.config["ALLOWED_EXTENSIONS"]


# This function returns the lowercase extension from a filename.
# Input: filename string
# Output: file extension string
def get_file_extension(filename):
    return filename.rsplit(".", 1)[1].lower()


# This function calculates the size of an uploaded file without consuming it permanently.
# Input: Werkzeug uploaded file object
# Output: integer size in bytes
def get_uploaded_file_size(uploaded_file):
    uploaded_file.stream.seek(0, os.SEEK_END)
    file_size = uploaded_file.stream.tell()
    uploaded_file.stream.seek(0)
    return file_size


# This function saves an uploaded file into the temporary storage folder.
# Input: uploaded file object
# Output: tuple of saved file path and safe filename
def save_uploaded_file(uploaded_file):
    safe_name = secure_filename(uploaded_file.filename)
    unique_name = f"{uuid.uuid4().hex}_{safe_name}"
    saved_path = os.path.join(current_app.config["TEMP_UPLOAD_FOLDER"], unique_name)
    uploaded_file.save(saved_path)
    return saved_path, safe_name


# This function loads a pandas DataFrame from a saved CSV or Excel file.
# Input: saved file path string and original filename string
# Output: pandas DataFrame
def load_dataframe_from_file(file_path, original_filename):
    try:
        extension = get_file_extension(original_filename)

        if extension == "csv":
            dataframe = pd.read_csv(file_path)
        elif extension == "xlsx":
            dataframe = pd.read_excel(file_path)
        else:
            raise ValueError("Invalid file format. Only CSV and XLSX files are allowed.")

        if dataframe.empty and len(dataframe.columns) == 0:
            raise ValueError("The uploaded file is empty.")

        if len(dataframe.columns) == 0:
            raise ValueError("The uploaded file has an invalid structure.")

        return dataframe
    except ValueError:
        raise
    except Exception as error:
        raise ValueError("The file could not be read. Please upload a valid CSV or XLSX file.") from error


# This function saves a cleaned DataFrame in the same format as the original upload.
# Input: pandas DataFrame, original filename string, and output label string
# Output: tuple of output file path and download filename
def save_cleaned_dataframe(dataframe, original_filename, output_label="cleaned"):
    extension = get_file_extension(original_filename)
    base_name = os.path.splitext(secure_filename(original_filename))[0]
    download_name = f"{base_name}_{output_label}.{extension}"
    output_path = os.path.join(current_app.config["TEMP_UPLOAD_FOLDER"], f"{uuid.uuid4().hex}_{download_name}")

    try:
        if extension == "csv":
            dataframe.to_csv(output_path, index=False)
        elif extension == "xlsx":
            dataframe.to_excel(output_path, index=False)
        else:
            raise ValueError("Invalid file format. Only CSV and XLSX files are allowed.")
    except ValueError:
        raise
    except Exception as error:
        raise ValueError("Processing failed while saving the cleaned file.") from error

    return output_path, download_name


# This function deletes a temporary file if it exists.
# Input: file path string
# Output: none
def cleanup_temp_file(file_path):
    if file_path and os.path.exists(file_path):
        os.remove(file_path)


# This function deletes old temporary files from the temp upload folder.
# Input: temp folder path string and maximum file age in seconds
# Output: none
def cleanup_expired_temp_files(temp_folder, max_age_seconds):
    current_time = time.time()

    if not os.path.exists(temp_folder):
        return

    for filename in os.listdir(temp_folder):
        file_path = os.path.join(temp_folder, filename)

        if not os.path.isfile(file_path):
            continue

        file_age = current_time - os.path.getmtime(file_path)
        if file_age > max_age_seconds:
            os.remove(file_path)


# This function formats a byte size limit into a user-friendly megabyte message.
# Input: integer size in bytes
# Output: formatted size string
def format_size_limit(size_in_bytes):
    size_in_mb = size_in_bytes / (1024 * 1024)
    return f"{size_in_mb:.0f} MB"
