import dash_bootstrap_components as dbc
from dash import html, dcc

from utils import load_credit_cards

CREDIT_CARDS = load_credit_cards()

def credit_card_section():
    return dbc.Row([
        dbc.Col([
            html.H4("Credit Card"),

            # Card selection dropdown
            html.Div("Select Card", className="mb-1"),
            dcc.Dropdown(
                id="credit-card-dropdown",
                options=[{"label": card["name"], "value": card["name"]} for card in CREDIT_CARDS],
                value="Custom",
                clearable=False,
                className="mb-3"
            ),

            # Grocery cashback rate
            html.Div("Grocery Cashback Rate (%)", className="mb-1"),
            dbc.Input(
                id="grocery-rate",
                type="number",
                placeholder="e.g., 1.5",
                className="mb-2",
                disabled=False
            ),

            # Other cashback rate
            html.Div("Other Cashback Rate (%)", className="mb-1"),
            dbc.Input(
                id="other-rate",
                type="number",
                placeholder="e.g., 0.5",
                className="mb-2",
                disabled=False
            ),

            # Annual card cost
            html.Div("Annual Card Cost ($)", className="mb-1"),
            dbc.Input(
                id="annual-cost",
                type="number",
                placeholder="e.g., 120",
                className="mb-2",
                disabled=False
            ),
        ], width=4),
    ], className="mb-4")