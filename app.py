# Imports
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
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

# Image
userIcon = "Assets/User/person.png"

# Dash App Information
app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    title="Kinaadman Learning Dashboard",
)

# Dash Datasets
studentData = pd.read_csv("studentData.csv")
studentData.index = np.arange(1, len(studentData) + 1)

print(studentData)
# Dash Students
currentStudent = studentData.loc[1]


# Dash Design
app.layout = html.Div(
    children=[
        # Navigation Bar
        html.Nav(
            className="navbar bg-body-tertiary p-3",
            style={"background-color": "#4066a3"},
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
                            },
                            children=["KLD"],
                        ),
                        # Account Details <- Right Side
                        html.Div(
                            className="d-flex align-items-center text-white",
                            style={
                                "font-family": "Roboto",
                                "font-weight": "500",
                            },
                            # Student #
                            children=[
                                html.Span(
                                    className="px-3",
                                    id="currentStudent",
                                    children=[
                                        html.Img(src=userIcon),
                                        "Student #"
                                        + str(currentStudent["studentNumber"]),
                                    ],
                                ),
                                dbc.Button(
                                    "Change Student",
                                    id="open",
                                    n_clicks=0,
                                    outline=True,
                                    active=True,
                                    className="px-2 bg-transparent border-white text-white",
                                    style={
                                        "font-family": "Roboto",
                                        "font-weight": "300",
                                    },
                                ),
                                # Change Student Form
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader(
                                            dbc.ModalTitle("Change Student")
                                        ),
                                        dbc.ModalBody(
                                            children=[
                                                html.Div(
                                                    children=[
                                                        dbc.Label("Student ID"),
                                                        dbc.Input(
                                                            type="text",
                                                            id="inputStudentID",
                                                        ),
                                                    ]
                                                ),
                                            ]
                                        ),
                                        dbc.ModalFooter(
                                            children=[
                                                dbc.Button(
                                                    "Change",
                                                    id="changeStudentID",
                                                    className="ms-auto",
                                                    n_clicks=0,
                                                ),
                                            ]
                                        ),
                                    ],
                                    id="modal",
                                    is_open=False,
                                ),
                            ],
                        ),
                    ],
                )
            ],
        ),
    ],
)


@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("changeStudentID", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=True)
