import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from . import callbacks
from .components import credit_card_section, yearly_spending_section, results_display_section

dash.register_page(
    __name__,
    path="/tools/cashback",
    title="Cashback Calculator"
)

layout = dbc.Container([
    dcc.Location(id="url", refresh=False),

    html.H2("Credit Card Cashback Calculator", className="my-4 text-center"),

    credit_card_section(),

    yearly_spending_section(),

    results_display_section()
])
