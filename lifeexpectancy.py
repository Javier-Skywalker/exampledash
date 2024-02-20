#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 15:47:14 2024

@author: Javi
"""

# This is good too because it has the host url

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# This code will read the CSV file and convert it to a dataframe.
df = pd.read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2023/2023-12-05/life_expectancy.csv")

# Initialize the Dash Application
app = dash.Dash(__name__)

# This is where we create the layout of the dashboard.
app.layout = html.Div([
    html.H1("Life Expectancy Dashboard"),
    
    dcc.Dropdown(
        id="entity-dropdown",
        options=[{"label": Entity, "value": Entity} for Entity in df["Entity"].unique()],
        value=df["Entity"].iloc[0],
        multi=False,
        style={"width": "50%"}
    ),
    
    dcc.Graph(id="LifeExpectancy-Graph")
])

# Define callback to update the graph based on user input
@app.callback(
    Output("LifeExpectancy-Graph", "figure"),
    [Input("entity-dropdown", "value")]
)
def update_graph(selected_entity):
    filtered_df = df[df["Entity"] == selected_entity]

    # Use Plotly Express to create a line graph
    fig = px.scatter(filtered_df, x="Year", y="LifeExpectancy", 
                  title=f"Life Expectancy Over Years - {selected_entity}",
                  labels={"LifeExpectancy": "Life Expectancy (years)"})

    return fig

# Run the app and print the URL
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
    print(f"Dash app is running at: http://127.0.0.1:8050/")
