
import os


def write_file(working_dir: str, file_path: str, content: str) -> str | None:
    try: 
        abs_wd: str = os.path.abspath(working_dir)

        abs_file_path: str = os.path.normpath(os.path.join(abs_wd,file_path))
        
        valid_path: bool = os.path.commonpath([abs_wd,abs_file_path]) == abs_wd

        if not valid_path: 
            raise Exception(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')

        if os.path.isdir(abs_file_path):
            raise Exception(f'Error: Cannot write to "{file_path}" as it is a directory')

        # Creating the missing parent directories, if none are missing no changes 
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)

        with open(abs_file_path, "w") as f:
            print(f"Writing to {file_path}...")
            f.write(content)

            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


    except Exception as err:
        
        print(err)
