import dash_bootstrap_components as dbc
from dash import html

def results_display_section():
    return dbc.Row([
        dbc.Col([
            html.H4("Net Value"),
            html.Div(id="net-value", className="mb-1"),
            html.Small(id="net-value-subtext", className="text-muted")
        ], width=6)
    ])
