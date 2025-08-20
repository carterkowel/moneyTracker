import dash_bootstrap_components as dbc
from dash import html, dcc

def yearly_spending_section(year_options=None):
    return dbc.Row([
        dbc.Col([
            html.H4("Yearly Spending"),

            # Dropdown to choose method
            html.Div("Annual Average Method", className="mb-1"),
            dcc.Dropdown(
                id="yearly-method",
                options=[
                    {"label": "All Data", "value": "all"},
                    {"label": "Last 12 Months", "value": "last12"},
                    {"label": "By Year", "value": "by_year"},
                    {"label": "Custom", "value": "custom"},
                ],
                value="custom",
                clearable=False,
                className="mb-3"
            ),

            # Year selection (hidden unless method == by_year)
            html.Div([
                html.Div("Select Year", className="mb-1"),
                dcc.Dropdown(
                    id="yearly-year",
                    options=[{"label": str(y), "value": y} for y in (year_options or [])],
                    value=year_options[-1] if year_options else None,
                    clearable=False,
                    className="mb-3"
                ),
            ], id="yearly-year-container", style={"display": "none"}),

            # Groceries
            html.Div("Groceries", className="mb-1"),
            dbc.Input(id="yearly-groceries", type="number", disabled=True, className="mb-2"),

            # Other
            html.Div("Other", className="mb-1"),
            dbc.Input(id="yearly-other", type="number", disabled=True, className="mb-2"),
        ], width=4),
    ], className="mb-4")
