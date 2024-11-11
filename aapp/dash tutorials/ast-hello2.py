"""
Nov 11 2024
https://dash.plotly.com/tutorial

Second tutorial
"""

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


# Incorporate data
df: pd.DataFrame = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv"
)
# df = px.data.gapminder().query("year == 2007")


# Initialize the app
app = Dash()

# App layout
app.layout = [
    html.Div(children="My First App with Data and a Graph"),
    html.Hr(),
    dcc.RadioItems(
        options=["pop", "lifeExp", "gdpPercap"],
        value="lifeExp",
        id="controls-and-radio-item",
    ),
    dash_table.DataTable(data=df.to_dict("records"), page_size=7),
    dcc.Graph(figure={}, id="controls-and-graph"),
    html.Div(id='chat-history', children=[]),  # Chat history display
    dcc.Input(id='chat-input', type='text', placeholder='Type a message...'),  # Chat input
    html.Button('Send', id='send-button', n_clicks=0)  # Send button
]

@callback(
    Output(component_id="controls-and-graph", component_property="figure"),
    Input(component_id="controls-and-radio-item", component_property="value"),
)
def update_graph(col_chosen: str):
    fig = px.histogram(data_frame=df, x="continent", y=col_chosen, histfunc="avg")
    return fig

@callback(
    Output('chat-history', 'children'),
    Input('send-button', 'n_clicks'),
    Input('chat-input', 'value'),
    prevent_initial_call=True
)
def update_chat(n_clicks, message):
    if n_clicks > 0 and message:
        # Here you would integrate with an AI model to generate a response
        ai_response = f"AI: {message[::-1]}"  # Example: reversing the message as a mock response
        return [html.Div(f"User: {message}"), html.Div(ai_response)]


# from dash.development.base_component import Component
# from dash import Dash, html, dash_table, dcc #noqa
# getattr(dcc, "RadioItems")
# getattr(dash_table, "DataTable")


app.layout = [
    html.Div(children="My First App with Data and a Graph"),
    html.Hr(),
]


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
