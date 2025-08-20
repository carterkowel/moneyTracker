import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
from utils.data_io import read_root_csv

def budget_inputs():
    df = read_root_csv()
    year_options = []

    if df is not None and "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        year_options = sorted(df["Date"].dt.year.dropna().unique(), reverse=True)

    # Date filter section
    date_filter = dbc.Row([
        # Select Range Dropdown
        dbc.Col([
            html.H4("Date Filter"),
            html.Div("Select Range", className="mb-1"),
            dcc.Dropdown(
                id="budget-date-method",
                options=[
                    {"label": "All Data", "value": "all"},
                    {"label": "Last 12 Months", "value": "last12"},
                    {"label": "By Year", "value": "by_year"},
                    {"label": "Custom", "value": "custom"},
                ],
                value="all",
                clearable=False,
                className="mb-3"
            ),
        ], width=4),

        # Year Dropdown (shown only when By Year is selected)
        dbc.Col([
            html.Div("Select Year", className="mb-1"),
            dcc.Dropdown(
                id="budget-date-year",
                options=[{"label": str(y), "value": y} for y in (year_options or [])],
                value=year_options[0] if year_options else None,
                clearable=False,
                className="mb-3"
            ),
        ], id="budget-date-year-container", width=2, style={"display": "none"}),  # initially hidden
    ], className="mb-4", align="end")  # align the dropdowns vertically at bottom

    # Original Needs/Wants/Savings inputs
    inputs_row = dbc.Row([
        dbc.Col([
            html.H4("Needs"),
            html.Div("Credit Card", className="mb-1"),
            dbc.Input(id="needs-cc", type="number", disabled=True, className="mb-2"),

            html.Div("Housing", className="mb-1"),
            dbc.Input(id="needs-housing", type="number", placeholder="e.g. 1400 (rent + utilities + insurance)", className="mb-2"),

            html.Div("Other", className="mb-1"),
            dbc.Input(id="needs-other", type="number", className="mb-2"),
        ], width=4),

        dbc.Col([
            html.H4("Wants"),
            html.Div("Credit Card", className="mb-1"),
            dbc.Input(id="wants-cc", type="number", disabled=True, className="mb-2"),

            html.Div("Other", className="mb-1"),
            dbc.Input(id="wants-other", type="number", className="mb-2"),
        ], width=4),

        dbc.Col([
            html.H4("Savings"),
            html.Div("Monthly Savings", className="mb-1"),
            dbc.Input(id="savings-input", type="number", placeholder="e.g. 1000", className="mb-2"),
        ], width=4)
    ])

    return html.Div([date_filter, inputs_row])