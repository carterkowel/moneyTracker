import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
import pandas as pd


from utils import read_root_csv
from .components import load_card_currentness, load_root_table, upload_statements, editor_toggle
from . import callbacks

initial_df = read_root_csv()

dash.register_page(
    __name__,
    path="/",
    title="Edit & Upload"
)

layout = html.Div([
    dcc.Store(id='csv-updated-flag', storage_type='memory'),
    dcc.Location(id="url", refresh=False),

    html.H1("Edit & Upload"),
    html.Hr(),

    upload_statements(),

    html.Div(
        load_card_currentness(initial_df),
        id="transaction-summary",
        style={"marginTop": "1rem"}
    ),

    html.Hr(),
    html.H4("Edit Transactions"),

    dbc.Button(
        "Upload & Auto-Categorize Processed Transactions",
        id="run-updater-btn",
        color="success",
        className="mt-3"
    ),
    html.Div(
        id="run-updater-output",
        style={"whiteSpace": "pre-wrap", "marginTop": "1rem"}
    ),

    editor_toggle(),

    html.Div(
        load_root_table(initial_df),
        id="root-table-container",
        style={"marginTop": "1rem"}
    ),

    dcc.Store(id="temp-df-store", storage_type="memory"),
])