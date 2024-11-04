import matplotlib.pyplot as plt
import openai, marvin
from rich import print as rprint
from pprint import pprint
import json

def plot_graph(x=None, y=None):
    # Example data
    x = x or [1, 2, 3, 4, 5]
    y = y or [2, 3, 5, 7, 11]

    plt.plot(x, y)
    plt.title("Function called!")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.show()

    # Call the function to plot the graph
    # plot_graph()


def reponse_length(response: str) -> int:
    return len(response)


tool_response_length = {
    "type": "function",
    "function": {
        "name": "reponse_length",
        "description": "Returns the length (number of characters) of the response",
        "parameters": {
            "type": "object",
            "properties": {
                "response": {"type": "string"},
            },
            "required": ["response"],
        },
    },
}

tools = [
    tool_response_length,
    {
        "name": "plot_graph",
        "parameters": {"x": list, "y": list},
        "description": "Plots a graph with the given x and y values",
        "fn": plot_graph,
    },
]

available_functions = {
    "reponse_length": reponse_length,
    "plot_graph": plot_graph,
}


def openai_response(prompt: str, messages: list) -> str:
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=[tool_response_length],
        # tools=tools,
        # tool_choice="auto",
    )
    message = response.choices[0].message
    messages.append(message)
    rprint(message)
    return response


if __name__ == "__main__":
    prompt = "What is the length of the response?"
    messages = [{"role": "user", "content": prompt}]
    response = openai_response(prompt, messages)

    rprint(response.choices[0])

    for tool_call in response.choices[0].message.tool_calls:
        rprint(tool_call)
        arguments = json.loads(tool_call.function.arguments)
        rprint(arguments)
        function = available_functions[tool_call.function.name]
        result = function(**arguments)
        rprint(result)

        result_message = {
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": tool_call.function.name,
            "content": str(result),
        }
        messages.append(result_message)

        second_response = openai.chat.completions.create(
            model="gpt-4o-mini", messages=messages, stream=True
        )
        chunks = list(second_response)
        deltas = [chunk.choices[0].delta.content or "" for chunk in chunks]
        final_response = "".join(deltas)
        actual_truth = f"The length of the response is {len(final_response)}"

        rprint(final_response)
        rprint(actual_truth)


    rprint(second_response)
