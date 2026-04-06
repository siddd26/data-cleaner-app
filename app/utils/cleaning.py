import pandas as pd


# This function cleans a dataset by removing duplicates and handling missing values.
# Input: pandas DataFrame and current user object
# Output: cleaned pandas DataFrame
def clean_dataframe(dataframe, user):
    try:
        cleaned_dataframe = dataframe.copy()
        cleaned_dataframe = cleaned_dataframe.drop_duplicates()
        cleaned_dataframe = cleaned_dataframe.dropna(how="all")

        text_columns = cleaned_dataframe.select_dtypes(include=["object", "string"]).columns
        numeric_columns = cleaned_dataframe.select_dtypes(include=["number"]).columns

        if len(text_columns) > 0:
            cleaned_dataframe[text_columns] = cleaned_dataframe[text_columns].fillna("")

        if len(numeric_columns) > 0:
            cleaned_dataframe[numeric_columns] = cleaned_dataframe[numeric_columns].fillna(0)

        return cleaned_dataframe
    except Exception as error:
        raise ValueError("Processing failed while cleaning the file.") from error


# This function creates a simple summary of the cleaning changes made to a dataset.
# Input: original pandas DataFrame and cleaned pandas DataFrame
# Output: dictionary with cleaning statistics
def calculate_cleaning_summary(original_dataframe, cleaned_dataframe):
    return {
        "original_rows": len(original_dataframe.index),
        "cleaned_rows": len(cleaned_dataframe.index),
        "removed_rows": max(len(original_dataframe.index) - len(cleaned_dataframe.index), 0),
        "column_count": len(cleaned_dataframe.columns),
    }


# This function creates a preview of the first rows for display in the UI.
# Input: pandas DataFrame and optional row limit integer
# Output: dictionary with column names and row values
def create_preview_rows(dataframe, row_limit=10):
    preview_dataframe = dataframe.head(row_limit).fillna("")
    return {
        "columns": preview_dataframe.columns.tolist(),
        "rows": preview_dataframe.astype(str).values.tolist(),
    }
