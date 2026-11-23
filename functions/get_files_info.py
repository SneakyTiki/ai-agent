import os

def format_result(directory, info: list[dict[str, str]]) -> str:
    dir_name: str = "current" if directory == "." else f"'{directory}'"
    formatted_answer: list = [f'Result for {dir_name} directory:']
    for item in info:
        formatted_answer.append(
            f'  - {item["name"]}: file_size={item["size"]} bytes, is_dir={item["is_dir"]}'
            )
    return "\n".join(formatted_answer)

#moved the validation check from Ch2 L2 into this function
def validate_directory(working_directory: str, directory: str = ".") -> tuple[str, str]:    
    """Return (target_dir, error). One of them is an empty string.

That's a docstring: a string literal placed as the first statement inside a function, class, or module. Python stores it as documentation for that object instead of treating it as ordinary code.

print(add.__doc__)  # Return the sum of a and b.
help(add)           # shows it formatted

    Editors show it as a tooltip when you hover over the function.
    help() and documentation generators read it.
    It runs no logic. It's a description for humans and tools.

Triple quotes let it span several lines, which is why they're the convention
    
It isn't the same as a # comment. A comment is thrown away at runtime, while a docstring is kept on the function as __doc__.    
    """
    try:
        abs_path = os.path.abspath(working_directory) #https://docs.python.org/3/library/os.path.html#os.path.abspath
        #full_path = os.path.join(abs_path, directory)
        #normalize_path = os.path.normpath(full_path)
        target_dir = os.path.normpath(
                        os.path.join(abs_path, directory)
                    )

        valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path #True if valid, False if not
        if not valid_target_dir:
            return "", f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return "", f'Error: "{directory}" is not a directory'
        else:
            return target_dir, ""                

    except Exception as e:
        return "", f'Error: os.path encountered the following problem - "{e}"'

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        #If validation clears, we do stuff. Otherwise, just pass errors from validation
        target_dir, error = validate_directory(working_directory, directory)
        if error:
            return error    

        info_list: list[dict] = []
        for item in os.listdir(target_dir):
            path = os.path.join(target_dir, item)
            info_list.append({
                "name": item,
                "size": os.path.getsize(path),
                "is_dir": os.path.isdir(path)
            })

        return format_result(directory, info_list)
    except Exception as e:
            return f'Error: Itemizing the directory items failed - "{e}"'