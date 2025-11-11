# get_file_content.py
import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    working_file = os.path.join(working_directory, file_path)
    abs_working_file = os.path.abspath(working_file)

    # Check file is under working_directory
    if not abs_working_file.startswith(abs_working_dir):
        return(f'Error: Cannot list "{file_path}" as it is outside the permitted working directory')
    # Check that directory input is a valid directory
    if not os.path.isfile(abs_working_file):
        return(f'Error: File not found or is not a regular file: "{file_path}"')

    # Read the File and Return Content as a string
    # Truncating at Maximum Characters (Default 10,000) and appending a note
    truncated = os.path.getsize(abs_working_file) > MAX_CHARS

    with open(abs_working_file, "r") as f:
        file_content_string = f.read(MAX_CHARS)

    if truncated:
        file_content_string += f'[...File "{file_path}" truncated at 10000 characters].'

    return file_content_string