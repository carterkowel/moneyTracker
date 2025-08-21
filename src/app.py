# Import Packages
import dash
from dash import Dash, html, dash_table, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import base64
import datetime
import io
import os
from dotenv import load_dotenv

from components import navbar, footer

# Initialize the app
app = dash.Dash(
    __name__,
    use_pages=True,   
    external_stylesheets=[
        dbc.themes.CERULEAN,
        dbc.icons.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css",
    ],  
    suppress_callback_exceptions=True,
    title='Expense Tracker App'
)

def serve_layout():
    return html.Div(
        [
            navbar,
            dbc.Container(
                dash.page_container,
                class_name='my-2'
            ),
            footer
        ]
    )

app.layout = serve_layout

if __name__ == '__main__':
    app.run(debug=True)