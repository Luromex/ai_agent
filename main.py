import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("API key not found")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Send a prompt to an AI chatbot.")
    parser.add_argument("user_prompt", type=str, help="The message to send to the chatbot.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages=[
        {"role": "user", "content": args.user_prompt},
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages = messages
    )

    if response.usage is None:
        raise RuntimeError("API response appears to be malformed")

    if args.verbose: 
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
        print("Response:")
        print(response.choices[0].message.content)
    else:
        print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
