
from google.genai import types

from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file 


available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
            ],
        )

def call_function(function_call: types.FunctionCall, verbose: bool=False ) -> type.Content:

    function_name = function_call.name or "" 
    
    print(f"Calling function: {function_name}({function_call.args})" if verbose else f" - Calling function: {function_name}"
              )

    function_map: dict[str,types.FunctionDeclaration] = {
            "schema_get_files_info":schema_get_files_info,
            "schema_get_file_content":schema_get_file_content,
            "schema_write_file":schema_write_file,
            "schema_run_python_file": schema_run_python_file
            }

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    else:
        # makinge a shallow copy of the args dictonnary
        args = dict(function_call.args) if function_call.args else {}

    args["working_directory"] = "./calculator"

    #calling the required function to execute task
    function_result: str = function_map[function_name](**args)


    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
            )
        ],
    )



