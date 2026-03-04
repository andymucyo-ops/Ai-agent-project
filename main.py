import os
from dotenv import load_dotenv
from google import genai
import argparse

def main():

    # loading all variables from .env file
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("Api key not found")

    client = genai.Client(api_key=api_key)

    # generating argparse object that accepts users input
    user_input = argparse.ArgumentParser(description="Chatbot")
    user_input.add_argument("user_prompt", type=str, help="User's prompt")
    args = user_input.parse_args()

    response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=args.user_prompt
            )

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if response.usage_metadata is None:
        raise RuntimeError("failed Api request")

    # print("User prompt:", response )
    print("Prompt tokens: ", prompt_tokens)
    print("Response tokens: ", response_tokens)
    print("Response:\n", response.text)

if __name__ == "__main__":
    main()
