# Imports
from dash_iconify import DashIconify
from dash import Dash, html, dcc
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

# Dashboard Content
layout = html.Div(
    children=[
        dmc.Center(
            className="mt-5 mb-5",
            style={
                "width": "100%",
                "font-family": "Roboto",
                "font-weight": "500",
                "font-size": "2em",
            },
            children=[
                html.Div(
                    style={
                        "background-color": mainColors["uclaBlue"],
                    },
                    className="text-white rounded shadow p-3",
                    children="Welcome to Kinaadman Learning Dashboard",
                )
            ],
        ),
        dmc.Center(
            className="mt-5 mb-5",
            style={
                "width": "100%",
                "font-family": "Roboto",
                "font-weight": "300",
                "font-size": "1.2em",
            },
            children=[
                html.Div(
                    style={"background-color": "#f8f9fa", "width": "50%"},
                    className="text-black text-center rounded shadow text-wrap p-3",
                    children=[
                        "The Kinaadman learning dashboard is a website that allows students to track academic progress and grades. It offers a consolidated platform for recording and assessing student performance, allowing for effective tracking of individual and class-wide improvement. The grade tracker includes features such as log-in, topic recommendations, data display, and progress reporting."
                    ],
                )
            ],
        ),
        dmc.Center(
            className="mt-5 mb-5",
            style={
                "width": "100%",
                "font-family": "Roboto",
                "font-weight": "500",
                "font-size": "1em",
            },
            children=[
                html.Div(
                    style={
                        "background-color": mainColors["burgandy"],
                        "color": "white",
                        "highlight": "none",
                    },
                    className="text-black text-center rounded shadow text-wrap p-3",
                    children=[
                        html.A(
                            style={
                                "color": "white",
                                "highlight": "none",
                                "text-decoration": "none",
                            },
                            children=["Go to the Dashboard"],
                            href="dashboard",
                        )
                    ],
                )
            ],
        ),
        # dmc.Center(
        #     className="mt-5 mb-5",
        #     style={
        #         "width": "100%",
        #         "font-family": "Roboto",
        #         "font-weight": "500",
        #         "font-size": "1em",
        #     },
        #     children=[
        #         html.Div(
        #             style={
        #                 "color": mainColors["burgandy"],
        #                 "highlight": "none",
        #             },
        #             className="text-black text-center rounded shadow text-wrap p-3",
        #             children=[
        #                 html.A(
        #                     style={
        #                         "color": mainColors["burgandy"],
        #                         # "highlight": "none",
        #                         # "text-decoration": "none",
        #                     },
        #                     children=["Log In"],
        #                     href="dashboard",
        #                 )
        #             ],
        #         )
        #     ],
        # ),
    ],
)
