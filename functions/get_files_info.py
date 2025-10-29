import os


def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.abspath(os.path.join(working_directory, directory))
        if not full_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        contents = []
        for item in os.listdir(full_path):
            full_item = os.path.join(full_path, item)
            contents.append(
                f" - {item}: file_size={os.path.getsize(full_item)} bytes, is_dir={os.path.isdir(full_item)}"
            )
        return "\n".join(contents)
    except Exception as e:
        print(f"Error: {e}")
