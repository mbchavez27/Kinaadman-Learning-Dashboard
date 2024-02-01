# /bo /c/ Imports
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
from flask import redirect


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
    "green": "#1c7211",
}

# Datasets
studentList = pd.read_csv("studentList.csv")
studentList = studentList.set_index("Student_Email")
currentStudent_dict = {"current_student": "mbchavez2@student.apc.edu.ph"}
currentStudentInfo = {
    "currentStudentName": studentList.loc[
        currentStudent_dict["current_student"],
        "Student_Names",
    ],
    "currentStudentData": studentList.loc[
        currentStudent_dict["current_student"],
        "Student_Data",
    ],
}


studentDatas = {"studentData": pd.read_csv(currentStudentInfo["currentStudentData"])}
studentDatas["studentData"] = studentDatas["studentData"].set_index("Subjects")
subjects = studentDatas["studentData"].index.values
studentDatas["studentData"]["Status"] = [
    "Failed" if value < 75 else "Passed"
    for value in studentDatas["studentData"]["Performance"]
]
color_grades = {"Passed": mainColors["green"], "Failed": mainColors["burgandy"]}


# Visualization
studentPerformanceGraph = px.bar(
    studentDatas["studentData"],
    x="Performance",
    y=studentDatas["studentData"].index,
    labels={
        "Performance": "Grades",
        "index": "Subjects",
    },
    color=studentDatas["studentData"]["Status"],
    color_discrete_map=color_grades,
    orientation="h",
)
studentPerformanceGraph.update_layout(
    margin=dict(l=25, r=25, t=10, b=25),
    legend=dict(
        orientation="h",  # Set the orientation to horizontal
        yanchor="bottom",  # Anchor the legend to the bottom
        y=1.02,  # Adjust the y position
        xanchor="right",  # Anchor the legend to the right
        x=1,  # Adjust the x position
    ),
)
studentPerformanceGraph.update_layout(
    {
        "plot_bgcolor": "rgba(0,0,0,0)",
        "paper_bgcolor": "rgb(248, 248, 249)",
        "xaxis_range": [70, 100],
    }
)
# studentPerformanceGraph.update_traces(marker_color=studentDatas["studentData"]["Color"])


subjectPerformance = {
    "bestSubject": studentDatas["studentData"]["Performance"].idxmax(axis=0),
    "bestSubjectGrade": studentDatas["studentData"]["Performance"].max(axis=0),
    "worstSubject": studentDatas["studentData"]["Performance"].idxmin(axis=0),
    "worstSubjectGrade": studentDatas["studentData"]["Performance"].min(axis=0),
}

subjectRecommendation = pd.read_csv("subjectRecommendation.csv")

# Import App
from app import app

# Import Components
from components import navbar

# Get Navigation Bar
nav = navbar.navBar()


# Layout of the App
app.layout = html.Div(
    children=[
        html.Meta(
            name="viewport",
            content="width=device-width, initial-scale=1.0, maximum-scale=1.2, user-scalable=yes",
        ),
        html.Link(rel="icon", href="assets/kldLogoWhite.ico", type="image/x-icon"),
        dcc.Store(id="currentStudent"),
        dcc.Location(id="url", pathname="/changeStudent", refresh=True),
        nav,
        html.Div(id="page-content", children=[]),
    ],
)


# changeStudentLayout = (
#     html.Div(
#         children=[
#             dmc.Center(
#                 className="p-5",
#                 children=[
#                     dmc.Card(
#                         children=[
#                             dmc.CardSection(
#                                 className="text-white pb-4 pt-3",
#                                 children=[
#                                     dmc.Center(
#                                         className="p-3",
#                                         children=[
#                                             html.Img(
#                                                 src="../assets/kldLogoWhite.png",
#                                                 height="80px",
#                                             ),
#                                         ],
#                                     ),
#                                     dmc.Center(
#                                         className="p-1",
#                                         children=["Kinaadman Learning Dashboard"],
#                                         style={
#                                             "font-family": "Roboto",
#                                             "font-weight": "500",
#                                             "font-size": "1.5em",
#                                         },
#                                     ),
#                                     dmc.Center(
#                                         className="p-1",
#                                         children=["Change Student"],
#                                         style={
#                                             "font-family": "Roboto",
#                                             "font-weight": "300",
#                                             "font-size": "1em",
#                                         },
#                                     ),
#                                 ],
#                                 style={"background-color": mainColors["uclaBlue"]},
#                             ),
#                             html.Div(
#                                 className="pt-2",
#                                 children=[
#                                     dmc.Center(
#                                         className="p-3",
#                                         children=[
#                                             dmc.TextInput(
#                                                 label="Email:",
#                                                 id="email",
#                                                 name="email",
#                                                 style={
#                                                     "width": 300,
#                                                     "font-family": "Roboto",
#                                                     "font-weight": "500",
#                                                 },
#                                                 placeholder="Your Email",
#                                                 icon=DashIconify(
#                                                     icon="ic:round-alternate-email"
#                                                 ),
#                                             ),
#                                         ],
#                                     ),
#                                     dmc.Center(
#                                         className="p-3",
#                                         children=[
#                                             dmc.PasswordInput(
#                                                 label="Password:",
#                                                 id="password",
#                                                 name="password",
#                                                 style={
#                                                     "width": 300,
#                                                     "font-family": "Roboto",
#                                                     "font-weight": "500",
#                                                 },
#                                                 placeholder="Your password",
#                                                 icon=DashIconify(icon="bi:shield-lock"),
#                                             ),
#                                         ],
#                                     ),
#                                     dmc.Center(
#                                         className="pb-2 pt-2",
#                                         children=[
#                                             dmc.Button(
#                                                 id="submit",
#                                                 n_clicks=0,
#                                                 children=["Change Student"],
#                                                 leftIcon=DashIconify(
#                                                     icon="solar:user-check-rounded-broken"
#                                                 ),
#                                                 style={
#                                                     "background-color": mainColors[
#                                                         "uclaBlue"
#                                                     ]
#                                                 },
#                                             ),
#                                         ],
#                                     ),
#                                     dmc.Center(
#                                         className="p-1 text-danger",
#                                         children=[html.Div(id="output1")],
#                                         style={
#                                             "font-family": "Roboto",
#                                             "font-weight": "300",
#                                             "font-size": "1em",
#                                         },
#                                     ),
#                                 ],
#                             ),
#                         ],
#                         withBorder=True,
#                         shadow="sm",
#                         radius="md",
#                         style={"width": 500, "height": 520},
#                     ),
#                 ],
#             )
#         ],
#     ),
# )


