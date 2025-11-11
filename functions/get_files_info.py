# get_files_info.py
import os

def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    working_path = os.path.join(working_directory, directory)
    abs_working_path = os.path.abspath(working_path)
    
    # Check directory is under working_directory
    if not abs_working_path.startswith(abs_working_dir):
        return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    # Check that directory input is a valid directory
    if not os.path.isdir(abs_working_path):
        return(f'Error: "{directory}" is not a directory')
    
    # Gather File Info
    file_info = []
    for item in os.listdir(abs_working_path):
        item_path = os.path.join(abs_working_path, item)
        name = item
        size = os.path.getsize(item_path)
        is_dir = os.path.isdir(item_path)
        file_info.append(f'- {name}: file_size={size} bytes, is_dir={is_dir}')
    return "\n".join(file_info)
        
        
