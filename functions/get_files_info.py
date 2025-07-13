import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    wd_full_path = os.path.abspath(working_directory)
    path = os.path.join(wd_full_path, directory)
    full_path = os.path.abspath(path)

    if not full_path.startswith(wd_full_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'

    files_info = []
    for item in os.listdir(full_path):
        size = os.path.getsize(os.path.join(full_path, item))
        is_dir = os.path.isdir(os.path.join(full_path, item))
        files_info.append(f'- {item}: file_size={size} bytes, is_dir={is_dir}')

    return "\n".join(files_info)


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
