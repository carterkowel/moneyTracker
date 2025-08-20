
from dash import Input, Output, State, callback, html
import pandas as pd
import datetime as dt
from utils.data_io import read_root_csv
from utils import load_credit_cards

CREDIT_CARDS = load_credit_cards()

@callback(
    Output("yearly-groceries", "value"),
    Output("yearly-other", "value"),
    Output("yearly-groceries", "disabled"),
    Output("yearly-other", "disabled"),
    Output("net-value", "children"),
    Output("net-value-subtext", "children"),
    Input("yearly-method", "value"),
    Input("grocery-rate", "value"),
    Input("other-rate", "value"),
    Input("annual-cost", "value"),
    Input("yearly-groceries", "value"),
    Input("yearly-other", "value"),
    Input("yearly-year", "value"),
)
def update_yearly_spending_and_cashback(
    method, grocery_rate, other_rate, annual_cost,
    current_groceries, current_other, selected_year
):
    df = read_root_csv()
    if df is None or df.empty:
        return 0, 0, True, True, "", ""

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    if df["Date"].isnull().all():
        return 0, 0, True, True, "", ""

    df["Month"] = df["Date"].dt.to_period("M")

    groceries_annual, other_annual = 0, 0
    inputs_disabled = True

    if method == "all":
        groceries_annual = df[df["Category"] == "Groceries"].groupby("Month")["Amount"].sum().mean() * 12
        other_annual = df[df["Category"] != "Groceries"].groupby("Month")["Amount"].sum().mean() * 12

    elif method == "last12":
        cutoff = dt.datetime.today() - pd.DateOffset(months=12)
        recent = df[df["Date"] >= cutoff]
        if not recent.empty:
            recent["Month"] = recent["Date"].dt.to_period("M")
            groceries_annual = recent[recent["Category"] == "Groceries"].groupby("Month")["Amount"].sum().mean() * 12
            other_annual = recent[recent["Category"] != "Groceries"].groupby("Month")["Amount"].sum().mean() * 12

    elif method == "by_year" and selected_year:
        df_year = df[df["Date"].dt.year == selected_year]
        if not df_year.empty:
            df_year["Month"] = df_year["Date"].dt.to_period("M")
            groceries_annual = df_year[df_year["Category"] == "Groceries"].groupby("Month")["Amount"].sum().mean() * 12
            other_annual = df_year[df_year["Category"] != "Groceries"].groupby("Month")["Amount"].sum().mean() * 12

    elif method == "custom":
        groceries_annual, other_annual = current_groceries, current_other
        inputs_disabled = False

    # Cashback calculation
    grocery_rate = grocery_rate or 0
    other_rate = other_rate or 0
    annual_cost = annual_cost or 0

    cashback_grocery = (groceries_annual or 0) * grocery_rate / 100
    cashback_other = (other_annual or 0) * other_rate / 100
    total_cashback = cashback_grocery + cashback_other

    net_value = total_cashback - annual_cost
    net_color = "green" if net_value >= 0 else "red"

    net_value_div = html.Div(f"${net_value:,.2f}", style={"color": net_color, "font-weight": "bold"})
    subtext_div = html.Div([
        html.Div(f"Grocery Cashback Earned: ${cashback_grocery:,.2f}"),
        html.Div(f"Other Cashback Earned: ${cashback_other:,.2f}"),
        html.Div(f"Card Annual Cost: ${annual_cost:,.2f}")
    ], style={"font-size": "0.9rem", "color": "gray"})

    return (
        round(groceries_annual or 0, 2),
        round(other_annual or 0, 2),
        inputs_disabled,
        inputs_disabled,
        net_value_div,
        subtext_div
    )



@callback(
    Output("grocery-rate", "value"),
    Output("other-rate", "value"),
    Output("annual-cost", "value"),
    Output("grocery-rate", "disabled"),
    Output("other-rate", "disabled"),
    Output("annual-cost", "disabled"),
    Input("credit-card-dropdown", "value"),
    State("grocery-rate", "value"),
    State("other-rate", "value"),
    State("annual-cost", "value"),
)
def autofill_card_parameters(selected_card, grocery_rate, other_rate, annual_cost):
    card = next((c for c in CREDIT_CARDS if c["name"] == selected_card), None)

    if not card or card["name"] == "Custom":
        # Enable editing for custom card
        return grocery_rate, other_rate, annual_cost, False, False, False

    # Disable editing for preset cards
    return card["grocery_rate"], card["other_rate"], card["annual_cost"], True, True, True

@callback(
    Output("yearly-year-container", "style"),
    Input("yearly-method", "value"),
)
def toggle_year_dropdown(method):
    if method == "by_year":
        return {"display": "block"}
    return {"display": "none"}


@callback(
    Output("yearly-year", "options"),
    Output("yearly-year", "value"),
    Input("yearly-method", "value"),
)
def populate_year_dropdown(method):
    if method != "by_year":
        return [], None

    df = read_root_csv()
    if df is None or df.empty or "Date" not in df:
        return [], None

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    years = sorted(df["Date"].dt.year.dropna().unique())

    if not years:
        return [], None

    return (
        [{"label": str(y), "value": int(y)} for y in years],
        int(years[-1])  # default = most recent year
    )