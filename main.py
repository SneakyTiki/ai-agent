import os
from dotenv import load_dotenv
from openai import OpenAI #openai is the OpenAI Python SDK https://github.com/openai/openai-python

import argparse #https://docs.python.org/3/library/argparse.html

#Get the OpenRouter API key from the environment variables.
#They don't live here and the enviornment variables are not maintained by git to prevent exposing the API key (essentially the password/authentication)
load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key == None:
    raise RuntimeError("Whoopsie-poopsie, you don't have an API key set")

#The path to where the LLM gets accessed I guess. https://openrouter.ai/
client = OpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key = api_key,
)


parser = argparse.ArgumentParser(
    description="Simple Python CLI program for interacting with an LLM via OpenRouter."
)

parser.add_argument(
    "user_prompt", type=str, help="User input which is sent into the LLM. Input should be inside quotation marks"
)
args = parser.parse_args()

human_input = args.user_prompt

#<response> becomes and instance of a custom Python class (specifically a data model created by the OpenAI library)
#https://developers.openai.com/api/reference/python/resources/chat/subresources/completions/methods/create
response = client.chat.completions.create(
    model = "openrouter/free",
    messages=[
        {
            "role": "user",
            "content": human_input,
        }
    ],
)

if response.usage is None:
    raise RuntimeError("response.usage is None. that would likely indicate a failed API request. API response missing usage data.")

robot_response = response.choices[0].message.content
input_tokens = response.usage.prompt_tokens
output_tokens = response.usage.completion_tokens
chosen_model = response.model

print(f"User prompt: {human_input}")
print(f"Model used: {chosen_model}")
print(f"Prompt tokens: {input_tokens}")
print(f"Response tokens: {output_tokens}")
print(f"Bot response:\n{robot_response}")