from io import BytesIO

import pandas as pd


# This function builds an in-memory CSV file for upload tests.
# Input: raw CSV text string
# Output: BytesIO file-like object
def make_csv_file(csv_text):
    return BytesIO(csv_text.encode("utf-8"))


# This function builds an in-memory Excel file for upload tests.
# Input: pandas DataFrame
# Output: BytesIO file-like object
def make_excel_file(dataframe):
    file_buffer = BytesIO()
    dataframe.to_excel(file_buffer, index=False)
    file_buffer.seek(0)
    return file_buffer


# This function verifies that a guest user can upload, clean, preview, and download a CSV file.
# Input: Flask test client
# Output: none
def test_guest_can_upload_preview_and_download_csv(client):
    response = client.post(
        "/upload",
        data={
            "data_file": (
                make_csv_file("name,age\nAlice,30\nAlice,30\nBob,\n,\n"),
                "sample.csv",
            )
        },
        content_type="multipart/form-data",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"File uploaded and cleaned successfully." in response.data
    assert b"Showing the first 10 rows of the cleaned dataset." in response.data
    assert b"Alice" in response.data
    assert b"Bob" in response.data

    download_response = client.get("/download")

    assert download_response.status_code == 200
    assert "attachment; filename=sample_cleaned.csv" in download_response.headers["Content-Disposition"]


# This function verifies that an Excel upload is accepted and previewed successfully.
# Input: Flask test client
# Output: none
def test_guest_can_upload_excel_file(client):
    dataframe = pd.DataFrame({"city": ["Berlin", "Berlin"], "score": [10, 10]})

    response = client.post(
        "/upload",
        data={"data_file": (make_excel_file(dataframe), "report.xlsx")},
        content_type="multipart/form-data",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"File uploaded and cleaned successfully." in response.data
    assert b"Berlin" in response.data


# This function verifies that unsupported file types are rejected with a clear error.
# Input: Flask test client
# Output: none
def test_upload_rejects_invalid_file_type(client):
    response = client.post(
        "/upload",
        data={"data_file": (BytesIO(b"plain text"), "notes.txt")},
        content_type="multipart/form-data",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Invalid file format. Only CSV and XLSX files are allowed." in response.data


# This function verifies that free users cannot upload files above the free plan limit.
# Input: Flask test client
# Output: none
def test_upload_rejects_file_too_large_for_free_plan(client):
    oversized_csv = b"name\n" + (b"Alice\n" * (1024 * 1024))

    response = client.post(
        "/upload",
        data={"data_file": (BytesIO(oversized_csv), "large.csv")},
        content_type="multipart/form-data",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"File too large. Your free plan allows up to 5 MB." in response.data
