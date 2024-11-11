""""

explore dataframe summaries
"""

import pandas as pd
import marvin, openai
from dotenv import load_dotenv
import plotly.express as px

load_dotenv()

from dash import html, Dash, dcc, dash_table

df = px.data.gapminder()

app = Dash()
app.layout = [
    html.H2("pandas dataframe summarizing"),
    html.Hr(),
    html.Div(
        style={"width": "25%"},
        children=[
            html.H3("Column Content"),
            dcc.Input(id="chat-input", type="text", placeholder="Type a message..."),
            html.Button("Send", id="send-button", n_clicks=0),
            html.Hr(),
            html.Div(id="div-query-string", children="text box"),
        ],
    ),
    dash_table.DataTable(id="table", data=df.to_dict("records")),
]


if __name__ == "__main__":
    app.run(debug=True)

    """These were kind of crap at generating a signature
        print("DataFrame Info:")
        df.info()
        print("\nDataFrame Description:")
        df.describe()
        print("\nDataFrame Data Types:")
        print(df.dtypes)
        print("\nDataFrame Columns:")
        print(df.columns)
        print("\nDataFrame Shape:")
        print(df.shape)
        print("\nUnique Values per Column:")
        print(df.nunique())
        print("\nNull Values per Column:")
        print(df.isnull().sum())
        print("\nValue Counts:")
        print(df.value_counts())
        print("\nMemory Usage:")
        print(df.memory_usage())"""

