"""
need to test the CodeInterpreter tool real quick
"""

from logging import Logger
from dotenv import load_dotenv
import os
import numpy as np
import openai
import pandas as pd

load_dotenv()
from pathlib import Path
import marvin
from marvin.beta.assistants import Assistant, CodeInterpreter

#set verbose to true
marvin.settings.verbose = True
marvin.settings.log_level = "DEBUG"
from marvin.utilities.logging import get_logger
mvlogger: Logger = get_logger("debug_mv_ai_assistant"   )

def makes_dataframe(n: int) -> pd.DataFrame:
    """
    Returns a 2 column by `n` row dataframe by evaluating a trigonometric function
    """
    x = np.linspace(0., 10, n)
    y = np.sin(x) * np.cos(x)
    return pd.DataFrame( {'x': x, 'y': y})


# def test_codeinterpreter():
#     """
#     Can it use tools I give it to return objects rather than text?
#     """

# def dataframe_exec():
#     #create a CodeInterpreter object
#     interpreter = CodeInterpreter(logger=mvlogger,tools=[makes_dataframe])

ai = Assistant(tools=[makes_dataframe])
def get_content(result: AssistantResult):
    return result.messages[1].content[0]#.replace("```python","").replace("```","")

if __name__ == "__main__":
    # out = ai.say("make me a dataframe with at least 20 rows")

    out_code = ai.say("return a string which is valid python code, potentially using makes_dataframe as a function, to provide a string which when `eval` is applied will generate a dataframe with at least 20 rows")
    
    pycode = out_code.messages[1].content[0].text.value
    # .replace("*```python","").replace("```*","")
    pprint(out_code)
    from rich import print as rprint
    rprint(pycode)
    
    result2=ai.say("oh hey by the way could you just returnb the code and nothing else. I don't want to be rude but I don't want to do any parsing")
    from typing import TypeVar 
    T = TypeVar("T")    
    def squareit(x: T) -> T:
        return x*x
    ai.say( "calcalate sum of the first 10 numbers squared", tools=[squareit])    
    ai.say("why are you not using the squareit tool?", tools=[squareit])
    
    ai.say("give me an example of a custom python function which was really useful as a tool given to you, an ai assistant")
    
    ai.say("if I give you a function that plots, can you use it to plot?")


    def sollicits_information( query: str)->str:
        """asks the user a folow-up question"""
        print(query)
        user_input = input(query)
        return user_input
    
    ai.say("am I a boy or a girl?", tools=[sollicits_information])