
import dash
import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc


from utils import read_root_csv
from . import callbacks
from .components import date_filter_section, grouping_dropdown_row


# Load initial data for default dates
initial_df = read_root_csv()
year_options = []

if initial_df is not None and "Date" in initial_df.columns:
    initial_df["Date"] = pd.to_datetime(initial_df["Date"], errors="coerce")
    year_options = sorted(initial_df["Date"].dt.year.dropna().unique(), reverse=True)
    min_date = initial_df["Date"].min()
    max_date = initial_df["Date"].max()

dash.register_page(
    __name__,
    path="/analysis",
    title="Analysis"
)

layout = html.Div([
    dcc.Location(id="url", refresh=False),

    html.H1("Spending Analysis"),
    html.Hr(),

    date_filter_section(year_options=year_options, min_date=min_date, max_date=max_date),

    grouping_dropdown_row(),

    # Line Chart
    dcc.Graph(id="monthly-spending-chart"),

    # Bar Chart
    dcc.Graph(id="average-monthly-spending-bar-chart")
])
