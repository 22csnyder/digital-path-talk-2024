"""Nov10
query operations on a dataframe from natural language
"""

from typing import List, Literal
import pandas as pd
import marvin, openai
from dotenv import load_dotenv
import plotly.express as px

from pathlib import Path
from dotenv import load_dotenv
import os

import pandas as pd

load_dotenv()

import marvin, openai, requests, json
from pydantic import BaseModel


import seaborn as sns
import matplotlib.pyplot as plt

from marvin.beta.assistants import Assistant, Thread, CodeInterpreter
from marvin.utilities.logging import get_logger

df = px.data.gapminder()
df_head = df.sample(n=5, random_state=42)


@marvin.fn
def code_data_slicing(query_string="", df_head=df_head) -> str:
    """
    returns a string parsing as valid python code\
    which slices the dataframe `df` based on the `query_string`,\
    both interpreting and implementing the informatics request.

    example:
    condition: "bugs with increasing positivity"
    return_string: 'df.query(Trend == "up")'
    """
    if query_string == "":
        return "df"
    string_code: str = ""  # placeholder (logging hack)
    return string_code


def get_column_names() -> str:
    return list(df.columns)


import json

# TODO: revisit
"""class Column(BaseModel):
    name: str
    unique_values: List[str]
    dtype: Literal["str", "int", "float", "datetime"]


class DataSignature(BaseModel):
    columns: List[Column]"""


# * don't pass df in the parameter list explicitly. If I just let it be context, then it doesn't complain that it's not serializable.
def get_unique_values(column_name: str) -> str:
    unique_values = df[column_name].unique()
    # return f"the unique values in the `{column_name}` column are: {unique_values}"
    return str(unique_values)


ai = marvin.beta.Assistant(
    model="gpt-4o-mini",
    system=f"You are a helpful assistant that answers questions about the dataframe `df`.\
        the column values are: {list(df.columns)}. you may assume the name of the dataframe is `df`",
    tools=[
        CodeInterpreter,
        get_column_names,
        get_unique_values,
    ],
)

if __name__ == "__main__":
    # ai.run("what is the average life expectancy in the dataframe?")
    # run = ai.say("how many unique values are there in the `continent` column?")

    df.shape.__doc__

    column_name = "continent"

    ai.say(f"what are the unique values in the `{column_name}` column?")
