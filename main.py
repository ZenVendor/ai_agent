import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    system_prompt = """
        You are a helpful AI coding agent.
        We are working with calculator program in Python. You can find its files in the working directory.
        You can perform the following operations:
            - List files and directories
            - Read file contents
            - Execute Python files with optional arguments
            - Write or overwrite files
        All paths you provide should be relative to the working directory.
        You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        Do not provide partial responses for tasks - summarize your actions and say "DONE!" when the taks is completed.
    """
    try:
        prompt = sys.argv[1]
    except Exception:
        print("Please provide prompt.")
        sys.exit(1)

    verbose = False
    if len(sys.argv) == 3:
        if sys.argv[2] == "--verbose":
            verbose = True

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    loop_count = 1
    while True:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            ),
        )

        for c in response.candidates:
            messages.append(c.content)

        if response.function_calls:
            for f in response.function_calls:
                function_call_result = call_function(f, verbose)

                if not function_call_result.parts[0].function_response.response:
                    raise Exception("No function result")
                    exit(1)

                messages.append(function_call_result)

        elif response.text:
            print(response.text)
            if "DONE!" in response.text:
                break


        loop_count += 1
        if loop_count > 20:
            print("Too many actions, exiting")
            break

    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
