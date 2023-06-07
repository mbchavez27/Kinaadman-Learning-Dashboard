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

# Datasets
studentData = pd.read_csv("studentData.csv")
studentData = studentData.set_index("Subjects")
currentStudent_dict = {"current_student": "mbchavez2@student.apc.edu.ph"}
studentList = pd.read_csv("studentList.csv")
studentList = studentList.set_index("Student_Email")


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
    margin=dict(l=20, r=20, t=3, b=20),
)
studentPerformanceGraph.update_layout(
    {"plot_bgcolor": "rgba(0,0,0,0)", "paper_bgcolor": "rgb(248, 248, 249)"}
)
studentPerformanceGraph.update_traces(marker_color=mainColors["burgandy"])

subjectPerformance = {
    "bestSubject": studentData["Performance"].idxmax(),
    "bestSubjectGrade": studentData["Performance"].max(),
    "worstSubject": studentData["Performance"].idxmin(),
    "worstSubjectGrade": studentData["Performance"].min(),
}


# Dashboard Content
layout = (
    html.Div(
        className="container-fluid",
        children=[
            # Student Name
            html.Div(
                className="row mt-4 mx-2 align-items-start justify-content-md-start ",
                children=[
                    html.Div(
                        className="col-md-3",
                        children=[
                            html.Div(
                                className="shadow-sm text-white p-2 text-left rounded mr-auto",
                                children=[
                                    html.P(
                                        className="px-3",
                                        children=[
                                            studentList.loc[
                                                currentStudent_dict["current_student"],
                                                "Student_Names",
                                            ]
                                        ],
                                        style={
                                            "font-family": "Roboto",
                                            "font-weight": "500",
                                            "font-size": "2em",
                                        },
                                    ),
                                    html.P(
                                        className="px-3",
                                        children=[
                                            studentList.loc[
                                                currentStudent_dict["current_student"],
                                                "Strand",
                                            ],
                                            " - ",
                                            studentList.loc[
                                                currentStudent_dict["current_student"],
                                                "Section",
                                            ],
                                        ],
                                        style={
                                            "font-family": "Roboto",
                                            "font-weight": "300",
                                            "font-size": "1.5em",
                                        },
                                    ),
                                ],
                                style={
                                    "background-color": mainColors["uclaBlue"],
                                },
                            ),
                        ],
                    ),
                    html.Div(
                        className="col-md-3",
                        children=[
                            html.Div(
                                children=[""],
                                style={
                                    "font-family": "Roboto",
                                    "font-weight": "300",
                                    "font-size": "2em",
                                },
                            ),
                        ],
                    ),
                ],
            ),
            # Headers
            html.Div(
                className="row mt-4 mx-5 align-items-start justify-content-md-center ",
                children=[
                    html.Div(
                        className="col-md-6",
                        children=[
                            html.Div(
                                className="shadow-sm text-white p-2 text-center rounded mr-auto",
                                children=["Student's Performance"],
                                style={
                                    "background-color": mainColors["uclaBlue"],
                                    "font-family": "Roboto",
                                    "font-weight": "500",
                                    "font-size": "1.5em",
                                },
                            ),
                        ],
                    ),
                    html.Div(
                        className="col-md-6 ms-md-auto",
                        children=[
                            html.Div(
                                className="shadow-sm text-white p-2 text-center rounded mr-auto",
                                children=["Analysis"],
                                style={
                                    "background-color": mainColors["uclaBlue"],
                                    "font-family": "Roboto",
                                    "font-weight": "500",
                                    "font-size": "1.5em",
                                },
                            ),
                        ],
                    ),
                ],
            ),
            # Content
            html.Div(
                className="row mb-2 mt-4 mx-5 justify-content-md-center",
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
                                        className="shadow-sm m-3",
                                        children=[
                                            dmc.AccordionControl(
                                                "Best Performing Subject",
                                                icon=DashIconify(icon="bi:award"),
                                            ),
                                            dmc.AccordionPanel(
                                                "Subject: "
                                                + subjectPerformance["bestSubject"]
                                            ),
                                            dmc.AccordionPanel(
                                                "Grades: "
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
                                        className="shadow-sm m-3",
                                        children=[
                                            dmc.AccordionControl(
                                                "Worst Performing Subject",
                                                icon=DashIconify(icon="bi:fire"),
                                            ),
                                            dmc.AccordionPanel(
                                                "Subject: "
                                                + subjectPerformance["worstSubject"]
                                            ),
                                            dmc.AccordionPanel(
                                                "Grades: "
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
                                        className="shadow-sm m-3",
                                        children=[
                                            dmc.AccordionControl(
                                                "Recommendation",
                                                icon=DashIconify(icon="bi:lightbulb"),
                                            ),
                                            dmc.AccordionPanel("Recommended"),
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
                                        "font-size": ".8em",
                                    },
                                    "item": {
                                        "backgroundColor": dmc.theme.DEFAULT_COLORS[
                                            "gray"
                                        ][0],
                                        "border": "1px solid transparent",
                                        "font-family": "Roboto",
                                        "font-weight": "300",
                                        "font-size": "1.5em",
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
        ],
    ),
)
