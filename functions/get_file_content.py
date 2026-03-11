import os

from google.genai import types
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_working_dir: str= os.path.abspath(working_directory)
        abs_file_path: str= os.path.normpath(os.path.join(abs_working_dir,file_path))
        valid_dir: bool = os.path.commonpath([abs_working_dir,abs_file_path]) == abs_working_dir
        
        if not valid_dir: 
            raise Exception(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')

        if not os.path.isfile(abs_file_path):
            raise Exception(f'Error: File not found or is not a regular file: "{file_path}"')


        with open(abs_file_path,"r") as f:
            content: str= f.read(MAX_CHARS)

            #adding message to content if chars in file exceeded MAX_CHARS 
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                print("WARNING: File truncated!")


        return content

    except Exception as err:
        print(err)

# create function declaration object to be stored for available functions to call by the agent
schema_get_file_content: types.FunctionDeclaration = types.FunctionDeclaration(
    name="get_file_content",
    description="read and return content of a specified file in the working directrory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path to the file to read from",
            ),
        },
        required=["file_path"]
    ),
)
