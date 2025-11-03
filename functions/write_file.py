import os
from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not full_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(os.path.dirname(full_path)):
            os.makedirs(os.path.dirname(full_path))

        with open(full_path, "w") as f:
            f.write(content)
        return (
            f"Successfully wrote to '{full_path}' ({len(content)} characters written)"
        )
    except Exception as e:
        print(f"Error: {e}")


# ai agent schema information

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a file at file_path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to be read, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to be written to the file at file_path.",
            ),
        },
    ),
)
