import os


def get_files_info(working_dir, directory="."):
    try:
        abs_working_dir = os.path.abspath(working_dir)
        # print("abs_working_dir: ", abs_working_dir)
        
        target_dir = os.path.normpath(os.path.join(abs_working_dir,directory))
        # print("target_dir: ", target_dir)
        
        valid_target_dir = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir
      
        if not valid_target_dir:
            return f"Error: {directory} cannot be listed, because it is outside of the permitted working directory"

        if not os.path.isdir(directory):
            return f"{directory} is not a directory"

        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir,item) 
            # print("item_path_abs: ", item_path_abs)
            print(f"- {item}: file_size={os.path.getsize(item_path)}, is_dir={os.path.isdir(item_path)} ")

    except Exception:
        print("Error")

if __name__ == "__main__":
    get_files_info("calculator")
