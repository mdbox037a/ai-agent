import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


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
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    print(response.text)

    if verbose is True:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")


if __name__ == "__main__":
    main()