# Dashboard Content
# homeLayout = html.Div(
#     children=[
#         dmc.Center(
#             className="mt-5 mb-5",
#             style={
#                 "width": "100%",
#                 "font-family": "Roboto",
#                 "font-weight": "500",
#                 "font-size": "2em",
#             },
#             children=[
#                 html.Div(
#                     style={
#                         "background-color": mainColors["uclaBlue"],
#                     },
#                     className="text-white rounded shadow p-3",
#                     children="Welcome to Kinaadman Learning Dashboard",
#                 )
#             ],
#         ),
#         dmc.Center(
#             className="mt-5 mb-5",
#             style={
#                 "width": "100%",
#                 "font-family": "Roboto",
#                 "font-weight": "300",
#                 "font-size": "1.2em",
#             },
#             children=[
#                 html.Div(
#                     style={"background-color": "#f8f9fa", "width": "50%"},
#                     className="text-black text-center rounded shadow text-wrap p-3",
#                     children=[
#                         "The Kinaadman learning dashboard is a website that allows students to track academic progress and grades. It offers a consolidated platform for recording and assessing student performance, allowing for effective tracking of individual and class-wide improvement. The grade tracker includes features such as log-in, topic recommendations, data display, and progress reporting."
#                     ],
#                 )
#             ],
#         ),
#     ]
# )


