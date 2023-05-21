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
mainColor = "#5b8dde"

# App Information
app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    title="Kinaadman Learning Dashboard",
)

# Datasets
studentData = pd.read_csv("studentData.csv")
studentData = studentData.set_index("Subjects")


# Visualization
studentPerformanceGraph = px.bar(
    studentData,
    x="Performance",
    y=studentData.index,
    labels={
        "Performance": "Subject Performance",
        "index": "Subjects",
    },
    orientation="h",
)
studentPerformanceGraph.update_layout(
    legend_bgcolor=mainColor,
    margin=dict(l=20, r=20, t=3, b=20),
)
subjectPerformance = {
    "bestSubject": studentData["Performance"].idxmax(),
    "bestSubjectGrade": studentData["Performance"].max(),
    "worstSubject": studentData["Performance"].idxmin(),
    "worstSubjectGrade": studentData["Performance"].min(),
}


# Dash Design
app.layout = html.Div(
    children=[
        # Navigation Bar
        html.Nav(
            className="navbar bg-body-tertiary rounded-bottom p-4",
            style={"background-color": mainColor},
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
                            children=["Kinaadman Learning Dashboard"],
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
                                    className="px-3 d-flex align-items-center",
                                    children=[
                                        html.Img(
                                            className="px-3",
                                            src="assets/user.svg",
                                            style={
                                                "height": "2.5em",
                                                "filter": "brightness(0) invert(1)",
                                            },
                                        ),
                                        dmc.Menu(
                                            [
                                                dmc.MenuTarget(
                                                    dmc.Button(
                                                        "Student #1",
                                                        style={
                                                            "background-color": "rgba(0, 0, 0, 0)",
                                                            "border": "2px solid white",
                                                            "font-family": "Roboto",
                                                            "font-weight": "500",
                                                            "font-size": "1em",
                                                        },
                                                    ),
                                                ),
                                                dmc.MenuDropdown(
                                                    [
                                                        dmc.MenuLabel("Account"),
                                                        dmc.MenuItem(
                                                            "Log-Out",
                                                            href="https://www.github.com/snehilvj",
                                                            icon=DashIconify(
                                                                icon="tabler:settings"
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
        # Dashboard Content
        # Grid
        html.Div(
            className="container-fluid",
            children=[
                # Headers
                html.Div(
                    className="row mt-5 mx-5 align-items-start justify-content-md-center ",
                    children=[
                        html.Div(
                            className="col-md-6",
                            children=[
                                html.Div(
                                    className="text-white p-2 text-center rounded mr-auto",
                                    children=["Student's Performance"],
                                    style={
                                        "background-color": mainColor,
                                        "font-family": "Roboto",
                                        "font-weight": "500",
                                        "font-size": "2em",
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            className="col-md-6 ms-md-auto",
                            children=[
                                html.Div(
                                    className="text-white p-2 text-center rounded mr-auto",
                                    children=["Analysis"],
                                    style={
                                        "background-color": mainColor,
                                        "font-family": "Roboto",
                                        "font-weight": "500",
                                        "font-size": "2em",
                                    },
                                ),
                            ],
                        ),
                    ],
                ),
                # Content
                html.Div(
                    className="row mt-3 mx-5 justify-content-md-center",
                    children=[
                        html.Div(
                            className="col-md-6",
                            children=[
                                dcc.Graph(
                                    figure=studentPerformanceGraph,
                                ),
                            ],
                        ),
                        html.Div(
                            className="col-md-6 ms-md-auto",
                            children=[
                                dmc.Accordion(
                                    className="text-white",
                                    children=[
                                        dmc.AccordionItem(
                                            [
                                                dmc.AccordionControl(
                                                    "Best Performing Subject"
                                                ),
                                                dmc.AccordionPanel(
                                                    "Subject: "
                                                    + subjectPerformance["bestSubject"]
                                                ),
                                                dmc.AccordionPanel(
                                                    "Subject: "
                                                    + str(
                                                        subjectPerformance[
                                                            "bestSubjectGrade"
                                                        ]
                                                    )
                                                ),
                                            ],
                                            value="bestPerformingSubject",
                                        ),
                                        dmc.AccordionItem(
                                            [
                                                dmc.AccordionControl(
                                                    "Worst Performing Subject"
                                                ),
                                                dmc.AccordionPanel(
                                                    "Subject: "
                                                    + subjectPerformance["worstSubject"]
                                                ),
                                                dmc.AccordionPanel(
                                                    "Subject: "
                                                    + str(
                                                        subjectPerformance[
                                                            "worstSubjectGrade"
                                                        ]
                                                    )
                                                ),
                                            ],
                                            value="worstPerformingSubject",
                                        ),
                                        dmc.AccordionItem(
                                            [
                                                dmc.AccordionControl("Reccomendation"),
                                                dmc.AccordionPanel("Reccomended"),
                                            ],
                                            value="recommendation",
                                        ),
                                    ],
                                    styles={
                                        "root": {
                                            "backgroundColor": dmc.theme.DEFAULT_COLORS[
                                                "gray"
                                            ][0],
                                            "borderRadius": 5,
                                        },
                                        "control": {
                                            "font-family": "Roboto",
                                            "font-weight": "500",
                                        },
                                        "item": {
                                            "backgroundColor": dmc.theme.DEFAULT_COLORS[
                                                "gray"
                                            ][0],
                                            "border": "1px solid transparent",
                                            "font-family": "Roboto",
                                            "font-weight": "300",
                                            "font-size": "1em",
                                            "position": "relative",
                                            "zIndex": 0,
                                            "transition": "transform 150ms ease",
                                            "&[data-active]": {
                                                "transform": "scale(1.03)",
                                                "backgroundColor": "white",
                                                "boxShadow": 5,
                                                "borderColor": dmc.theme.DEFAULT_COLORS[
                                                    "gray"
                                                ][2],
                                                "borderRadius": 5,
                                                "zIndex": 1,
                                            },
                                        },
                                        "chevron": {
                                            "&[data-rotate]": {
                                                "transform": "rotate(-90deg)",
                                            },
                                        },
                                    },
                                )
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="row mt-3 mx-5 justify-content-md-center", children=[]
                ),
            ],
        ),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
