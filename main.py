import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from config import MAX_ITER, system_prompt
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

    if args.verbose:
        print("User prompt:\n", args.user_prompt)
    #assign user's promt to message variable
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    # function_results: list[types.Content.part] = []
    # prompt_history: list[types.GenerateContentResponse.candidates] = []

    for _ in range(MAX_ITER):
        generate_content(client, messages, args.verbose)
        if generate_content(client, messages, args.verbose) == 0:
             break
        if _ == MAX_ITER:
            sys.exit(1)
            




def generate_content(client, messages, verbose ):
    # initalize empty list to store content previous prompts
    prompt_history: list[types.GenerateContentResponse.candidates] = []
    #assign Gemini reponse to response variable
    response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents= messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt),
            )

    if response.candidates:
        prompt_history.append(response.candidates)


    for candidates_list in prompt_history:
        for candidate in candidates_list:
            messages.append(candidate.content)

    # keep track of token usage
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    #storing function calls of response as a list
    function_calls: list[types.FunctionCall] = response.function_calls

    if response.usage_metadata is None:
        raise RuntimeError("failed Api request")

    # output formatting given the arguments passed by the user
    # print("User prompt:", response )
    if verbose:
        print("Prompt tokens:\n", prompt_tokens)
        print("Response tokens:\n", response_tokens)
    

    if function_calls is None:
        print("Response:\n", response.text)
        return 0 


    function_results: list[types.Content.part] = [] 
    #calling all functions requested by the user
    for function_call in function_calls:
        # print(f"Calling function: {function_call.name}({function_call.args})")
        function_call_result: types.Content = call_function(function_call)

        # storing result of the called function
        function_results.append(function_call_result.parts[0])

        # error handling if function call fails
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
            or not function_call_result.parts[0].function_response.response
           ):
           raise RuntimeError(f"no results found for {function_call.name}")


    if verbose: 
        print(f"-> {function_call_result.parts[0].function_response.response}")

    messages.append(types.Content(role="user", parts=function_results))


    



if __name__ == "__main__":
    main()
