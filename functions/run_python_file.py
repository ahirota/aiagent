# run_python_file.py
import os, subprocess

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    working_file = os.path.join(working_directory, file_path)
    abs_working_file = os.path.abspath(working_file)

    # Check file is under working_directory
    if not abs_working_file.startswith(abs_working_dir):
        return(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    
    # Check file exists
    if not os.path.exists(abs_working_file):
        return(f'Error: File "{file_path}" not found.')
    
    # Check file is a python file
    if not file_path.endswith(".py"):
        return(f'Error: "{file_path}" is not a Python file.')
    
    try:
        command = ['python3', abs_working_file]
        if args:
            command += args
        run = subprocess.run(command, capture_output=True, timeout=30, text=True)
        stdout = 'STDOUT:'+run.stdout
        stderr = 'STDERR:'+run.stderr
        returncode = f'\nProcess exited with code {run.returncode}' if run.returncode != 0 else ''
        return(f'{stdout}\n{stderr}{returncode}')
    except Exception as e:
        return f"Error: executing Python file: {e}"