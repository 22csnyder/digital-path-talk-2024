import os, pandas as pd, marvin
import sys, json
from pprint import pprint
from rich import print as rprint
from dotenv import load_dotenv
from pathlib import Path
from loguru import logger
load_dotenv()
logger.remove()
logger.add(sys.stdout, level="WARNING")
logger.add("bugchat.log", level="INFO")
DATA_PATH = Path(os.getenv("DATA"))
logger.info(f"Data path: {DATA_PATH}")

import marvin, openai
from marvin.utilities.logging import get_logger
marvin_logger = get_logger(name="marvin.bugchat")


from pydantic import BaseModel

df = pd.read_csv(DATA_PATH / "raw" / "pathogens.csv")
with pd.option_context('display.max_columns', 100, 'display.width', 1000, 'display.max_colwidth', 200):
    rprint(df)


from IPython.display import display, HTML, IFrame
import ipywidgets as widgets
from ipywidgets.embed import embed_minimal_html


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


#------------------------------------------------------------------------------#

from typing import Callable
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display


def plot_sin(n):
    x = np.linspace(0, 2 * np.pi, n)
    y = np.sin(x)
    
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set(title='Sine Wave', xlabel='x', ylabel='sin(x)')
    
    display(fig)
    plt.close(fig)


def interactive_slider_plot(fn:Callable[int,None]): # type: ignore
    n_slider = widgets.IntSlider(value=100, min=10, max=1000, step=10, description='n pts:', continuous_update=False)
    
    def update_plot(n):
        output_widget.clear_output()
        with output_widget:
            display(fn(n))
    
    output_widget = widgets.Output()
    display(n_slider, output_widget)
    
    widgets.interactive(update_plot, n=n_slider)

# Example usage
interactive_plot_sin()


#------------------------------------------------------------------------------#




def display_refresh(fn:Callable[str,None], output_widget:widgets.Output): # type: ignore
    def update_fn(*args, **kwargs):
        output_widget.clear_output()
        with output_widget:
            display(fn(*args, **kwargs))
    return update_fn

def interactive_text_response(fn:Callable[str,None]): # type: ignore
    # n_slider = widgets.IntSlider(value=100, min=10, max=1000, step=10, description='n pts:')
    text_input = widgets.Text(description='text input:', continuous_update=False)
    output_widget = widgets.Output()
    update_callback = display_refresh(fn=fn, output_widget=output_widget)
    
    display(text_input, output_widget)
    widgets.interactive(update_callback,# __interact_f : function
                        # The function to which the interactive widgets are tied
                        text=text_input)
                        # The interactive widget

def double_string(text:str):
    return text*2
# Example usage
interactive_text_response(double_string)