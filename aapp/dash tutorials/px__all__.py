"""
Can I given an AI assistant access to all Plotly Express examples?
"""

# Import packages
import plotly.express as px
from dash import Dash, html

import os
import json
from rich import print as rprint
from pprint import pprint
import openai
from dotenv import load_dotenv
import openai, marvin


df = px.data.gapminder(year=2007)


all_px = px.__all__ #['scatter',...]

pprint(getattr(px, all_px[0]).__doc__)

pxScatter = getattr(px, all_px[0])

pprint(pxScatter.__name__)  # 'scatter'

import inspect
def example_function(param1, param2, param3="default"):
    pass

# Get the signature of the function
signature = inspect.signature(example_function)


inspect.signature(pxScatter)
