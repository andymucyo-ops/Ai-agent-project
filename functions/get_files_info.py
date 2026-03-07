import os


def get_files_info(working_dir, directory="."):
    """
    function that prints the info of a directroy, the files contained and the size of those files 
    """
    try:
        abs_working_dir = os.path.abspath(working_dir)
        # print("abs_working_dir: ", abs_working_dir)
        
        target_dir = os.path.normpath(os.path.join(abs_working_dir,directory))
        # print("target_dir: ", target_dir)
        
        valid_target_dir = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir
      
        if not valid_target_dir:
            raise Exception(f"Error: {directory} cannot be listed, because it is outside of the permitted working directory")

        if not os.path.isdir(target_dir):
            raise Exception(f"Error: {directory} is not a directory")
        if directory == ".":
            print("Results for current directory")        
        else:
            print(f"Results for '{directory}' directory")

        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir,item) 
            # print("item_path_abs: ", item_path)
            print(f"- {item}: file_size={os.path.getsize(item_path)}, is_dir={os.path.isdir(item_path)} ")

    except Exception as err:
        print(err)