# dashboardLayout = (
#     html.Div(
#         className="container-fluid",
#         children=[
#             # Student Name
#             html.Div(
#                 className="row mt-4 mx-2 align-items-start justify-content-md-start ",
#                 children=[
#                     html.Div(
#                         className="col-md-4",
#                         children=[
#                             html.Div(
#                                 className="shadow-sm text-white p-2 text-left rounded mr-auto",
#                                 children=[
#                                     html.P(
#                                         className="px-3",
#                                         children=[
#                                             studentList.loc[
#                                                 currentStudent_dict["current_student"],
#                                                 "Student_Names",
#                                             ],
#                                         ],
#                                         style={
#                                             "font-family": "Roboto",
#                                             "font-weight": "500",
#                                             "font-size": "2em",
#                                         },
#                                     ),
#                                     html.P(
#                                         className="px-3",
#                                         children=[
#                                             studentList.loc[
#                                                 currentStudent_dict["current_student"],
#                                                 "Strand",
#                                             ],
#                                             " - ",
#                                             studentList.loc[
#                                                 currentStudent_dict["current_student"],
#                                                 "Section",
#                                             ],
#                                         ],
#                                         style={
#                                             "font-family": "Roboto",
#                                             "font-weight": "300",
#                                             "font-size": "1.5em",
#                                         },
#                                     ),
#                                 ],
#                                 style={
#                                     "background-color": mainColors["uclaBlue"],
#                                 },
#                             ),
#                         ],
#                     ),
#                     html.Div(
#                         className="col-md-3",
#                         children=[
#                             html.Div(
#                                 children=[""],
#                                 style={
#                                     "font-family": "Roboto",
#                                     "font-weight": "300",
#                                     "font-size": "2em",
#                                 },
#                             ),
#                         ],
#                     ),
#                 ],
#             ),
#             # Headers
#             html.Div(
#                 className="row mt-4 mx-5 align-items-start justify-content-md-center ",
#                 children=[
#                     html.Div(
#                         className="col-md-6",
#                         children=[
#                             html.Div(
#                                 className="shadow-sm text-white p-2 text-center rounded mr-auto",
#                                 children=["Student's Performance"],
#                                 style={
#                                     "background-color": mainColors["uclaBlue"],
#                                     "font-family": "Roboto",
#                                     "font-weight": "500",
#                                     "font-size": "1.5em",
#                                 },
#                             ),
#                         ],
#                     ),
#                     html.Div(
#                         className="col-md-6 ms-md-auto",
#                         children=[
#                             html.Div(
#                                 className="shadow-sm text-white p-2 text-center rounded mr-auto",
#                                 children=["Analysis"],
#                                 style={
#                                     "background-color": mainColors["uclaBlue"],
#                                     "font-family": "Roboto",
#                                     "font-weight": "500",
#                                     "font-size": "1.5em",
#                                 },
#                             ),
#                         ],
#                     ),
#                 ],
#             ),
#             # Content
#             html.Div(
#                 className="row mb-2 mt-2 mx-5 justify-content-md-center",
#                 children=[
#                     html.Div(
#                         className="col-md-6 mb-4",
#                         children=[
#                             dmc.Tabs(
#                                 [
#                                     dmc.TabsList(
#                                         [
#                                             dmc.Tab(
#                                                 "Graph View",
#                                                 value="graph",
#                                                 style={
#                                                     "font-family": "Roboto",
#                                                     "font-weight": "400",
#                                                     "font-size": "1em",
#                                                 },
#                                             ),
#                                             dmc.Tab(
#                                                 "Numerical View",
#                                                 value="number",
#                                                 style={
#                                                     "font-family": "Roboto",
#                                                     "font-weight": "400",
#                                                     "font-size": "1em",
#                                                 },
#                                             ),
#                                         ]
#                                     ),
#                                     dmc.TabsPanel(
#                                         className="mt-3",
#                                         children=[
#                                             dcc.Graph(
#                                                 figure=studentPerformanceGraph,
#                                             ),
#                                         ],
#                                         value="graph",
#                                     ),
#                                     dmc.TabsPanel(
#                                         className="mt-3",
#                                         children=[
#                                             dmc.Accordion(
#                                                 className="text-white",
#                                                 children=[
#                                                     dmc.AccordionItem(
#                                                         className="shadow-sm",
#                                                         children=[
#                                                             dmc.AccordionControl(
#                                                                 studentDatas[
#                                                                     "studentData"
#                                                                 ]
#                                                                 .loc[subjects[0]]
#                                                                 .name,
#                                                             ),
#                                                             dmc.AccordionPanel(
#                                                                 "Grades: "
#                                                                 + str(
#                                                                     studentDatas[
#                                                                         "studentData"
#                                                                     ].loc[
#                                                                         subjects[0],
#                                                                         "Performance",
#                                                                     ]
#                                                                 ),
#                                                             ),
#                                                             dmc.AccordionPanel(
#                                                                 "Status: "
#                                                                 + str(
#                                                                     studentDatas[
#                                                                         "studentData"
#                                                                     ].loc[
#                                                                         subjects[0],
#                                                                         "Status",
#                                                                     ]
#                                                                 ),
#                                                             ),
#                                                         ],
#                                                         value="subject0",
#                                                     ),
#                                                     dmc.AccordionItem(
#                                                         className="shadow-sm",
#                                                         children=[
#                                                             dmc.AccordionControl(
#                                                                 studentDatas[
#                                                                     "studentData"
#                                                                 ]
#                                                                 .loc[subjects[1],]
#                                                                 .name,
#                                                             ),
#                                                             dmc.AccordionPanel(
#                                                                 "Grades: "
#                                                                 + str(
#                                                                     studentDatas[
#                                                                         "studentData"
#                                                                     ].loc[
#                                                                         subjects[1],
#                                                                         "Performance",
#                                                                     ]
#                                                                 ),
#                                                             ),
#                                                             dmc.AccordionPanel(
#                                                                 "Status: "
#                                                                 + str(
#                                                                     studentDatas[
#                                                                         "studentData"
#                                                                     ].loc[
#                                                                         subjects[1],
#                                                                         "Status",
#                                                                     ]
#                                                                 ),
#                                                             ),
#                                                         ],
#                                                         value="subject1",
#                                                     ),
#                                                     dmc.AccordionItem(
#                                                         className="shadow-sm",
#                                                         children=[
#                                                             dmc.AccordionControl(
#                                                                 studentDatas[
#                                                                     "studentData"
#                                                                 ]
#                                                                 .loc[subjects[2],]
#                                                                 .name,
#                                                             ),
#                                                             dmc.AccordionPanel(
#                                                                 "Grades: "
#                                                                 + str(
#                                                                     studentDatas[
#                                                                         "studentData"
#                                                                     ].loc[
#                                                                         subjects[2],
#                                                                         "Performance",
#                                                                     ]
#                                                                 ),
#                                                             ),
#                                                             dmc.AccordionPanel(
#                                                                 "Status: "
#                                                                 + str(
#                                                                     studentDatas[
#                                                                         "studentData"
#                                                                     ].loc[
#                                                                         subjects[2],
#                                                                         "Status",
#                                                                     ]
#                                                                 ),
#                                                             ),
#                                                         ],
#                                                         value="subject2",
#                                                     ),
#                                                     dmc.AccordionItem(
#                                                         className="shadow-sm",
#                                                         children=[
#                                                             dmc.AccordionControl(
#                                                                 studentDatas[
#                                                                     "studentData"
#                                                                 ]
#                                                                 .loc[subjects[3],]
#                                                                 .name,
#                                                             ),
#                                                             dmc.AccordionPanel(
#                                                                 "Grades: "
#                                                                 + str(
#                                                                     studentDatas[
#                                                                         "studentData"
#                                                                     ].loc[
#                                                                         subjects[3],
#                                                                         "Performance",
#                                                                     ]
#                                                                 ),
#                                                             ),
#                                                             dmc.AccordionPanel(
#                                                                 "Status: "
#                                                                 + str(
#                                                                     studentDatas[
#                                                                         "studentData"
#                                                                     ].loc[
#                                                                         subjects[3],
#                                                                         "Status",
#                                                                     ]
#                                                                 ),
#                                                             ),
#                                                         ],
#                                                         value="subject3",
#                                                     ),
#                                                     dmc.AccordionItem(
#                                                         className="shadow-sm",
#                                                         children=[
#                                                             dmc.AccordionControl(
#                                                                 studentDatas[
#                                                                     "studentData"
#                                                                 ]
#                                                                 .loc[subjects[4],]
#                                                                 .name,
#                                                             ),
#                                                             dmc.AccordionPanel(
#                                                                 "Status: "
#                                                                 + str(
#                                                                     studentDatas[
#                                                                         "studentData"
#                                                                     ].loc[
#                                                                         subjects[4],
#                                                                         "Performance",
#                                                                     ]
#                                                                 ),
#                                                             ),
#                                                             dmc.AccordionPanel(
#                                                                 "Grades: "
#                                                                 + str(
#                                                                     studentDatas[
#                                                                         "studentData"
#                                                                     ].loc[
#                                                                         subjects[4],
#                                                                         "Status",
#                                                                     ]
#                                                                 ),
#                                                             ),
#                                                         ],
#                                                         value="subject4",
#                                                     ),
#                                                 ],
#                                                 styles={
#                                                     "root": {
#                                                         "backgroundColor": dmc.theme.DEFAULT_COLORS[
#                                                             "gray"
#                                                         ][
#                                                             0
#                                                         ],
#                                                         "borderRadius": 5,
#                                                     },
#                                                     "control": {
#                                                         "font-family": "Roboto",
#                                                         "font-weight": "300",
#                                                         "font-size": "1em",
#                                                     },
#                                                     "item": {
#                                                         "backgroundColor": dmc.theme.DEFAULT_COLORS[
#                                                             "gray"
#                                                         ][
#                                                             0
#                                                         ],
#                                                         "border": "1px solid transparent",
#                                                         "font-family": "Roboto",
#                                                         "font-weight": "300",
#                                                         "font-size": "1em",
#                                                         "position": "relative",
#                                                         "zIndex": 0,
#                                                         "transition": "transform 150ms ease",
#                                                         "&[data-active]": {
#                                                             "transform": "scale(1.03)",
#                                                             "backgroundColor": "white",
#                                                             "boxShadow": 5,
#                                                             "borderColor": dmc.theme.DEFAULT_COLORS[
#                                                                 "gray"
#                                                             ][
#                                                                 2
#                                                             ],
#                                                             "borderRadius": 5,
#                                                             "zIndex": 1,
#                                                         },
#                                                     },
#                                                     "chevron": {
#                                                         "&[data-rotate]": {
#                                                             "transform": "rotate(-90deg)",
#                                                         },
#                                                     },
#                                                 },
#                                             )
#                                         ],
#                                         value="number",
#                                     ),
#                                 ],
#                                 value="graph",
#                                 color=mainColors["burgandy"],
#                                 orientation="horizontal",
#                             ),
#                         ],
#                     ),
#                     html.Div(
#                         className="col-md-6 ms-md-auto",
#                         children=[
#                             dmc.Accordion(
#                                 className="text-white",
#                                 children=[
#                                     dmc.AccordionItem(
#                                         className="shadow-sm m-3",
#                                         children=[
#                                             dmc.AccordionControl(
#                                                 "Best Performing Subject",
#                                                 icon=DashIconify(icon="bi:award"),
#                                             ),
#                                             dmc.AccordionPanel(
#                                                 "Subject: "
#                                                 + str(subjectPerformance["bestSubject"])
#                                             ),
#                                             dmc.AccordionPanel(
#                                                 "Grades: "
#                                                 + str(
#                                                     subjectPerformance[
#                                                         "bestSubjectGrade"
#                                                     ]
#                                                 )
#                                             ),
#                                         ],
#                                         value="bestPerformingSubject",
#                                     ),
#                                     dmc.AccordionItem(
#                                         className="shadow-sm m-3",
#                                         children=[
#                                             dmc.AccordionControl(
#                                                 "Worst Performing Subject",
#                                                 icon=DashIconify(icon="bi:fire"),
#                                             ),
#                                             dmc.AccordionPanel(
#                                                 "Subject: "
#                                                 + str(
#                                                     subjectPerformance["worstSubject"]
#                                                 )
#                                             ),
#                                             dmc.AccordionPanel(
#                                                 "Grades: "
#                                                 + str(
#                                                     subjectPerformance[
#                                                         "worstSubjectGrade"
#                                                     ]
#                                                 )
#                                             ),
#                                         ],
#                                         value="worstPerformingSubject",
#                                     ),
#                                     dmc.AccordionItem(
#                                         className="shadow-sm m-3",
#                                         children=[
#                                             dmc.AccordionControl(
#                                                 "Recommendation",
#                                                 icon=DashIconify(icon="bi:lightbulb"),
#                                             ),
#                                             dmc.AccordionPanel(
#                                                 "Books to Study for "
#                                                 + str(
#                                                     subjectPerformance["worstSubject"]
#                                                 )
#                                                 + ":"
#                                             ),
#                                             dmc.AccordionPanel(
#                                                 subjectRecommendation.loc[
#                                                     0,
#                                                     subjectPerformance["worstSubject"],
#                                                 ]
#                                             ),
#                                             dmc.AccordionPanel(
#                                                 subjectRecommendation.loc[
#                                                     1,
#                                                     subjectPerformance["worstSubject"],
#                                                 ]
#                                             ),
#                                             dmc.AccordionPanel(
#                                                 subjectRecommendation.loc[
#                                                     2,
#                                                     subjectPerformance["worstSubject"],
#                                                 ]
#                                             ),
#                                         ],
#                                         style={"font-size": "0,8em"},
#                                         value="recommendation",
#                                     ),
#                                 ],
#                                 styles={
#                                     "root": {
#                                         "backgroundColor": dmc.theme.DEFAULT_COLORS[
#                                             "gray"
#                                         ][0],
#                                         "borderRadius": 5,
#                                     },
#                                     "control": {
#                                         "font-family": "Roboto",
#                                         "font-weight": "500",
#                                         "font-size": ".8em",
#                                     },
#                                     "item": {
#                                         "backgroundColor": dmc.theme.DEFAULT_COLORS[
#                                             "gray"
#                                         ][0],
#                                         "border": "1px solid transparent",
#                                         "font-family": "Roboto",
#                                         "font-weight": "300",
#                                         "font-size": "1.5em",
#                                         "position": "relative",
#                                         "zIndex": 0,
#                                         "transition": "transform 150ms ease",
#                                         "&[data-active]": {
#                                             "transform": "scale(1.03)",
#                                             "backgroundColor": "white",
#                                             "boxShadow": 5,
#                                             "borderColor": dmc.theme.DEFAULT_COLORS[
#                                                 "gray"
#                                             ][2],
#                                             "borderRadius": 5,
#                                             "zIndex": 1,
#                                         },
#                                     },
#                                     "chevron": {
#                                         "&[data-rotate]": {
#                                             "transform": "rotate(-90deg)",
#                                         },
#                                     },
#                                 },
#                             )
#                         ],
#                     ),
#                 ],
#             ),
#         ],
#     ),
# )

