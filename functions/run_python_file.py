import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        abs_dir_path = os.path.dirname(abs_file_path)
        abs_cwd_path = os.path.abspath(working_directory)

        if not abs_file_path.startswith(abs_cwd_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(abs_file_path):
            return f'Error: File "{file_path}" not found.'
        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        cmd = ["uv", "run", file_path]
        cmd.extend(args)
        completed_process = subprocess.run(
            cmd, timeout=30, capture_output=True, cwd=abs_cwd_path, text=True
        )

        output = (
            f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}"
        )
        if completed_process.returncode != 0:
            output = (
                f"{output}\nProcess exited with code {completed_process.returncode}"
            )
        if output == "":
            output = "No output produced"

        return output
    except Exception as e:
        print(f"Error: executing Python file: {e}")
