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


# Navigation Bar
def navBar():
    layout = html.Div(
        html.Nav(
            className="navbar shadow bg-body-tertiary rounded-bottom p-2",
            style={"background-color": mainColors["oxfordBlue"]},
            children=[
                html.Div(
                    className="container-fluid",
                    children=[
                        # Title Text with Logo <- Left Side
                        html.Span(
                            className="navbar-brand mb-0 h1 text-white",
                            style={
                                "font-family": "Roboto",
                                "font-weight": "500",
                                "font-size": "1.5rem",
                            },
                            children=[
                                html.Img(
                                    src="../assets/kldLogoWhite.png", height="70px"
                                )
                            ],
                        ),
                        # Account Details <- Right Side
                        html.Div(
                            className="d-flex align-items-center text-white",
                            style={
                                "font-family": "Roboto",
                                "font-weight": "500",
                                "font-size": "1em",
                            },
                            # Student #
                            children=[
                                html.Span(
                                    className="px-3 pt-2 d-flex align-items-center",
                                    children=[
                                        dmc.Menu(
                                            [
                                                dmc.MenuTarget(
                                                    dmc.Button(
                                                        "Menu",
                                                        style={
                                                            "background-color": "rgba(0, 0, 0, 0)",
                                                            "border": "3px solid white",
                                                            "font-family": "Roboto",
                                                            "font-weight": "500",
                                                            "font-size": "1em",
                                                        },
                                                    ),
                                                ),
                                                dmc.MenuDropdown(
                                                    [
                                                        dmc.MenuLabel("Directory"),
                                                        dmc.MenuItem(
                                                            "Home",
                                                            href="/home",
                                                            icon=DashIconify(
                                                                icon="material-symbols:home"
                                                            ),
                                                            style={
                                                                "font-family": "Roboto",
                                                                "font-weight": "300",
                                                                "font-size": "1em",
                                                            },
                                                        ),
                                                        dmc.MenuItem(
                                                            "Dashboard",
                                                            href="/dashboard",
                                                            icon=DashIconify(
                                                                icon="material-symbols:empty-dashboard-outline"
                                                            ),
                                                            style={
                                                                "font-family": "Roboto",
                                                                "font-weight": "300",
                                                                "font-size": "1em",
                                                            },
                                                        ),
                                                        dmc.MenuItem(
                                                            "About Us",
                                                            href="/aboutUs",
                                                            icon=DashIconify(
                                                                icon="bi:globe-asia-australia"
                                                            ),
                                                            style={
                                                                "font-family": "Roboto",
                                                                "font-weight": "300",
                                                                "font-size": "1em",
                                                            },
                                                        ),
                                                        dmc.MenuItem(
                                                            "Support & Frequently Asked Questions",
                                                            href="/support",
                                                            icon=DashIconify(
                                                                icon="bi:patch-question"
                                                            ),
                                                            style={
                                                                "font-family": "Roboto",
                                                                "font-weight": "300",
                                                                "font-size": "1em",
                                                            },
                                                        ),
                                                        dmc.MenuItem(
                                                            "Change Student",
                                                            href="/changeStudent",
                                                            icon=DashIconify(
                                                                icon="material-symbols:account-circle-outline"
                                                            ),
                                                            style={
                                                                "font-family": "Roboto",
                                                                "font-weight": "300",
                                                                "font-size": "1em",
                                                            },
                                                        ),
                                                    ]
                                                ),
                                            ],
                                            trigger="hover",
                                        ),
                                    ],
                                    style={
                                        "font-size": "1em",
                                    },
                                ),
                            ],
                        ),
                    ],
                )
            ],
        ),
    )
    return layout
