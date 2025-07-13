import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path):
    wd_path = os.path.abspath(working_directory)
    path = os.path.join(wd_path, file_path)
    full_path = os.path.abspath(path)

    if not full_path.startswith(wd_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'

    if not os.path.isfile(full_path):
        return f'Error: "{file_path}" is not a file'

    if file_path[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
                ["uv", "run", full_path],
                timeout=30,
                capture_output=True,
                text=True,
                cwd=wd_path
        )
    except Exception as e:
        return f"Error: executing Python file: {e}"

    if not result:
        return 'No output produced'

    results = []
    results.append(f'STDOUT: {result.stdout}')
    results.append(f'STDERR: {result.stderr}')
    if result.returncode != 0:
        results.append(f'Process exited with code {result.returncode}')

    return "\n".join(results)


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path to the Python file, relative to the working directory.",
            ),
        },
    ),
)