# aboutUsLayout = html.Div(
#     children=[
#         dmc.Center(
#             className="mt-5 mb-5",
#             style={
#                 "width": "100%",
#                 "font-family": "Roboto",
#                 "font-weight": "500",
#                 "font-size": "1.5em",
#             },
#             children=[
#                 html.Div(
#                     style={
#                         "background-color": mainColors["uclaBlue"],
#                     },
#                     className="text-white rounded shadow p-3",
#                     children="About Us",
#                 )
#             ],
#         ),
#         dmc.Grid(
#             className="text-center m-5",
#             children=[
#                 dmc.Col(
#                     html.Div(
#                         dmc.Card(
#                             children=[
#                                 dmc.CardSection(
#                                     dmc.Image(
#                                         src="../assets/max.jpeg",
#                                         height=160,
#                                     )
#                                 ),
#                                 dmc.Group(
#                                     [
#                                         dmc.Text("Max Benedict Chavez", weight=500),
#                                         dmc.Badge(
#                                             "Lead Developer",
#                                             color="red",
#                                             variant="light",
#                                         ),
#                                     ],
#                                     position="apart",
#                                     mt="md",
#                                     mb="xs",
#                                 ),
#                                 dmc.Text(
#                                     "The Programmer and the Project Manager of the Team",
#                                     size="sm",
#                                     color="dimmed",
#                                 ),
#                             ],
#                             withBorder=True,
#                             shadow="sm",
#                             radius="md",
#                             style={"width": 350},
#                         )
#                     ),
#                     span=4,
#                 ),
#                 dmc.Col(
#                     html.Div(
#                         dmc.Card(
#                             children=[
#                                 dmc.CardSection(
#                                     dmc.Image(
#                                         src="../assets/Jasper.jpg",
#                                         height=160,
#                                     )
#                                 ),
#                                 dmc.Group(
#                                     [
#                                         dmc.Text("Jasper Valdez", weight=500),
#                                         dmc.Badge(
#                                             "Lead Documentation",
#                                             color="red",
#                                             variant="light",
#                                         ),
#                                     ],
#                                     position="apart",
#                                     mt="md",
#                                     mb="xs",
#                                 ),
#                                 dmc.Text(
#                                     "Did the Documentation of the Team and Designed the Website",
#                                     size="sm",
#                                     color="dimmed",
#                                 ),
#                             ],
#                             withBorder=True,
#                             shadow="sm",
#                             radius="md",
#                             style={"width": 350},
#                         )
#                     ),
#                     span=4,
#                 ),
#                 dmc.Col(
#                     html.Div(
#                         dmc.Card(
#                             children=[
#                                 dmc.CardSection(
#                                     dmc.Image(
#                                         src="../assets/Shan.jpg",
#                                         height=160,
#                                     )
#                                 ),
#                                 dmc.Group(
#                                     [
#                                         dmc.Text("Shanteiy Camama", weight=500),
#                                         dmc.Badge(
#                                             "Lead Designer",
#                                             color="red",
#                                             variant="light",
#                                         ),
#                                     ],
#                                     position="apart",
#                                     mt="md",
#                                     mb="xs",
#                                 ),
#                                 dmc.Text(
#                                     "Designed the Majority of the Website",
#                                     size="sm",
#                                     color="dimmed",
#                                 ),
#                             ],
#                             withBorder=True,
#                             shadow="sm",
#                             radius="md",
#                             style={"width": 350},
#                         )
#                     ),
#                     span=4,
#                 ),
#             ],
#             gutter="xl",
#         ),
#     ]
# )

