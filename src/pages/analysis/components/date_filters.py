import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd

def date_filter_section(year_options=None, min_date=None, max_date=None):
    # Ensure min_date and max_date are proper strings for DatePickerSingle
    min_date_str = pd.to_datetime(min_date).date() if min_date is not None else None
    max_date_str = pd.to_datetime(max_date).date() if max_date is not None else None

    return dbc.Row([
        dbc.Col([
            html.H4("Date Filter"),

            # Dropdown to choose method
            html.Div("Select Range", className="mb-1"),
            dcc.Dropdown(
                id="analysis-date-method",
                options=[
                    {"label": "All Data", "value": "all"},
                    {"label": "Last 12 Months", "value": "last12"},
                    {"label": "By Year", "value": "by_year"},
                    {"label": "Custom Range", "value": "custom"},
                ],
                value="all",
                clearable=False,
                className="mb-3"
            ),

            # Year selection (hidden unless by_year)
            html.Div([
                html.Div("Select Year", className="mb-1"),
                dcc.Dropdown(
                    id="analysis-date-year",
                    options=[{"label": str(y), "value": y} for y in (year_options or [])],
                    value=year_options[-1] if year_options else None,
                    clearable=False,
                    className="mb-3"
                ),
            ], id="analysis-date-year-container", style={"display": "none"}),

            # Start / End dates (only shown for custom)
            html.Div([
                html.Div("Start Date", className="mb-1"),
                dcc.DatePickerSingle(
                    id="analysis-start-date",
                    date=min_date_str,
                    display_format="YYYY-MM-DD",
                    className="mb-3"
                ),
                html.Div("End Date", className="mb-1"),
                dcc.DatePickerSingle(
                    id="analysis-end-date",
                    date=max_date_str,
                    display_format="YYYY-MM-DD"
                ),
            ], id="analysis-custom-dates-container", style={"display": "none"}),
        ], width=4),
    ], className="mb-4")
