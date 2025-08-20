import dash
from dash import html, dcc
from . import callbacks
from .components import budget_inputs, performance_markers

dash.register_page(
    __name__,
    path="/tools/50_30_20",
    title="50-30-20 Budgeting"
)

layout = html.Div([
    dcc.Location(id="url", refresh=False),

    html.H2("50-30-20 Budgeting Tool", className="my-4 text-center"),

    budget_inputs(),

    dcc.Graph(id="budget-pie-chart"),

    html.Hr(),

    performance_markers(),
])