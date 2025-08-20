from dash import Input, Output, callback, html
import plotly.express as px
import pandas as pd
from datetime import datetime
from utils.data_io import read_root_csv


# Populate Monthly Average for Needs/Wants
@callback(
    Output("needs-cc", "value"),
    Output("wants-cc", "value"),
    Input("budget-date-method", "value"),
    Input("budget-date-year", "value"),
)
def populate_monthly_avg_needs_wants(method, selected_year):
    """
    Calculates the monthly average spending for Needs and Wants
    depending on the selected date filter.
    """
    df = read_root_csv()
    if df is None or df.empty:
        return 0, 0

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    if df["Date"].isnull().all():
        return 0, 0

    # Apply the selected date filter
    if method == "all":
        filtered = df
    elif method == "last12":
        cutoff = datetime.today() - pd.DateOffset(months=12)
        filtered = df[df["Date"] >= cutoff]
    elif method == "by_year" and selected_year:
        filtered = df[df["Date"].dt.year == int(selected_year)]
    elif method == "custom":
        return None, None
    else:
        filtered = df

    if filtered.empty:
        return 0, 0

    # Monthly totals
    filtered["Month"] = filtered["Date"].dt.to_period("M")
    monthly = filtered.groupby(["Month", "Necessity"])["Amount"].sum().reset_index()

    # Monthly averages
    needs_avg = monthly[monthly["Necessity"] == "Needs"]["Amount"].mean()
    wants_avg = monthly[monthly["Necessity"] == "Wants"]["Amount"].mean()

    needs_avg = round(needs_avg, 2) if pd.notnull(needs_avg) else 0
    wants_avg = round(wants_avg, 2) if pd.notnull(wants_avg) else 0

    return needs_avg, wants_avg


# Update Budget Pie Chart & Performance
@callback(
    Output("budget-pie-chart", "figure"),
    Output("needs-performance", "children"),
    Output("wants-performance", "children"),
    Output("savings-performance", "children"),
    Input("needs-cc", "value"),
    Input("needs-housing", "value"),
    Input("needs-other", "value"),
    Input("wants-cc", "value"),
    Input("wants-other", "value"),
    Input("savings-input", "value")
)
def update_budget_chart(needs_cc, needs_housing, needs_other, wants_cc, wants_other, savings_val):
    # Calculate totals
    needs_total = sum(v or 0 for v in [needs_cc, needs_housing, needs_other])
    wants_total = sum(v or 0 for v in [wants_cc, wants_other])
    savings_total = savings_val or 0

    total = needs_total + wants_total + savings_total
    if total == 0:
        return px.pie(values=[1], names=["No data"], title="No Budget Data"), "", "", ""

    # Pie chart
    fig = px.pie(
        names=["Needs", "Wants", "Savings"],
        values=[needs_total, wants_total, savings_total],
        title="Budget Distribution",
        hole=0.4
    )

    # Performance indicators (50-30-20)
    target = {"Needs": 50, "Wants": 30, "Savings": 20}
    actual = {
        "Needs": (needs_total / total) * 100,
        "Wants": (wants_total / total) * 100,
        "Savings": (savings_total / total) * 100
    }

    def perf_text(label):
        diff = actual[label] - target[label]
        arrow = "⬆️" if diff > 0 else "⬇️" if diff < 0 else "➡️"

        # Neutral color for Needs, red/green for Wants and Savings
        if label == "Needs":
            color = "black"
        else:
            color = "green" if (label == "Savings" and diff > 0) or (label == "Wants" and diff < 0) else "red"
        return html.Div(f"{label}: {actual[label]:.1f}% ({arrow} {abs(diff):.1f}%)", style={"color": color})

    return fig, perf_text("Needs"), perf_text("Wants"), perf_text("Savings")


# Toggle Year Dropdown and Enable Custom Inputs
@callback(
    Output("budget-date-year-container", "style"),
    Output("needs-cc", "disabled"),
    Output("wants-cc", "disabled"),
    Input("budget-date-method", "value")
)
def toggle_budget_date_inputs(method):
    # Show year dropdown only for "by_year"
    year_style = {"display": "block"} if method == "by_year" else {"display": "none"}
    
    # Enable credit card inputs only for custom
    cc_disabled = False if method == "custom" else True

    return year_style, cc_disabled, cc_disabled
