from dash import html
import dash_bootstrap_components as dbc
import pandas as pd

def load_card_currentness(df):
    try:
        if df is None or df.empty:
            return html.Div("📭 No data yet.")

        temp_df = df.copy()
        temp_df['Date'] = pd.to_datetime(temp_df['Date'])

        cards = []
        for card_name in ['bmo_cashback', 'scotia_scene', 'scotia_momentum']:
            if card_name in temp_df['Card'].unique():
                most_recent = temp_df[temp_df['Card'] == card_name]['Date'].max()
                days_since = (pd.Timestamp.today() - most_recent).days

                if days_since <= 7:
                    message = html.H5("Up To Date!", style={"color": "green", "margin": 0})
                else:
                    message = html.H5(f"{days_since} days out of date", style={"color": "red", "margin": 0})
                
                subtitle = html.P(f"💳 {card_name.replace('_', ' ').title()}", className="card-subtitle", style={"fontWeight": "bold"})

                cards.append(
                    dbc.Card(
                        dbc.CardBody([subtitle, message]),
                        className="m-1 p-2 shadow-sm text-center",
                        style={"width": "18rem", "borderRadius": "10px"}
                    )
                )

        return dbc.Row(cards, className="g-2 d-flex justify-content-center")

    except Exception as e:
        return html.Div(f"⚠️ Error generating summary: {e}", style={'color': 'red'})
