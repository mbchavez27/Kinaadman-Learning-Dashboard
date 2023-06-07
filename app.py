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
    color="Performance",
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


# Dash App
app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    title="Kinaadman Learning Dashboard",
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    suppress_callback_exceptions=True,
)


if __name__ == "__main__":
    app.run_server(debug=True)
