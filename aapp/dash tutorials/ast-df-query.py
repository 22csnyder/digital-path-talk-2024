"""query operations on a dataframe from natural language"""

# Import packages
from dash import Dash, html, dash_table, dcc
from dash import callback, Output, Input
import pandas as pd
import plotly.express as px


import os
import json
from rich import print as rprint
from pprint import pprint
import openai
from dotenv import load_dotenv
import openai, marvin


df = px.data.gapminder().query("year == 2007")

# Initialize the app

if __name__ == "__main__":
    print("hello")
    print(df.query.__doc__)
