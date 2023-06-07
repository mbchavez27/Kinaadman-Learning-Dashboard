# Imports
from dash_iconify import DashIconify
from dash import Dash, html, dcc, callback, clientside_callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import matplotlib.pyplot as plt
from dash.dependencies import Input, Output, State

# Styles
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

# Designs
mainColors = {
    "oxfordBlue": "#011638",
    "uclaBlue": "#4F759B",
    "snow": "#FFFCFF",
    "burgandy": "#721121",
}

# Datasets
studentData = pd.read_csv("studentData.csv")
studentData = studentData.set_index("Subjects")


# Dashboard Content
layout = (
    html.Div(
        children=[
            dmc.Center(
                className="p-5",
                children=[
                    dmc.Card(
                        children=[
                            dmc.CardSection(
                                className="text-white pb-4 pt-3",
                                children=[
                                    dmc.Center(
                                        className="p-3",
                                        children=[
                                            html.Img(
                                                src="../assets/kldLogoWhite.png",
                                                height="80px",
                                            ),
                                        ],
                                    ),
                                    dmc.Center(
                                        className="p-1",
                                        children=["Kinaadman Learning Dashboard"],
                                        style={
                                            "font-family": "Roboto",
                                            "font-weight": "500",
                                            "font-size": "1.5em",
                                        },
                                    ),
                                    dmc.Center(
                                        className="p-1",
                                        children=["Change Student"],
                                        style={
                                            "font-family": "Roboto",
                                            "font-weight": "300",
                                            "font-size": "1em",
                                        },
                                    ),
                                ],
                                style={"background-color": mainColors["uclaBlue"]},
                            ),
                            html.Div(
                                className="pt-2",
                                children=[
                                    dmc.Center(
                                        className="p-3",
                                        children=[
                                            dmc.TextInput(
                                                label="Email:",
                                                id="email",
                                                name="email",
                                                style={
                                                    "width": 300,
                                                    "font-family": "Roboto",
                                                    "font-weight": "500",
                                                },
                                                placeholder="Your Email",
                                                icon=DashIconify(
                                                    icon="ic:round-alternate-email"
                                                ),
                                            ),
                                        ],
                                    ),
                                    dmc.Center(
                                        className="p-3",
                                        children=[
                                            dmc.PasswordInput(
                                                label="Password:",
                                                id="password",
                                                name="password",
                                                style={
                                                    "width": 300,
                                                    "font-family": "Roboto",
                                                    "font-weight": "500",
                                                },
                                                placeholder="Your password",
                                                icon=DashIconify(icon="bi:shield-lock"),
                                            ),
                                        ],
                                    ),
                                    dmc.Center(
                                        className="pb-2 pt-2",
                                        children=[
                                            dmc.Button(
                                                id="submit",
                                                n_clicks=0,
                                                children=["Change Student"],
                                                leftIcon=DashIconify(
                                                    icon="solar:user-check-rounded-broken"
                                                ),
                                                style={
                                                    "background-color": mainColors[
                                                        "uclaBlue"
                                                    ]
                                                },
                                            ),
                                        ],
                                    ),
                                    dmc.Center(
                                        className="p-1 text-danger",
                                        children=[],
                                        style={
                                            "font-family": "Roboto",
                                            "font-weight": "300",
                                            "font-size": "1em",
                                        },
                                    ),
                                    html.Div(id="output1"),
                                ],
                            ),
                        ],
                        withBorder=True,
                        shadow="sm",
                        radius="md",
                        style={"width": 500, "height": 520},
                    ),
                ],
            )
        ],
    ),
)


@app.callback(
    Output("output1", "children"),
    [Input("submit", "n_clicks")],
    State("email", "value"),
    State("password", "value"),
)
def update_output(n_clicks, email, password):
    return email
