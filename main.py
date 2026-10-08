import os
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function

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
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages = messages,
        temperature=0,
        tools=available_functions,
    )

    message = response.choices[0].message

    if message.tool_calls:
        for tool_call in message.tool_calls:
            if tool_call.type != "function": continue

            result_message = call_function(tool_call, args.verbose)

            if not result_message.get("content"):
                raise RuntimeError(f"Empty function response for {tool_call.function.name}")

            if args.verbose:
                print(f"-> {result_message['content']}")
    else:
        print("Response:")
        print(message.content)


    if response.usage is None:
        raise RuntimeError("API response appears to be malformed")

    if args.verbose: 
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

if __name__ == "__main__":
    main()
