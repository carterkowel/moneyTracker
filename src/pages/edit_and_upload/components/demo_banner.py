import dash_bootstrap_components as dbc
from dash import html
import os

from config.settings import DEMO_MODE

def get_demo_banner():
    """
    Returns a demo mode banner is in demo mode.
    """
    if DEMO_MODE:
        return dbc.Alert(
            "⚠️ Demo Mode: Uploading and editing is disabled. Data is pre-filled.",
            color="info",
            dismissable=False,
            style={"textAlign": "center", "marginBottom": "1rem"}
        )
    else:
        return None