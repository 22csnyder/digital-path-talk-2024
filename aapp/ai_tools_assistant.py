import openai
from openai import OpenAI

import json
from pprint import pprint
from openai.types.beta.assistant import Assistant
from rich import print as rprint



client = OpenAI()

assistant: Assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o",
)
