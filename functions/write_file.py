import os
from google.genai import types


def write_file(working_directory, file_path, content):
    wd_path = os.path.abspath(working_directory)
    path = os.path.join(wd_path, file_path)
    full_path = os.path.abspath(path)

    if not full_path.startswith(wd_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(os.path.dirname(full_path)):
        os.makedirs(os.path_dirname(full_path))

    with open(full_path, "w") as file:
        file.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites a file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file.",
            ),
        },
    ),
)
