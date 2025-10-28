import os
import sys
from dotenv import load_dotenv
from google import genai


def main():
    if sys.argv[1] is None:
        print("error: no prompt supplied")
        sys.exit(1)
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=sys.argv[1]
    )
    print(response.text)

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")


if __name__ == "__main__":
    main()
