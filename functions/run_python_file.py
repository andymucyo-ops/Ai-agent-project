import os
import subprocess

def run_python_file(working_directory: str, file_path: str, args = None) -> str:
    try:
        abs_working_dir: str= os.path.abspath(working_directory)
        # print("abs_working_dir", abs_working_dir)
        abs_file_path: str= os.path.normpath(os.path.join(abs_working_dir,file_path))
        # print("abs_file_path", abs_file_path)
        valid_dir: bool = os.path.commonpath([abs_working_dir,abs_file_path]) == abs_working_dir
        # print("valid_dir", valid_dir)
        
        if not valid_dir: 
            raise Exception(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')

        if not os.path.isfile(abs_file_path):
            raise Exception(f'Error: "{file_path}" does not exist or is not a regular file')

        if not file_path.endswith(".py"):
            raise Exception(f'Error: "{file_path}" is not a Python file')


        #once all previous tests are passed, set commands to run as list
        commands: list[str] = ["python", abs_file_path]
        
        if args is not None:
            commands.extend(args)

        python_process: subprocess.CompletedProcess = subprocess.run(args=commands, capture_output=True,text=True, timeout=30)

        output_string = python_process.stdout
        error_string = python_process.stderr
        
        if python_process.returncode != 0:
            print(f"Process exited with code {python_process.returncode}")
        
        if error_string is None and output_string is None:
            print("No output produced")
        if error_string is not None:
            print(f"STDERR: {error_string}")
        if output_string is not None:
            print(f"STDOUT: {output_string}")

        return output_string


    
    except Exception as err:
        print(f"Error: executing Python File: {err}")
