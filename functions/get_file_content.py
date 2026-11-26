#from functions.get_files_info import validate_directory
import os
from config import * #Imports all

def validate_file(working_directory: str, file_path: str) -> tuple[str, str]:    
    """
    Return (target_file, error). One of them is an empty string.    
    """
    try:
        abs_path = os.path.abspath(working_directory) #https://docs.python.org/3/library/os.path.html#os.path.abspath
        target_file = os.path.normpath(
                        os.path.join(abs_path, file_path)
                    )

        valid_target_file = os.path.commonpath([abs_path, target_file]) == abs_path #True if valid, False if not
        if not valid_target_file:
            return "", f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return "", f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            return target_file, ""                

    except Exception as e:
        return "", f'Error: os.path encountered the following problem - "{e}"'

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        target_file, error = validate_file(working_directory, file_path)
        if error:
            return error

        file_content = open(target_file).read(MAX_CHARS)
        truncated_msg = f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        if len(file_content) < len(open(target_file).read(MAX_CHARS+10)):
            file_content += truncated_msg
        return file_content

    except Exception as e:
        return f'Error: Getting file contents failed for the following reason - "{e}"'
    pass