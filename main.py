# System Imports
import os, sys
from dotenv import load_dotenv

# GenAI Imports
from google import genai
from google.genai import types

# Functional Imports
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    # Load and set up GenAI Client
    load_dotenv()
    api_key = os.environ.get('GEMINI_API_KEY')
    client = genai.Client(api_key=api_key)

    # Check and Validate User Input
    verbose_flag = "--verbose" in sys.argv[1:]
    args = []
    for arg in sys.argv[1:]:
        # Remove ALL flags where they appear
        if not arg.startswith('--'):
            args.append(arg)

    # Error Message and exit if prompt is empty or contains ONLY flags
    if not args:
        print('Error: No Prompt Detected.')
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        if verbose_flag:
            print('\nThe "--verbose" flag adds additional User Information to the response of this agent, and is not sufficient as a User Prompt.')
            print('Information includes: the user\'s prompt, as well as remaining prompt/response tokens from using this API.')
        sys.exit(1)

    # Build User Prompt from Input
    user_prompt = ' '.join(args)
    messages = [
       types.Content(role='user', parts=[types.Part(text=user_prompt)]),
    ]

    # If Verbose, State User Prompt
    if verbose_flag:
        print(f"User prompt: {user_prompt}")

    # Generate Content
    generate_content(client, messages, verbose_flag)


def generate_content(client, messages, verbose):
    # Get Response from GenAI
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )

    # Print Response
    # Verbose Flag Details
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    # Check for Function Calls and Execute
    if not response.function_calls:
        print(response.text)

    # Get Function Calls and Print Where Necessary
    function_responses = []
    for function_call_part in response.function_calls:
        function_response = call_function(function_call_part, verbose)
        if not function_response.parts or not function_response.parts[0].function_response.response:
            raise Exception("Function Response is Empty")
        if verbose:
            print(f"-> {function_response.parts[0].function_response.response}")
        function_responses.append(function_response.parts[0])
    
    if not function_responses:
        raise Exception("No function responses generated, exiting.")            


if __name__ == "__main__":
    main()