# supportLayout = html.Div(
#     children=[
#         dmc.Center(
#             className="mt-5 mb-5",
#             style={
#                 "width": "100%",
#                 "font-family": "Roboto",
#                 "font-weight": "500",
#                 "font-size": "1.5em",
#             },
#             children=[
#                 html.Div(
#                     style={
#                         "background-color": mainColors["uclaBlue"],
#                     },
#                     className="text-white rounded shadow p-3",
#                     children="Support and Frequently Asked Questions",
#                 )
#             ],
#         ),
#         dmc.Center(
#             dmc.Accordion(
#                 value="flexibility",
#                 children=[
#                     dmc.AccordionItem(
#                         [
#                             dmc.AccordionControl(
#                                 "Where can I access the Recommended Topics?"
#                             ),
#                             dmc.AccordionPanel(
#                                 "You can find your recommended topics in the right part of the dashboard"
#                             ),
#                         ],
#                         value="customization",
#                     ),
#                     dmc.AccordionItem(
#                         [
#                             dmc.AccordionControl(
#                                 "Do you need to have an account to access the dashboard"
#                             ),
#                             dmc.AccordionPanel(
#                                 "You need to have an account to acccess the dashboard"
#                             ),
#                         ],
#                         value="flexibility",
#                     ),
#                     dmc.AccordionItem(
#                         [
#                             dmc.AccordionControl(
#                                 "What type of account can I use to access the dashboard"
#                             ),
#                             dmc.AccordionPanel(
#                                 "You can use the accounts that your school gives to you to access the dashboard"
#                             ),
#                         ],
#                         value="ring",
#                     ),
#                 ],
#                 styles={
#                     "root": {
#                         "backgroundColor": dmc.theme.DEFAULT_COLORS["gray"][0],
#                         "borderRadius": 5,
#                     },
#                     "control": {
#                         "font-family": "Roboto",
#                         "font-weight": "500",
#                         "font-size": "1em",
#                     },
#                     "item": {
#                         "backgroundColor": dmc.theme.DEFAULT_COLORS["gray"][0],
#                         "border": "1px solid transparent",
#                         "position": "relative",
#                         "zIndex": 0,
#                         "transition": "transform 150ms ease",
#                         "&[data-active]": {
#                             "transform": "scale(1.03)",
#                             "backgroundColor": "white",
#                             "boxShadow": 5,
#                             "borderColor": dmc.theme.DEFAULT_COLORS["gray"][2],
#                             "borderRadius": 5,
#                             "zIndex": 1,
#                         },
#                     },
#                     "chevron": {
#                         "&[data-rotate]": {
#                             "transform": "rotate(-90deg)",
#                         },
#                     },
#                 },
#             )
#         ),
#     ]
# )


def generateHomeLayout():
    homeLayout = html.Div(
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
        ]
    )

    return homeLayout


def generateChangeStudentLayout():
    changeStudentLayout = (
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
                                                    icon=DashIconify(
                                                        icon="bi:shield-lock"
                                                    ),
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
                                            children=[html.Div(id="output1")],
                                            style={
                                                "font-family": "Roboto",
                                                "font-weight": "300",
                                                "font-size": "1em",
                                            },
                                        ),
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
    return changeStudentLayout


