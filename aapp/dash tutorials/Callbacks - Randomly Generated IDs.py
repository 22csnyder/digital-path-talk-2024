"""dynamic layout?

by using callbacks that modify 'children' property of a component, we can dynamically change the layout of the app
"""

from dash import Dash, html, dcc, callback, Output, Input

app = Dash(__name__)


text = dcc.Input(value="hello (replace me with 'Checklist')")
user_input = html.Div()
app.layout = html.Div([text, user_input])


clargs = dict(
    options=["New York City", "Montreal", "San Francisco"],
    value=["Montreal", "San Francisco"],
    id="checklist-example",
)


@app.callback(Output(user_input, "children"), Input(text, "value"))
def update_output(input_value):
    if input_value in dcc.__all__:
        Component = getattr(dcc, input_value)
        return Component(**clargs)
    return input_value


# Checklist = dcc.Checklist(**clargs)
# dcc.Input
# dcc.Output #dne
# import dash
# dash.State

if __name__ == "__main__":
    app.run(debug=True)
