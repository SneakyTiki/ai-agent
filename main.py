import os
from dotenv import load_dotenv
from openai import OpenAI #openai is the OpenAI Python SDK https://github.com/openai/openai-python

import argparse #https://docs.python.org/3/library/argparse.html

#The import line below has no impact on code function, and simply prevents the linter from complaining about 'messages = list_of_messages' because it makes the wrong assumption about... something about dictionaries being mutable, rather than what the OpenAI SDK is doing which is "The OpenAI SDK defines ChatCompletionMessageParam not as a generic dictionary, but as a union of specific typed dictionaries (TypedDict), such as ChatCompletionUserMessageParam."
from openai.types.chat import ChatCompletionMessageParam

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
parser.add_argument(
    "--verbose", "-v", action="store_true", help="Enables verbose output, showing token usage and model"
)

#argparse strips the leading dashes and uses the remaining string as the destination attribute name on the Namespace object it returns. So --verbose becomes args.verbose
#This is controlled by a parameter called dest (short for "destination"), which argparse infers automatically from the first long option string (the one starting with --) if you don't set it explicitly. You can override it:
#parser.add_argument("--verbose", action="store_true", dest="is_loud")
#Then you'd access it as args.is_loud instead. But if you don't specify dest, argparse just takes the long flag name, strips the dashes, and uses that.
#argparse looks for the first string starting with --. If it finds one, that becomes the basis for the attribute name (dashes stripped, internal dashes converted to underscores). If there's no -- option at all, it just uses the first option string given, dash stripped.

args = parser.parse_args()

human_input = args.user_prompt

list_of_messages: list[ChatCompletionMessageParam] = [
    {"role": "user", "content": human_input}
]

#<response> becomes an instance of a custom Python class (specifically a data model created by the OpenAI library)
#https://developers.openai.com/api/reference/python/resources/chat/subresources/completions/methods/create
response = client.chat.completions.create(
    model = "openrouter/free",
    messages = list_of_messages
)

if response.usage is None:
    raise RuntimeError("response.usage is None. that would likely indicate a failed API request. API response missing usage data.")

robot_response = response.choices[0].message.content
input_tokens = response.usage.prompt_tokens
output_tokens = response.usage.completion_tokens
chosen_model = response.model

if args.verbose:
    print(f"User prompt: {human_input}")
    print(f"Model used: {chosen_model}")
    print(f"Prompt tokens: {input_tokens}")
    print(f"Response tokens: {output_tokens}")
    print(f"Bot response:\n{robot_response}")
else:
    print(f"Bot response:\n{robot_response}")