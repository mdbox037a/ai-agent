import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt, MAX_ITERATIONS
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function


def main():
    verbose = False
    if "--verbose" in sys.argv:
        verbose = True
    prompt_index = 1
    for i in range(len(sys.argv)):
        if "--" not in sys.argv[i]:
            prompt_index = i
    user_prompt = sys.argv[prompt_index]

    if user_prompt is None:
        print("error: no prompt supplied")
        sys.exit(1)
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    iterations = 0
    for i in range(MAX_ITERATIONS):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )

            made_tool_call = False

            for candidate in response.candidates or []:
                messages.append(candidate.content)

                for part in candidate.content.parts or []:
                    if getattr(part, "function_call", None):
                        made_tool_call = True
                        call = part.function_call
                        result = call_function(call)

                        if result.parts[0].function_response.response is None:
                            raise Exception("error: function call result error")
                        else:
                            messages.append(result)
                            if verbose is True:
                                print(
                                    f"-> {result.parts[0].function_response.response}"
                                )

            if not made_tool_call and response.text:
                print(response.text)
                if verbose is True:
                    prompt_tokens = response.usage_metadata.prompt_token_count
                    response_tokens = response.usage_metadata.candidates_token_count
                    print(f"User prompt: {user_prompt}")
                    print(
                        f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}"
                    )
                break
        except Exception as e:
            print(f"error: {e}")


if __name__ == "__main__":
    main()
