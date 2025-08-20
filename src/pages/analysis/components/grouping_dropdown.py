from dash import dcc, html
import dash_bootstrap_components as dbc

def grouping_dropdown_row():
    return dbc.Row([
        dbc.Col(
            html.H4("Sort By:", style={"marginBottom": "0", "display": "inline-block"}),
            width="auto",
            style={"paddingRight": "10px", "display": "flex", "alignItems": "center"}
        ),
        dbc.Col(
            dcc.Dropdown(
                id="grouping-dropdown",
                options=[
                    {"label": "Card Type", "value": "Card"},
                    {"label": "Category", "value": "Category"},
                    {"label": "Necessity", "value": "Necessity"}
                ],
                value="Category",
                clearable=False,
                style={"minWidth": "200px"}
            ),
            width="auto",
            style={"display": "flex", "alignItems": "center"}
        )
    ], className="mb-4", style={"alignItems": "center"})
