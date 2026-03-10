import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from config import system_prompt
from functions.call_function import available_functions, call_function

def main():

    # loading .env file to access variables declared in it, here GEMINI_API_KEY
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("Api key not found")

    client = genai.Client(api_key=api_key)

    # generating argparse object to manage users input
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User's prompt")
    parser.add_argument("--verbose", 
                            action="store_true", 
                            help="Enable verbose output"
                            )
    args = parser.parse_args()

    #assign user's promt to message variable
    message = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    #assign Gemini reponse to resdponse variable
    response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents= message,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt),
            )

    # keep track of token usage
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    #storing function calls of reponse as a list
    function_calls: list[types.FunctionCall] = response.function_calls

    if response.usage_metadata is None:
        raise RuntimeError("failed Api request")

    # output formatting given the arguments passed by the user
    # print("User prompt:", response )
    if args.verbose:
        print("User prompt:\n", args.user_prompt)
        print("Prompt tokens:\n", prompt_tokens)
        print("Response tokens:\n", response_tokens)
    
    if function_calls is None:
        print("Response:\n", response.text)
    else:
        #calling all functions requested by the user
        for function_call in function_calls:
            # print(f"Calling function: {function_call.name}({function_call.args})")
            function_call_result: types.Content = call_function(function_call)
    
    # error handling if function call fails
    try:
        if function_call_result.parts is None:
            raise Exception("empty parts list, something went wrong with function call!")
        if function_call_result.parts[0].function_response is None:
            raise Exception("No FunctionResponse object found!")
        if function_call_result.parts[0].function_response.response is None:
            raise Exception("No function result found!")

    except Exception as e:
        print(e)

    # storing result of the called function
    function_results: list = function_call_result.parts[0]

    if args.verbose: 
        print(f"-> {function_call_result.parts[0].function_response.response}")

    



if __name__ == "__main__":
    main()
