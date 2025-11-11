import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    args = sys.argv[1:]

    v_flag = "--verbose" in args 

    if v_flag:
        args.remove("--verbose")

    if len(args) == 0:
        print("Error: No Prompt Detected.")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        if v_flag:
            print("""\nThe "--verbose" flag adds additional User Information to the response of this agent, and is not sufficient as a User Prompt.
Information includes: the user's prompt, as well as remaining prompt/response tokens from using this API.
                  """)
        sys.exit(1)

    user_prompt = " ".join(args)

    messages = [
       types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ] 
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages
    )
    if v_flag:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(response.text)


if __name__ == "__main__":
    main()
