"""
Pathogen Prompting 

"""

from pathlib import Path
from dotenv import load_dotenv
import os

import pandas as pd

load_dotenv()

import marvin, openai, requests, json
from pydantic import BaseModel


import seaborn as sns
import matplotlib.pyplot as plt


from marvin.utilities.logging import get_logger

logger = get_logger("pathogen_prompt")

DATA_PATH = Path(os.getenv("DATA"))
pathogen_dataframe: pd.DataFrame = pd.read_csv(DATA_PATH / "raw" / "pathogens.csv")


@marvin.fn
def code_data_slicing(
    subset_description: str = "all data", df=pathogen_dataframe
) -> str:
    """
    returns a string parsing as valid python code\
    which slices the dataframe `df` based on the `subset_description`,\
    both interpreting and implementing the informatics request.

    example:
    condition: "bugs with increasing positivity"
    return_string: 'df.query(Trend == "up")'
    """
    if subset_description == "all data":
        return "df"
    string_code: str = ""  # placeholder (logging hack)
    return string_code


# logger.info(f"generating slicing code for {subset_description}")
# logger.debug(f"interpretation-equivalent code resulted: {string_code}")


@marvin.fn
def code_data_calculation(calculation_description: str, df=pathogen_dataframe) -> str:
    """
    Generates and returns a string of valid Python code that performs calculations or derivations
    on the dataframe `df` based on the `calculation_description`.

    This function interprets natural language instructions for data analysis tasks and translates
    them into executable Python code. It can handle various types of calculations, including but
    not limited to:
    - Basic statistical measures (mean, median, mode, etc.)
    - Aggregations and grouping operations
    - Percentile calculations
    - Cumulative statistics
    - Custom metrics and derivations

    Parameters:
    calculation_description (str): A natural language description of the calculation or derivation to be performed.
    df (pd.DataFrame): The input dataframe to perform calculations on. Defaults to pathogen_dataframe.

    Returns:
    str: A string containing valid Python code that implements the requested calculation or derivation.

    Example inputs and expected outputs:
    1. Input: "Calculate the average positivity rate across all pathogens"
       Output: 'df["Positivity"].mean()'

    2. Input: "Find the pathogen with the highest number of positive tests"
       Output: 'df.loc[df["Number Positives"].idxmax(), "Pathogen"]'

    3. Input: "Calculate what cumulative percentile of pathogens accounts for 50% of total positive tests"
       Output: '''
       df_sorted = df.sort_values("Number Positives", ascending=False)
       df_sorted["Cumulative_Positives"] = df_sorted["Number Positives"].cumsum()
       total_positives = df_sorted["Number Positives"].sum()
       percentile = df_sorted[df_sorted["Cumulative_Positives"] <= total_positives * 0.5].shape[0] / df_sorted.shape[0] * 100
       percentile
       '''

    Note: The function aims to generate code that is as accurate and efficient as possible,
    but the output should always be reviewed and tested before use in production environments.
    """
    string_code: str = ""  # placeholder (logging hack)
    return string_code


# logger.info(f"Generating calculation code for: {calculation_description}")
# logger.debug(f"Generated code for calculation: {string_code}")


class PlotInstructions(BaseModel):
    title: str
    x_label: str
    y_label: str
    plot_type: str
    color: str
    additional_instructions: list[str]


@marvin.fn
def generate_plot_instructions(
    data_description: str, plot_goal: str
) -> PlotInstructions:
    """
    Generate instructions for creating a plot based on the given data description and plot goal.

    Args:
    data_description (str): A description of the data to be plotted.
    plot_goal (str): The goal or purpose of the plot.

    Returns:
    PlotInstructions: A set of instructions for creating the plot.
    """


@marvin.fn
def generate_plot_code(instructions: PlotInstructions, data_variable: str) -> str:
    """
    Generate Python code to create a plot based on the given instructions.

    Args:
    instructions (PlotInstructions): The instructions for creating the plot.
    data_variable (str): The name of the variable containing the data to be plotted.

    Returns:
    str: Python code that creates the plot using matplotlib.
    """


def create_plot(instructions: PlotInstructions, data):
    """
    Create a plot based on the given instructions and data.

    Args:
    instructions (PlotInstructions): The instructions for creating the plot.
    data: The data to be plotted.

    Returns:
    bytes: The plot as a PNG image.
    """
    # Generate the plotting code
    plot_code = generate_plot_code(instructions, "data")

    # Create a new figure
    plt.figure(figsize=(10, 6))

    # Execute the plotting code
    local_vars = {"plt": plt, "data": data}
    exec(plot_code, globals(), local_vars)


#  # Save the plot to a bytes buffer
#  buf = io.BytesIO()
#  plt.savefig(buf, format="png")
#  buf.seek(0)

#  # Close the plot to free up memory
#  plt.close()

#  return buf.getvalue()
