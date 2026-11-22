import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_path = os.path.abspath(working_directory) #https://docs.python.org/3/library/os.path.html#os.path.abspath
        #full_path = os.path.join(abs_path, directory)
        #normalize_path = os.path.normpath(full_path)

        if os.path.isdir(directory):
            target_dir = os.path.normpath(
                os.path.join(abs_path, directory)
            )
        else:
            return f'Error: "{directory}" is not a directory'

        valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path #True if valid, False if not
        if valid_target_dir:
            return f'Success: "{directory}" is within the working directory'
        else:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    except Exception as e:
        return f'Error: os.path encountered the following problem "{e}"'