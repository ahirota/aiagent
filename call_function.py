from google.genai import types

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def call_function(function_call_part, verbose=False):
    # Dict of valid functions
    function_dict = {
        "get_files_info":get_files_info,
        "get_file_content":get_file_content,
        "write_file":write_file,
        "run_python_file":run_python_file
    }

    # Verbose Check and Print
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    # Set Function variables and add Hardcoded Calculator Directory to Args
    function_name = function_call_part.name
    function_args = {'working_directory':'./calculator', **function_call_part.args}

    # Check function call is valid
    if function_name not in function_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Execute Function
    function_result = function_dict[function_name](**function_args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )