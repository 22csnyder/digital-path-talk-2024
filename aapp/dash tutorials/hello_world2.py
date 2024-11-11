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
    # dcc.Graph(figure=px.histogram(df, x="continent", y="lifeExp", histfunc="avg")),
    dcc.Graph(figure={}, id="controls-and-graph"),
]

@callback(
    Output(component_id="controls-and-graph", component_property="figure"),
    Input(component_id="controls-and-radio-item", component_property="value"),
)
def update_graph(col_chosen: str):
    fig = px.histogram(data_frame=df, x="continent", y=col_chosen, histfunc="avg")
    return fig


# from dash.development.base_component import Component
# from dash import Dash, html, dash_table, dcc #noqa
# getattr(dcc, "RadioItems")
# getattr(dash_table, "DataTable")



# Run the app
if __name__ == "__main__":
    app.run(debug=True)
