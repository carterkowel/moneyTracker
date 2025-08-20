from dash import html
import dash_bootstrap_components as dbc

def performance_markers():
    return dbc.Row([
        dbc.Col(html.Div(id="needs-performance", className="text-center"), width=4),
        dbc.Col(html.Div(id="wants-performance", className="text-center"), width=4),
        dbc.Col(html.Div(id="savings-performance", className="text-center"), width=4),
    ], className="my-4")
