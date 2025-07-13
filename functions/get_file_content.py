import os
from google.genai import types


def get_file_content(working_directory, file_path):
    wd_path = os.path.abspath(working_directory)
    path = os.path.join(wd_path, file_path)
    full_path = os.path.abspath(path)

    if not full_path.startswith(wd_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    MAX_CHARS = 10000
    with open(full_path, "r") as file:
        file_content = file.read(MAX_CHARS)

    file_content += f"[...File '{file_path}' truncated at {MAX_CHARS} characters]"
    return file_content


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads contents of a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read content from, relative to the working directory.",
            ),
        },
    ),
)
