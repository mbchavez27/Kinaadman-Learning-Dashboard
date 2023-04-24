from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


external_stylesheets = [
    #  for Bootstrap CDN
    {
        "href": "https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css",
        "rel": "stylesheet",
        "integrity": "sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor:",
        "crossorigin": "anonymous",
    },
    # Roboto
    {
        "href": "https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap",
        "rel": "stylesheet",
    },
]

app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    title="Kinaadman Learning Dashboard",
)
app.layout = html.Div(
    children=[
        html.Nav(
            className="navbar bg-body-tertiary",
            children=[
                html.Div(
                    className="container-fluid",
                    children=[
                        html.Span(
                            className="navbar-brand mb-0",
                            style={"font-family": "Roboto"},
                            children=["Kinaadman Learning Dashboard"],
                        )
                    ],
                )
            ],
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
