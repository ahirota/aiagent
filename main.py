# System Imports
import os, sys
from dotenv import load_dotenv

# GenAI Imports
from google import genai
from google.genai import types

# Functional Imports
from prompts import system_prompt
from call_function import available_functions, call_function
from config import MAX_RUN_COUNT

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

    # Generate Content BY Looping
    run_count = 0
    while run_count < MAX_RUN_COUNT:
        run_count += 1

        try:
            final_response = generate_content(client, messages, verbose_flag)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")

    if run_count == MAX_RUN_COUNT:
        print(f"Loop has reached Maximum Iterations: {MAX_RUN_COUNT}. Terminating Prompt.")
        sys.exit(1)


def generate_content(client, messages, verbose):
    # Get Response from GenAI
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )

    # Check the Candidate property and add content to Messages
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    # Print Response
    # Verbose Flag Details
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    # Check for Function Calls and Execute
    if not response.function_calls:
        return response.text

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
    
    # Append Response as new User Message
    messages.append(types.Content(role='user', parts=function_responses),)


if __name__ == "__main__":
    main()
