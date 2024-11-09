import openai
from openai import OpenAI

import json
from pprint import pprint
from openai.types.beta.assistant import Assistant
from rich import print as rprint
import marvin

instructions = (
    "You are a personal math tutor. Write and run code to answer math questions."
)

# client = OpenAI()
# assistant: Assistant = client.beta.assistants.create(
#     name="Math Tutor",
#     instructions=instructions,
#     tools=[{"type": "code_interpreter"}],
#     model="gpt-4o",
# )


# r = assistant.say("thai, how are you? (do you get it?)")


mass = marvin.beta.Assistant(
    name="Math Tutor",
    instructions=instructions,
    tools=[{"type": "code_interpreter"}],
    # model="gpt-4o",
)

r = mass.say("what is 2 + 2?")

rprint(r)

# r.messages[-1].content[-1].text.value
