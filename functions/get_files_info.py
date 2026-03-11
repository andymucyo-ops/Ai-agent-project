import os
from google.genai import types


def get_files_info(working_directory: str, directory: str=".") -> None:
    """
    function that stores the info of a directory, the files contained and the size of those files 
    """
    try:
        abs_working_dir: str = os.path.abspath(working_directory)
        target_dir: str = os.path.normpath(os.path.join(abs_working_dir,directory))
        valid_target_dir: bool = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir
      
        if not valid_target_dir:
            raise Exception(f"Error: {directory} cannot be listed, because it is outside of the permitted working directory")

        if not os.path.isdir(target_dir):
            raise Exception(f"Error: {directory} is not a directory")

        # initialize list to store files info of the directory
        file_info = []

        for file in os.listdir(target_dir):
            file_path = os.path.join(target_dir,file) 
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            # print("item_path_abs: ", item_path)
            file_info.append(f"- {file}: file_size={file_size}, is_dir={is_dir} ")

        return "\n".join(file_info)
    except Exception as err:
        print(err)


# create function declaration object to be stored for available functions to call by the agent
schema_get_files_info: types.FunctionDeclaration = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