def generateDashboardLayout():
    # Visualization
    studentPerformanceGraph = px.bar(
        studentDatas["studentData"],
        x="Performance",
        y=studentDatas["studentData"].index,
        labels={
            "Performance": "Grades",
            "index": "Subjects",
        },
        color=studentDatas["studentData"]["Status"],
        color_discrete_map=color_grades,
        orientation="h",
    )
    studentPerformanceGraph.update_layout(
        barmode=None,
        margin=dict(l=25, r=25, t=10, b=25),
        legend=dict(
            orientation="h",  # Set the orientation to horizontal
            yanchor="bottom",  # Anchor the legend to the bottom
            y=1.02,  # Adjust the y position
            xanchor="right",  # Anchor the legend to the right
            x=1,  # Adjust the x position
        ),
    )
    studentPerformanceGraph.update_layout(
        {
            "plot_bgcolor": "rgba(0,0,0,0)",
            "paper_bgcolor": "rgb(248, 248, 249)",
            "xaxis_range": [70, 100],
        }
    )
    # studentPerformanceGraph.update_traces(marker_color=studentDatas["studentData"]["Color"])

    subjectPerformance = {
        "bestSubject": studentDatas["studentData"]["Performance"].idxmax(axis=0),
        "bestSubjectGrade": studentDatas["studentData"]["Performance"].max(axis=0),
        "worstSubject": studentDatas["studentData"]["Performance"].idxmin(axis=0),
        "worstSubjectGrade": studentDatas["studentData"]["Performance"].min(axis=0),
    }

    subjectRecommendation = pd.read_csv("subjectRecommendation.csv")

    dashboardLayout = (
        html.Div(
            className="container-fluid",
            children=[
                # Student Name
                html.Div(
                    className="row mt-4 mx-2 align-items-start justify-content-md-start ",
                    children=[
                        html.Div(
                            className="col-md-4",
                            children=[
                                html.Div(
                                    className="shadow-sm text-white p-2 text-left rounded mr-auto",
                                    children=[
                                        html.P(
                                            className="px-3",
                                            children=[
                                                studentList.loc[
                                                    currentStudent_dict[
                                                        "current_student"
                                                    ],
                                                    "Student_Names",
                                                ],
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
                                                    currentStudent_dict[
                                                        "current_student"
                                                    ],
                                                    "Strand",
                                                ],
                                                " - ",
                                                studentList.loc[
                                                    currentStudent_dict[
                                                        "current_student"
                                                    ],
                                                    "Section",
                                                ],
                                                " - Term #",
                                                studentList.loc[
                                                    currentStudent_dict[
                                                        "current_student"
                                                    ],
                                                    "Term",
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
                    className="row mb-2 mt-2 mx-5 justify-content-md-center",
                    children=[
                        html.Div(
                            className="col-md-6 mb-4",
                            children=[
                                dmc.Tabs(
                                    [
                                        dmc.TabsList(
                                            [
                                                dmc.Tab(
                                                    "Graph View",
                                                    value="graph",
                                                    style={
                                                        "font-family": "Roboto",
                                                        "font-weight": "400",
                                                        "font-size": "1em",
                                                    },
                                                ),
                                                dmc.Tab(
                                                    "Numerical View",
                                                    value="number",
                                                    style={
                                                        "font-family": "Roboto",
                                                        "font-weight": "400",
                                                        "font-size": "1em",
                                                    },
                                                ),
                                            ]
                                        ),
                                        dmc.TabsPanel(
                                            className="mt-3",
                                            children=[
                                                dcc.Graph(
                                                    figure=studentPerformanceGraph,
                                                ),
                                            ],
                                            value="graph",
                                        ),
                                        dmc.TabsPanel(
                                            className="mt-3",
                                            children=[
                                                dmc.Accordion(
                                                    className="text-white",
                                                    children=[
                                                        dmc.AccordionItem(
                                                            className="shadow-sm",
                                                            children=[
                                                                dmc.AccordionControl(
                                                                    studentDatas[
                                                                        "studentData"
                                                                    ]
                                                                    .loc[subjects[0]]
                                                                    .name,
                                                                ),
                                                                dmc.AccordionPanel(
                                                                    "Grades: "
                                                                    + str(
                                                                        studentDatas[
                                                                            "studentData"
                                                                        ].loc[
                                                                            subjects[0],
                                                                            "Performance",
                                                                        ]
                                                                    ),
                                                                ),
                                                                dmc.AccordionPanel(
                                                                    "Status: "
                                                                    + str(
                                                                        studentDatas[
                                                                            "studentData"
                                                                        ].loc[
                                                                            subjects[0],
                                                                            "Status",
                                                                        ]
                                                                    ),
                                                                ),
                                                            ],
                                                            value="subject0",
                                                        ),
                                                        dmc.AccordionItem(
                                                            className="shadow-sm",
                                                            children=[
                                                                dmc.AccordionControl(
                                                                    studentDatas[
                                                                        "studentData"
                                                                    ]
                                                                    .loc[subjects[1],]
                                                                    .name,
                                                                ),
                                                                dmc.AccordionPanel(
                                                                    "Grades: "
                                                                    + str(
                                                                        studentDatas[
                                                                            "studentData"
                                                                        ].loc[
                                                                            subjects[1],
                                                                            "Performance",
                                                                        ]
                                                                    ),
                                                                ),
                                                                dmc.AccordionPanel(
                                                                    "Status: "
                                                                    + str(
                                                                        studentDatas[
                                                                            "studentData"
                                                                        ].loc[
                                                                            subjects[1],
                                                                            "Status",
                                                                        ]
                                                                    ),
                                                                ),
                                                            ],
                                                            value="subject1",
                                                        ),
                                                        dmc.AccordionItem(
                                                            className="shadow-sm",
                                                            children=[
                                                                dmc.AccordionControl(
                                                                    studentDatas[
                                                                        "studentData"
                                                                    ]
                                                                    .loc[subjects[2],]
                                                                    .name,
                                                                ),
                                                                dmc.AccordionPanel(
                                                                    "Grades: "
                                                                    + str(
                                                                        studentDatas[
                                                                            "studentData"
                                                                        ].loc[
                                                                            subjects[2],
                                                                            "Performance",
                                                                        ]
                                                                    ),
                                                                ),
                                                                dmc.AccordionPanel(
                                                                    "Status: "
                                                                    + str(
                                                                        studentDatas[
                                                                            "studentData"
                                                                        ].loc[
                                                                            subjects[2],
                                                                            "Status",
                                                                        ]
                                                                    ),
                                                                ),
                                                            ],
                                                            value="subject2",
                                                        ),
                                                        dmc.AccordionItem(
                                                            className="shadow-sm",
                                                            children=[
                                                                dmc.AccordionControl(
                                                                    studentDatas[
                                                                        "studentData"
                                                                    ]
                                                                    .loc[subjects[3],]
                                                                    .name,
                                                                ),
                                                                dmc.AccordionPanel(
                                                                    "Grades: "
                                                                    + str(
                                                                        studentDatas[
                                                                            "studentData"
                                                                        ].loc[
                                                                            subjects[3],
                                                                            "Performance",
                                                                        ]
                                                                    ),
                                                                ),
                                                                dmc.AccordionPanel(
                                                                    "Status: "
                                                                    + str(
                                                                        studentDatas[
                                                                            "studentData"
                                                                        ].loc[
                                                                            subjects[3],
                                                                            "Status",
                                                                        ]
                                                                    ),
                                                                ),
                                                            ],
                                                            value="subject3",
                                                        ),
                                                        dmc.AccordionItem(
                                                            className="shadow-sm",
                                                            children=[
                                                                dmc.AccordionControl(
                                                                    studentDatas[
                                                                        "studentData"
                                                                    ]
                                                                    .loc[subjects[4],]
                                                                    .name,
                                                                ),
                                                                dmc.AccordionPanel(
                                                                    "Status: "
                                                                    + str(
                                                                        studentDatas[
                                                                            "studentData"
                                                                        ].loc[
                                                                            subjects[4],
                                                                            "Performance",
                                                                        ]
                                                                    ),
                                                                ),
                                                                dmc.AccordionPanel(
                                                                    "Grades: "
                                                                    + str(
                                                                        studentDatas[
                                                                            "studentData"
                                                                        ].loc[
                                                                            subjects[4],
                                                                            "Status",
                                                                        ]
                                                                    ),
                                                                ),
                                                            ],
                                                            value="subject4",
                                                        ),
                                                    ],
                                                    styles={
                                                        "root": {
                                                            "backgroundColor": dmc.theme.DEFAULT_COLORS[
                                                                "gray"
                                                            ][
                                                                0
                                                            ],
                                                            "borderRadius": 5,
                                                        },
                                                        "control": {
                                                            "font-family": "Roboto",
                                                            "font-weight": "300",
                                                            "font-size": "1em",
                                                        },
                                                        "item": {
                                                            "backgroundColor": dmc.theme.DEFAULT_COLORS[
                                                                "gray"
                                                            ][
                                                                0
                                                            ],
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
                                                                ][
                                                                    2
                                                                ],
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
                                            value="number",
                                        ),
                                    ],
                                    value="graph",
                                    color=mainColors["burgandy"],
                                    orientation="horizontal",
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
                                                    + str(
                                                        subjectPerformance[
                                                            "bestSubject"
                                                        ]
                                                    )
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
                                                    + str(
                                                        subjectPerformance[
                                                            "worstSubject"
                                                        ]
                                                    )
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
                                                    icon=DashIconify(
                                                        icon="bi:lightbulb"
                                                    ),
                                                ),
                                                dmc.AccordionPanel(
                                                    "Books to Study for "
                                                    + str(
                                                        subjectPerformance[
                                                            "worstSubject"
                                                        ]
                                                    )
                                                    + ":"
                                                ),
                                                dmc.AccordionPanel(
                                                    subjectRecommendation.loc[
                                                        0,
                                                        subjectPerformance[
                                                            "worstSubject"
                                                        ],
                                                    ]
                                                ),
                                                dmc.AccordionPanel(
                                                    subjectRecommendation.loc[
                                                        1,
                                                        subjectPerformance[
                                                            "worstSubject"
                                                        ],
                                                    ]
                                                ),
                                                dmc.AccordionPanel(
                                                    subjectRecommendation.loc[
                                                        2,
                                                        subjectPerformance[
                                                            "worstSubject"
                                                        ],
                                                    ]
                                                ),
                                            ],
                                            style={"font-size": "0,8em"},
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
    return dashboardLayout


def generateAboutUsLayout():
    aboutUsLayout = html.Div(
        children=[
            dmc.Center(
                className="mt-5 mb-5",
                style={
                    "width": "100%",
                    "font-family": "Roboto",
                    "font-weight": "500",
                    "font-size": "1.5em",
                },
                children=[
                    html.Div(
                        style={
                            "background-color": mainColors["uclaBlue"],
                        },
                        className="text-white rounded shadow p-3",
                        children="About Us",
                    )
                ],
            ),
            dmc.Grid(
                className="text-center m-5",
                children=[
                    dmc.Col(
                        html.Div(
                            dmc.Card(
                                children=[
                                    dmc.CardSection(
                                        dmc.Image(
                                            src="../assets/max.jpeg",
                                            height=160,
                                        )
                                    ),
                                    dmc.Group(
                                        [
                                            dmc.Text("Max Benedict Chavez", weight=500),
                                            dmc.Badge(
                                                "Lead Developer",
                                                color="red",
                                                variant="light",
                                            ),
                                        ],
                                        position="apart",
                                        mt="md",
                                        mb="xs",
                                    ),
                                    dmc.Text(
                                        "The Programmer and the Project Manager of the Team",
                                        size="sm",
                                        color="dimmed",
                                    ),
                                ],
                                withBorder=True,
                                shadow="sm",
                                radius="md",
                                style={"width": 350},
                            )
                        ),
                        span=4,
                    ),
                    dmc.Col(
                        html.Div(
                            dmc.Card(
                                children=[
                                    dmc.CardSection(
                                        dmc.Image(
                                            src="../assets/Jasper.jpg",
                                            height=160,
                                        )
                                    ),
                                    dmc.Group(
                                        [
                                            dmc.Text("Jasper Valdez", weight=500),
                                            dmc.Badge(
                                                "Lead Documentation",
                                                color="red",
                                                variant="light",
                                            ),
                                        ],
                                        position="apart",
                                        mt="md",
                                        mb="xs",
                                    ),
                                    dmc.Text(
                                        "Did the Documentation of the Team and Designed the Website",
                                        size="sm",
                                        color="dimmed",
                                    ),
                                ],
                                withBorder=True,
                                shadow="sm",
                                radius="md",
                                style={"width": 350},
                            )
                        ),
                        span=4,
                    ),
                    dmc.Col(
                        html.Div(
                            dmc.Card(
                                children=[
                                    dmc.CardSection(
                                        dmc.Image(
                                            src="../assets/Shan.jpg",
                                            height=160,
                                        )
                                    ),
                                    dmc.Group(
                                        [
                                            dmc.Text("Shanteiy Camama", weight=500),
                                            dmc.Badge(
                                                "Lead Designer",
                                                color="red",
                                                variant="light",
                                            ),
                                        ],
                                        position="apart",
                                        mt="md",
                                        mb="xs",
                                    ),
                                    dmc.Text(
                                        "Designed the Majority of the Website",
                                        size="sm",
                                        color="dimmed",
                                    ),
                                ],
                                withBorder=True,
                                shadow="sm",
                                radius="md",
                                style={"width": 350},
                            )
                        ),
                        span=4,
                    ),
                ],
                gutter="xl",
            ),
        ]
    )
    return aboutUsLayout


def generaterSupportLayout():
    supportLayout = html.Div(
        children=[
            dmc.Center(
                className="mt-5 mb-5",
                style={
                    "width": "100%",
                    "font-family": "Roboto",
                    "font-weight": "500",
                    "font-size": "1.5em",
                },
                children=[
                    html.Div(
                        style={
                            "background-color": mainColors["uclaBlue"],
                        },
                        className="text-white rounded shadow p-3",
                        children="Support and Frequently Asked Questions",
                    )
                ],
            ),
            dmc.Center(
                dmc.Accordion(
                    value="flexibility",
                    children=[
                        dmc.AccordionItem(
                            [
                                dmc.AccordionControl(
                                    "Where can I access the Recommended Topics?"
                                ),
                                dmc.AccordionPanel(
                                    "You can find your recommended topics in the right part of the dashboard"
                                ),
                            ],
                            value="customization",
                        ),
                        dmc.AccordionItem(
                            [
                                dmc.AccordionControl(
                                    "Do you need to have an account to access the dashboard"
                                ),
                                dmc.AccordionPanel(
                                    "You need to have an account to acccess the dashboard"
                                ),
                            ],
                            value="flexibility",
                        ),
                        dmc.AccordionItem(
                            [
                                dmc.AccordionControl(
                                    "What type of account can I use to access the dashboard"
                                ),
                                dmc.AccordionPanel(
                                    "You can use the accounts that your school gives to you to access the dashboard"
                                ),
                            ],
                            value="ring",
                        ),
                    ],
                    styles={
                        "root": {
                            "backgroundColor": dmc.theme.DEFAULT_COLORS["gray"][0],
                            "borderRadius": 5,
                        },
                        "control": {
                            "font-family": "Roboto",
                            "font-weight": "500",
                            "font-size": "1em",
                        },
                        "item": {
                            "backgroundColor": dmc.theme.DEFAULT_COLORS["gray"][0],
                            "border": "1px solid transparent",
                            "position": "relative",
                            "zIndex": 0,
                            "transition": "transform 150ms ease",
                            "&[data-active]": {
                                "transform": "scale(1.03)",
                                "backgroundColor": "white",
                                "boxShadow": 5,
                                "borderColor": dmc.theme.DEFAULT_COLORS["gray"][2],
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
            ),
        ]
    )
    return supportLayout


login_dict = {"login": False}

emails = studentList.index.to_numpy()
passwords = studentList["Student_Password"].to_numpy()


@app.callback(
    Output("output1", "children"),
    [Input("submit", "n_clicks")],
    State("email", "value"),
    State("password", "value"),
)
def update_output(n_clicks, email, password):
    if email == "" and password == "":
        return ""
    elif password in passwords and email in emails:
        login_dict["login"] = True
        currentStudent_dict["current_student"] = email
        currentStudentInfo["currentStudentName"] = studentList.loc[
            currentStudent_dict["current_student"],
            "Student_Names",
        ]
        currentStudentInfo["currentStudentData"] = studentList.loc[
            currentStudent_dict["current_student"],
            "Student_Data",
        ]
        studentDatas["studentData"] = pd.read_csv(
            currentStudentInfo["currentStudentData"]
        )
        studentDatas["studentData"] = studentDatas["studentData"].set_index("Subjects")
        subjects = studentDatas["studentData"].index.values
        studentDatas["studentData"]["Status"] = [
            "Failed" if value < 75 else "Passed"
            for value in studentDatas["studentData"]["Performance"]
        ]
        color_grades = {"Passed": mainColors["green"], "Failed": mainColors["burgandy"]}

        subjectPerformance = {
            "bestSubject": studentDatas["studentData"]["Performance"].idxmax(axis=0),
            "bestSubjectGrade": studentDatas["studentData"]["Performance"].max(axis=0),
            "worstSubject": studentDatas["studentData"]["Performance"].idxmin(axis=0),
            "worstSubjectGrade": studentDatas["studentData"]["Performance"].min(axis=0),
        }

        subjectRecommendation = pd.read_csv("subjectRecommendation.csv")
        return html.Div(children=dcc.Link("Access Granted", href="/dashboard"))
    else:
        return "Access Denied"


# Create the callback to handle mutlipage inputs
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")],
)
def display_page(pathname):
    if pathname == "/dashboard" and login_dict["login"] == True:
        return generateDashboardLayout()
    if pathname == "/home" and login_dict["login"] == True:
        return generateHomeLayout()
    if pathname == "/logOutStudent" or login_dict["login"] == False:
        login_dict["login"] = False
        return generateChangeStudentLayout()
    if pathname == "/changeStudent" or login_dict["login"] == False:
        return generateChangeStudentLayout()
    if pathname == "/aboutUs" or login_dict["login"] == False:
        return generateAboutUsLayout()
    if pathname == "/support" or login_dict["login"] == False:
        return generaterSupportLayout()
    else:  # if redirected to unknown link
        return "404 Page Error! Kinaadman Learning Dashboard Does Not Have This Page"


# Run the app on localhost:8050
if __name__ == "__main__":
    app.run_server(debug=False)
