#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 15:47:14 2024

@author: Javi
"""

# This is good too because it has the host URL

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from dash import dash_table
import numpy as np

# This code will read the CSV file and convert it to a dataframe.
df = pd.read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2023/2023-12-05/life_expectancy.csv")

# Define a function to calculate the three-number summary with Year (excluding 25th and 75th percentiles)
def calculate_three_number_summary(data, year):
    summary_values = [
        {"Summary": "Minimum", "Value": np.min(data), "Year": year[np.argmin(data)]},
        {"Summary": "Median", "Value": np.median(data), "Year": year[int(np.argsort(data)[len(data)//2])]},
        {"Summary": "Maximum", "Value": np.max(data), "Year": year[np.argmax(data)]}
    ]
    return summary_values

# Initialize the Dash Application
app = dash.Dash(__name__)
server = app.server

# This is where we create the layout of the dashboard.
app.layout = html.Div([
    html.H1("Life Expectancy Dashboard", style={"textAlign": "center"}),

    # Dropdown for 'Entity' choice for the first plot.
    dcc.Dropdown(
        id="entity-dropdown",
        options=[{"label": Entity, "value": Entity} for Entity in df["Entity"].unique()],
        value=df["Entity"].iloc[0],
        multi=False,
        style={"width": "50%"}
    ),

    # First Scatter Plot
    dcc.Graph(id="LifeExpectancy-Graph"),

    # Display the three-number summary values for the first plot as a table
    dash_table.DataTable(
        id="summary-table1",
        columns=[
            {"name": "Summary", "id": "Summary"},
            {"name": "Value", "id": "Value"},
            {"name": "Year", "id": "Year"}
        ],
        style_table={"height": "200px", "overflowY": "auto"},
    ),

    # Add a horizontal line for separation and new dropdowns for the second scatter plot.
    html.Hr(),
    html.H3("Second Scatter Plot for Comparison", style={"textAlign": "center"}),

    # Dropdown for entity choice in the second plot.
    dcc.Dropdown(
        id="entity-dropdown2",
        options=[{"label": Entity, "value": Entity} for Entity in df["Entity"].unique()],
        value=df["Entity"].iloc[1],  # Default to the second entity for comparison
        multi=False,
        style={"width": "50%"}
    ),

    # Second Scatter Plot
    dcc.Graph(id="Comparison-Graph"),

    # Display the three-number summary values for the second plot as a table
    dash_table.DataTable(
        id="summary-table2",
        columns=[
            {"name": "Summary", "id": "Summary"},
            {"name": "Value", "id": "Value"},
            {"name": "Year", "id": "Year"}
        ],
        style_table={"height": "200px", "overflowY": "auto"},
    ),

])

# Define callback to update the first scatter plot and summary table based on user input
@app.callback(
    [Output("LifeExpectancy-Graph", "figure"),
     Output("summary-table1", "data")],
    [Input("entity-dropdown", "value")]
)
def update_first_plot(selected_entity):
    filtered_df = df[df["Entity"] == selected_entity]

    # Check if the filtered DataFrame is empty
    if filtered_df.empty:
        return px.scatter(), []

    # Use Plotly Express to create the first scatter plot
    fig = px.scatter(filtered_df, x="Year", y="LifeExpectancy",
                     title=f"Life Expectancy Over Years - {selected_entity}",
                     labels={"LifeExpectancy": "Life Expectancy (years)"})

    # Calculate three-number summary for the first plot
    life_expectancy_values = filtered_df["LifeExpectancy"].values
    year_values = filtered_df["Year"].values

    summary_values = calculate_three_number_summary(life_expectancy_values, year_values)

    return fig, summary_values

# Define callback to update the second scatter plot and its summary table based on user input
@app.callback(
    [Output("Comparison-Graph", "figure"),
     Output("summary-table2", "data")],
    [Input("entity-dropdown2", "value")]
)
def update_second_plot(selected_entity):
    filtered_df = df[df["Entity"] == selected_entity]

    # Check if the filtered DataFrame is empty
    if filtered_df.empty:
        return px.scatter(), []

    # Use Plotly Express to create the second scatter plot
    fig = px.scatter(filtered_df, x="Year", y="LifeExpectancy",
                     title=f"Life Expectancy Over Years - {selected_entity} (Comparison)",
                     labels={"LifeExpectancy": "Life Expectancy (years)"})

    # Calculate three-number summary for the second plot
    life_expectancy_values = filtered_df["LifeExpectancy"].values
    year_values = filtered_df["Year"].values

    summary_values = calculate_three_number_summary(life_expectancy_values, year_values)

    return fig, summary_values

# Run the app and print the URL
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
    print(f"Dash app is running at: http://127.0.0.1:8050/")
