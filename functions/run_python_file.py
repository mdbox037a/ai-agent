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

        completed_process = subprocess.run(
            ["uv", "run", abs_file_path],
            timeout=30,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=abs_cwd_path,
            args=args,
        )

        output = (
            f"STDOUT: {completed_process.stdout}, STDERR: {completed_process.stderr}"
        )
        if completed_process.returncode != 0:
            output = (
                f"{output}, Process exited with code {completed_process.returncode}"
            )
        if output == "":
            output = "No output produced"
    except Exception as e:
        print(f"Error: executing Python file: {e}")
