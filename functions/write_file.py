# write_file.py
import os
from google import genai
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    working_file = os.path.join(working_directory, file_path)
    abs_working_file = os.path.abspath(working_file)

    # Check file is under working_directory
    if not abs_working_file.startswith(abs_working_dir):
        return(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')

    # If the file path doesn't exist, create it
    try:
        if not os.path.exists(os.path.dirname(abs_working_file)):
            os.makedirs(os.path.dirname(abs_working_file))

        # Write Content to File
        with open(abs_working_file, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{abs_working_file}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error writing to file: {e}"
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to file in the specified directory, overwriting existing text and creating subdirectories and file itself if necessary, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write inside the specified file.",
            ),
        },
        required=["file_path", "content"],
    ),
)